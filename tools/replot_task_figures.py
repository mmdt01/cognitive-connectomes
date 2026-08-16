"""Re-render the per-task figures from frozen results. No simulation.

Needed whenever the shared variant palette moves: `src/experiment/plots._VARIANT_STYLE`
is the colour source for every `*_vs_spectral_radius.png` / `*_factorial.png` under
`experiments/*/`, and `report/figlib/style.check_colour_consistency()` asserts the sweep
figures use the same one. Change the palette and the committed task figures are stale
until this runs.

**Why this exists rather than `python -m experiments.human.human_mc.run`:** each task's
`run.py:main` calls `runner.run_matrix(...)` before `stats.run` / `plots.run`, so
invoking it re-runs the whole experiment. `plots.run(cfg)` needs only `cfg`, the frozen
`results.parquet` and the frozen `stats_*.parquet`, all of which are already on disk.
This module rebuilds each task's config exactly as its `run.py` does -- reusing that
module's own `build_config`, so the two cannot drift -- and calls `plots.run` alone.

Two config fields need care and are taken from the task's `run.py`, not guessed:

* `supercritical_span`, which `run.py` sets from
  `builder.connectome_supercritical_radii(...)`. That is an eigendecomposition of the
  connectome per condition -- seconds, no reservoir simulation.
* the sweep grid at N=1000, which was widened past the default [0, 4] (`sr_crit` rises
  with N). It is read back off the frozen `results.parquet` rather than reconstructed.

Mackey-Glass is included: `PREREG_MACKEY_GLASS.md` sections 1 to 3 are written and
committed, so `CONVENTIONS` working rule 6 no longer holds it back.

    python -m tools.replot_task_figures --list      # what would be written
    python -m tools.replot_task_figures             # write them
"""

import importlib
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.reservoir import blas  # noqa: F401,E402  (limit BLAS threads; import early)
from src.experiment import plots  # noqa: E402


def _frozen_sweep(cfg):
    """The spectral-radius grid actually present in the frozen results."""
    import pandas as pd
    sweep = sorted(pd.read_parquet(cfg.results_parquet).spectral_radius.unique())
    return [float(sr) for sr in sweep]


def _human_single_metric(task_module: str, scale: int):
    """human_mc / human_narma10: one metric, config built as run.py builds it."""
    from experiments.human import matrix_config
    from experiments.human.substrates import HumanSubstrateBuilder

    run = importlib.import_module(f"experiments.human.{task_module}.run")
    cfg = run.build_config()
    cfg.results_dir = cfg.results_dir / f"scale_{scale}"
    cfg.figures_dir = cfg.figures_dir / f"scale_{scale}"
    if scale != matrix_config.SCALE:
        cfg.spectral_radii = _frozen_sweep(cfg)
        cfg.supercritical_radii = [sr for sr in cfg.spectral_radii if sr >= 1.25]
    builder = HumanSubstrateBuilder(scale=scale)
    cfg.supercritical_span = builder.connectome_supercritical_radii(cfg.conditions)
    return [cfg]


def _human_lorenz(scale: int):
    """human_lorenz: one matrix run, two metrics, one figure set per metric."""
    from experiments.human import matrix_config
    from experiments.human.substrates import HumanSubstrateBuilder

    run = importlib.import_module("experiments.human.human_lorenz.run")
    builder = HumanSubstrateBuilder(scale=scale)
    span = builder.connectome_supercritical_radii(matrix_config.CONDITIONS)
    configs = []
    for metric in run.METRICS:
        cfg = run.build_config(metric, scale, None, span)
        if scale != matrix_config.SCALE:
            cfg.spectral_radii = _frozen_sweep(cfg)
            cfg.supercritical_radii = [sr for sr in cfg.spectral_radii if sr >= 1.25]
        configs.append(cfg)
    return configs


def _celegans_mackey_glass(horizon: int):
    """celegans_mackey_glass: results and figures are horizon-tagged by task_config."""
    from experiments.celegans import matrix_config
    from experiments.celegans.substrates import SubstrateBuilder

    run = importlib.import_module("experiments.celegans.celegans_mackey_glass.run")
    cfg = run.build_config(horizon)
    builder = SubstrateBuilder()
    cfg.supercritical_span = builder.connectome_supercritical_radii(
        matrix_config.CONDITIONS)
    return [cfg]


# Every target whose figures are drawn with _VARIANT_STYLE and whose frozen results
# are on disk. Each entry yields one or more configs (Lorenz yields two, one per metric).
TARGETS = [
    ("human_mc @ N=448", lambda: _human_single_metric("human_mc", 448)),
    ("human_mc @ N=1000", lambda: _human_single_metric("human_mc", 1000)),
    ("human_narma10 @ N=448", lambda: _human_single_metric("human_narma10", 448)),
    ("human_narma10 @ N=1000", lambda: _human_single_metric("human_narma10", 1000)),
    ("human_lorenz @ N=448", lambda: _human_lorenz(448)),
    ("human_lorenz @ N=1000", lambda: _human_lorenz(1000)),
    ("celegans_mackey_glass h=84", lambda: _celegans_mackey_glass(84)),
    ("celegans_mackey_glass h=300", lambda: _celegans_mackey_glass(300)),
]


def main(argv) -> int:
    listing = "--list" in argv
    failures, written = [], 0
    for label, build in TARGETS:
        try:
            configs = build()
        except Exception as exc:                      # noqa: BLE001
            print(f"  [SKIP] {label}: config build failed -- {exc}")
            failures.append(label)
            continue
        for cfg in configs:
            if not cfg.results_parquet.exists():
                print(f"  [SKIP] {label} ({cfg.metric}): no frozen results at "
                      f"{cfg.results_parquet}")
                failures.append(f"{label}/{cfg.metric}")
                continue
            if listing:
                print(f"  [would write] {label} ({cfg.metric}) -> {cfg.figures_dir}")
                continue
            print(f"  [replot] {label} ({cfg.metric})", flush=True)
            plots.run(cfg)
            written += 1
    if failures:
        print(f"\n{len(failures)} target(s) skipped: {', '.join(failures)}")
    print(f"\n{'listed' if listing else f'replotted {written} figure set(s)'}; "
          f"{len(failures)} skipped.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
