"""Graph-structural analysis of the C. elegans connectome and its null ladder.

Characterises each substrate's *binary topology* (the mask, before weights) on
classical graph descriptors, using the generic ``src.analysis.null_models``
tools. Companion to the spectral driver: that one explains the *weight*-placement
axis; this one makes the *topology* axis -- the null ladder itself -- legible,
showing what each rung preserves vs destroys relative to the connectome.

Scope. Null masks depend only on topology, not on the weight condition, so this
analysis uses the **directed** topology (the v2b/v2d family -- the biologically
realistic substrate) and the binary masks alone. The weight-placement control
``connectome_weight_permuted`` permutes weights only; its mask is *identical* to
the connectome, so it is a no-op here and is omitted. That leaves the clean
ladder: the connectome plus rungs 0-4.

    python -m experiments.celegans.analysis.null_models

Outputs (here):
  figures/degree_distributions.png  in/out-degree CCDFs (rungs 2-4 trace the connectome)
  figures/structural_metrics.png    per-metric bars: connectome reference + null spread
  figures/preservation_heatmap.png  rung x metric staircase (0 = random, 1 = connectome)
  results/structural_metrics.csv    seed-averaged metrics (+ sem) for every variant
  results/structural_metrics.md     compact markdown table (for slides)
"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np
import pandas as pd

from src.reservoir import blas  # noqa: F401  (limit BLAS threads; import early)
from src.analysis import null_models
from experiments.celegans.substrates import SubstrateBuilder
from experiments.celegans import matrix_config

_DIR = Path(__file__).resolve().parent
FIGURES_DIR = _DIR / "figures"
RESULTS_DIR = _DIR / "results"

TOPOLOGY = "directed"  # the biologically realistic substrate (v2b/v2d family)
# The connectome plus the 5-rung ladder. The placement control is omitted (its
# mask equals the connectome's -- a no-op on graph structure).
VARIANTS = ["connectome", "random_gaussian", "erdos_renyi",
            "degree_rewire", "clustering_rewire", "modularity_rewire"]
RANDOM_VARIANT = "random_gaussian"  # rung 0, the "as-random" anchor for the heatmap
N_SEEDS = matrix_config.N_SEEDS
REPRESENTATIVE_SEED = 0  # degree sequences aren't averageable; show one sampled graph

VARIANT_TITLE = {
    "connectome": "connectome",
    "random_gaussian": "rung 0 (random)",
    "erdos_renyi": "rung 1 (ER)",
    "degree_rewire": "rung 2 (degree)",
    "clustering_rewire": "rung 3 (clustering)",
    "modularity_rewire": "rung 4 (modularity)",
}
VARIANT_COLOR = {  # shared palette with the spectral driver
    "connectome": "black",
    "random_gaussian": "#bbbbbb",
    "erdos_renyi": "#88aadd",
    "degree_rewire": "#e377c2",
    "clustering_rewire": "#2ca02c",
    "modularity_rewire": "#ff7f0e",
}

# All scalar metrics (CSV + markdown table).
TABLE_METRICS = ["n_edges", "density", "clustering_global",
                 "clustering_directed_mean", "modularity_q", "reciprocity",
                 "mean_path_length", "global_efficiency"]
METRIC_TITLE = {
    "n_edges": "edge count",
    "density": "density",
    "clustering_global": "global clustering\n(transitivity)",
    "clustering_directed_mean": "directed clustering\n(mean Fagiolo)",
    "modularity_q": "modularity Q\n(fixed partition)",
    "reciprocity": "reciprocity\n(bidirectional frac.)",
    "mean_path_length": "mean path length",
    "global_efficiency": "global efficiency",
}
# Bars: drop the redundant raw edge count (density carries it).
BAR_METRICS = ["density", "clustering_global", "clustering_directed_mean",
               "modularity_q", "reciprocity", "mean_path_length",
               "global_efficiency"]
# Heatmap: the descriptors that live on the random->connectome axis (density is
# exact by construction for rungs 1-4, so its normalisation is degenerate).
HEATMAP_METRICS = ["clustering_global", "clustering_directed_mean",
                   "modularity_q", "reciprocity", "mean_path_length",
                   "global_efficiency"]
HEATMAP_COLUMNS = ["connectome", "random_gaussian", "erdos_renyi",
                   "degree_rewire", "clustering_rewire", "modularity_rewire"]
# Short, single-line metric labels for the heatmap rows.
HEATMAP_ROW_TITLE = {
    "clustering_global": "global clustering",
    "clustering_directed_mean": "directed clustering",
    "modularity_q": "modularity Q",
    "reciprocity": "reciprocity",
    "mean_path_length": "mean path length",
    "global_efficiency": "global efficiency",
}


def _seed_values(builder, partition) -> dict:
    """``seed_values[(metric, variant)]`` -> per-seed array of metric values.

    The connectome is one fixed graph (length-1 array, seed-invariant); each
    null is sampled over the configured seeds.
    """
    seed_values = {}
    for variant in VARIANTS:
        seeds = [REPRESENTATIVE_SEED] if variant == "connectome" else range(N_SEEDS)
        per_seed = [
            null_models.structural_metrics(
                builder.get_mask(TOPOLOGY, variant, seed), partition)
            for seed in seeds
        ]
        for metric in TABLE_METRICS:
            seed_values[(metric, variant)] = np.array(
                [m[metric] for m in per_seed], dtype=float)
    return seed_values


def _write_markdown_table(seed_values: dict, path: Path) -> None:
    lines = ["# C. elegans structural metrics (directed topology, seed-averaged)\n",
             "Graph descriptors of the binary mask (topology only, before weights). "
             "The connectome is one fixed graph; nulls are averaged over "
             f"{N_SEEDS} seeds (± sem). Rungs 2-4 preserve the degree sequence "
             "exactly, so they match the connectome on degree-derived quantities; "
             "each higher rung restores one more descriptor.\n"]
    header = "| variant | " + " | ".join(METRIC_TITLE[m].replace("\n", " ")
                                         for m in TABLE_METRICS) + " |"
    sep = "|" + "---|" * (1 + len(TABLE_METRICS))
    lines += [header, sep]
    for variant in VARIANTS:
        cells = []
        for metric in TABLE_METRICS:
            values = seed_values[(metric, variant)]
            mean = values.mean()
            if metric == "n_edges":
                cell = f"{mean:.0f}"
            elif metric == "density":
                cell = f"{mean:.4f}"
            else:
                cell = f"{mean:.3f}"
            if values.size > 1:
                cell += f" ± {values.std() / np.sqrt(values.size):.3f}"
            cells.append(cell)
        lines.append(f"| {VARIANT_TITLE[variant]} | " + " | ".join(cells) + " |")
    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    builder = SubstrateBuilder()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    partition = builder.partitions[TOPOLOGY]

    # --- per-seed scalar metrics for every variant ----------------------------
    seed_values = _seed_values(builder, partition)

    rows = []
    for variant in VARIANTS:
        row = dict(variant=variant, rung=matrix_config.VARIANT_RUNG.get(variant, ""))
        for metric in TABLE_METRICS:
            values = seed_values[(metric, variant)]
            row[metric] = float(values.mean())
            row[f"{metric}_sem"] = (float(values.std() / np.sqrt(values.size))
                                    if values.size > 1 else 0.0)
        rows.append(row)
    pd.DataFrame(rows).to_csv(RESULTS_DIR / "structural_metrics.csv", index=False)
    _write_markdown_table(seed_values, RESULTS_DIR / "structural_metrics.md")
    print(f"Saved {RESULTS_DIR / 'structural_metrics.csv'}")
    print(f"Saved {RESULTS_DIR / 'structural_metrics.md'}")

    # --- degree distributions (one representative sampled graph) --------------
    degree_data = {
        variant: null_models.degree_sequences(
            builder.get_mask(TOPOLOGY, variant, REPRESENTATIVE_SEED))
        for variant in VARIANTS
    }
    null_models.plot_degree_distributions(
        degree_data, VARIANTS, VARIANT_TITLE, VARIANT_COLOR, "connectome",
        FIGURES_DIR / "degree_distributions.png",
        suptitle="In/out-degree distributions (CCDF): rungs 2-4 trace the connectome",
    )
    print(f"Saved {FIGURES_DIR / 'degree_distributions.png'}")

    # --- metric bars (connectome reference + null spread) ---------------------
    null_models.plot_metric_bars(
        seed_values, BAR_METRICS, [METRIC_TITLE[m] for m in BAR_METRICS],
        VARIANTS, VARIANT_TITLE, VARIANT_COLOR, "connectome",
        FIGURES_DIR / "structural_metrics.png",
        suptitle="Graph-structural metrics by variant "
                 "(dashed line = connectome; bars = null seed-mean ± std)",
    )
    print(f"Saved {FIGURES_DIR / 'structural_metrics.png'}")

    # --- preservation heatmap (normalised random -> connectome) ---------------
    normalized = {}
    for metric in HEATMAP_METRICS:
        connectome_value = seed_values[(metric, "connectome")].mean()
        random_value = seed_values[(metric, RANDOM_VARIANT)].mean()
        for column in HEATMAP_COLUMNS:
            normalized[(metric, column)] = null_models.normalize_to_ladder(
                seed_values[(metric, column)].mean(),
                connectome_value, random_value)
    null_models.plot_preservation_heatmap(
        normalized, HEATMAP_METRICS,
        [HEATMAP_ROW_TITLE[m] for m in HEATMAP_METRICS], HEATMAP_COLUMNS,
        VARIANT_TITLE, FIGURES_DIR / "preservation_heatmap.png",
        suptitle="What each rung restores (0 = random, 1 = connectome)",
    )
    print(f"Saved {FIGURES_DIR / 'preservation_heatmap.png'}")

    # Slide-tuned variant of the same heatmap (the recommended headline figure):
    # larger fonts + aspect ratio for projection.
    null_models.plot_preservation_heatmap(
        normalized, HEATMAP_METRICS,
        [HEATMAP_ROW_TITLE[m] for m in HEATMAP_METRICS], HEATMAP_COLUMNS,
        VARIANT_TITLE, FIGURES_DIR / "preservation_heatmap_slide.png",
        suptitle="What each null model preserves (0 = random, 1 = connectome)",
        figsize=(11.0, 6.0), annotation_fontsize=12, label_fontsize=12,
        title_fontsize=15, cbar_fontsize=11,
    )
    print(f"Saved {FIGURES_DIR / 'preservation_heatmap_slide.png'}")

    # --- adjacency "ladder of pictures" (community-ordered spy plots) ---------
    # The most intuitive single visual: the connectome's diagonal community
    # blocks dissolve into random speckle (rung 0), stay gone under degree
    # preservation (rung 2), then snap back when modularity is restored (rung 4).
    order, boundaries = null_models.community_order(partition)
    ladder_variants = ["connectome", "random_gaussian", "degree_rewire",
                       "modularity_rewire"]
    ladder_masks = {
        variant: builder.get_mask(TOPOLOGY, variant, REPRESENTATIVE_SEED)
        for variant in ladder_variants
    }
    null_models.plot_adjacency_ladder(
        ladder_masks, ladder_variants, VARIANT_TITLE, order,
        FIGURES_DIR / "adjacency_ladder.png", boundaries=boundaries,
        suptitle="Connectome wiring vs nulls (nodes ordered by community): "
                 "blocks dissolve, then return at rung 4",
    )
    print(f"Saved {FIGURES_DIR / 'adjacency_ladder.png'}")

    # --- headline glance to stdout -------------------------------------------
    print("\nDirected topology — key descriptors (connectome vs nulls):")
    for metric in ["clustering_directed_mean", "modularity_q", "reciprocity"]:
        cells = "  ".join(
            f"{VARIANT_TITLE[v].split(' (')[0]}={seed_values[(metric, v)].mean():.3f}"
            for v in VARIANTS)
        print(f"  [{metric}] {cells}")
    print("\nDone.")


if __name__ == "__main__":
    main()
