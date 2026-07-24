"""Manifold-geometry probes on the human SC reservoir (Probes 1 to 3).

A driver package (was a single ``manifold.py``; split for readability). Invoked as

    python -m experiments.human.analysis.manifold --probe {1,2,3} [--scale N] [--jobs N] [--smoke]

- ``probe1`` -- dimensionality and shape (PR / curvature / entropy vs sr) + the
  correctness gate that reproduces the committed four-task runs bit-for-bit.
- ``probe2`` -- alignment of the activity manifold with structural bases
  (Laplacian harmonics vs dominant W-eigenmodes vs random).
- ``probe3`` -- geometry -> performance link (no new reservoir runs).
- ``common`` -- shared task specs, sweep resolution, the fork-parallel capture
  harness, palettes/titles, and CLI helpers. ``__main__`` dispatches on ``--probe``.

Nothing is trained and no frozen hyperparameter or the run matrix is touched: this
is the substrate-analysis tier (like ``spectral.py``). Outputs are scale-tagged and
land in ``experiments/human/analysis/{results,figures}/scale_<N>/``.
"""

import sys
from pathlib import Path

# Belt-and-suspenders path bootstrap (parity with the other analysis drivers) and
# the headless matplotlib backend, set once before any submodule imports pyplot.
_ROOT = Path(__file__).resolve().parents[4]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import matplotlib

matplotlib.use("Agg")
