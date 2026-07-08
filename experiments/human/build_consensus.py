"""Build + validate the self-derived human group consensus, then cache it.

Constructs our OWN distance-dependent consensus from the .mat individual SC (the
raw Lausanne source) via the vendored Betzel-2018 struct_consensus, validates it
against the published Suárez consensus (density, node strength, edge overlap,
shared-edge weight correlation), and caches it to data/human/built_consensus/ so
the probe loads it without reloading the 701 MB .mat.

    python -m experiments.human.build_consensus

Cached artifacts (gitignored, regenerable from this script):
  data/human/built_consensus/consensus_<scale>.npy       the substrate W
  data/human/built_consensus/consensus_<scale>.meta.json metadata + validation
"""

import sys
import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np

from src.connectomes.human_suarez import (
    build_consensus, load_published_consensus,
    build_consensus_full, load_published_consensus_full,
)

OUT = _ROOT / "data" / "human" / "built_consensus"
SCALES = [448, 1000]


def _validate(C: np.ndarray, Cpub: np.ndarray) -> dict:
    """Compare the self-built consensus C against the published Cpub."""
    N = C.shape[0]
    iu = np.triu_indices(N, k=1)
    e_ours, e_pub = C[iu] > 0, Cpub[iu] > 0
    n_pairs = len(iu[0])
    shared = e_ours & e_pub
    return dict(
        density_ours=float(e_ours.sum() / n_pairs),
        density_pub=float(e_pub.sum() / n_pairs),
        edges_ours=int(e_ours.sum()),
        edges_pub=int(e_pub.sum()),
        edge_jaccard=float((e_ours & e_pub).sum() / (e_ours | e_pub).sum()),
        node_strength_r=float(np.corrcoef(C.sum(1), Cpub.sum(1))[0, 1]),
        shared_edge_weight_r=(
            float(np.corrcoef(C[iu][shared], Cpub[iu][shared])[0, 1])
            if shared.sum() else float("nan")
        ),
    )


def main(full: bool = False) -> None:
    """Build + validate + cache the self-derived consensus for both scales.

    ``full=False`` -> the cortical-only consensus from the .mat (``consensus_<scale>``).
    ``full=True``  -> the with-subcortical consensus from the release individual
    stacks (``consensus_full_<scale>``, N=463/1015), for the I/O-routing thread.
    """
    build = build_consensus_full if full else build_consensus
    load_pub = load_published_consensus_full if full else load_published_consensus
    prefix = "consensus_full" if full else "consensus"
    kind = "with-subcortical " if full else "cortical "

    OUT.mkdir(parents=True, exist_ok=True)
    for scale in SCALES:
        print(f"\n{'='*66}\nBuilding self-derived {kind}consensus, scale N={scale}\n{'='*66}")
        cd = build(scale=scale, weighted=True)
        C = cd.adjacency
        Cpub = load_pub(scale)
        v = _validate(C, Cpub)

        np.save(OUT / f"{prefix}_{scale}.npy", C)
        (OUT / f"{prefix}_{scale}.meta.json").write_text(
            json.dumps({"metadata": cd.metadata, "validation_vs_published": v}, indent=2)
        )

        print(f"\nValidation vs published Suárez {kind}consensus (scale {scale}):")
        for k, val in v.items():
            print(f"    {k:22s}: {val:.4f}" if isinstance(val, float)
                  else f"    {k:22s}: {val}")
        print(f"  cached -> {OUT / f'{prefix}_{scale}.npy'}")

    print("\nDone.")


if __name__ == "__main__":
    main(full="--full" in sys.argv)
