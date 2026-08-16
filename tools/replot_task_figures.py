"""Re-render the committed `_VARIANT_STYLE` figures from frozen results. No simulation.

Needed whenever the shared variant palette moves: `src/experiment/plots._VARIANT_STYLE`
is the colour source for every `*_vs_spectral_radius.png` / `*_factorial.png` under
`experiments/*/` **and for six manifold-probe figures**, and
`report/figlib/style.check_colour_consistency()` asserts the sweep figures use the same
one. Change the palette and those committed figures are stale until this runs.

**Nothing here may write a `.parquet`.** Every frozen artifact under `experiments/` is
fingerprinted (mtime + size) before the run and re-checked after; a single byte moving
raises. That guard is not paranoia -- see the probe section below, where the obvious
entry point does exactly that.

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

**The manifold probes, and why their `run*` entry points are NOT used.** Six committed
figures are drawn with `_VARIANT_STYLE`: probe1's `manifold_{pr,mean_curvature,
spectral_entropy}_vs_sr.png` and probe3's `probe3_deff_{vs_mc,vs_sr,two_axis}.png`. The
tempting call is `probe3.run_deff()`, whose docstring says "No reservoir runs" -- true of
compute, but it **rewrites `probe3_deff.parquet`**, which is the frozen source F6 reads
and which `TIER0` §3.12's numbers were promoted from. `probe3.run()` likewise rewrites
`manifold_geometry_performance.parquet` and `manifold_gap_tracking.parquet`. Refreshing a
palette must not regenerate a frozen artifact (`CONVENTIONS` working rule 1), so this
module reads the frozen parquets and calls the plotting functions directly. probe3's are
private (`_plot_*`); that is deliberate and is the reason.

None of the six are thesis figures -- `report/FIGURE_LIST.md` is canonical for those, and
Act II's chapter figures F4 to F6 render through `report/figlib` on the current palette.
These are analysis-time artifacts, tracked so probe results stay inspectable, and they
are refreshed so the repo does not carry two palettes.

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
import pandas as pd  # noqa: E402  (after `blas`, which must precede the numpy import)
from src.experiment import plots  # noqa: E402


# ---------------------------------------------------------------------------
# The guard: this module renders figures and must never touch a frozen artifact
# ---------------------------------------------------------------------------
def _parquet_fingerprint() -> dict:
    """(mtime_ns, size) for every frozen parquet under experiments/."""
    return {str(p): (p.stat().st_mtime_ns, p.stat().st_size)
            for p in sorted((_ROOT / "experiments").rglob("*.parquet"))}


def _assert_frozen(before: dict) -> int:
    after = _parquet_fingerprint()
    changed = sorted({*before, *after}
                     - {k for k in before if before.get(k) == after.get(k)})
    if changed:
        raise RuntimeError(
            "this tool wrote or removed a frozen artifact, which it must never do:\n  "
            + "\n  ".join(str(Path(c).relative_to(_ROOT)) for c in changed)
            + "\nA `run*` entry point was probably called where a plotting function was "
              "meant; see the module docstring.")
    return len(after)


def _frozen_sweep(cfg):
    """The spectral-radius grid actually present in the frozen results."""
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


# ---------------------------------------------------------------------------
# Manifold probes -- plotting functions only, never the `run*` entry points
# ---------------------------------------------------------------------------
def _probe1_figures(scale: int) -> list:
    """probe1's three `_VARIANT_STYLE` figures from the frozen manifold_metrics.parquet.

    `write_figures` is the same function `probe1.run` calls, and it receives the same
    frame: `run` writes `df` to manifold_metrics.parquet and then passes `df` straight
    on, so reading that parquet back reproduces its input exactly. `supercrit` is
    rebuilt the way `run` does -- an eigendecomposition of the connectome per condition,
    seconds, no reservoir simulation.
    """
    from experiments.human import matrix_config
    from experiments.human.analysis.manifold import common as manifold_common, probe1
    from experiments.human.substrates import HumanSubstrateBuilder

    results_dir, figures_dir = manifold_common.scale_dirs(scale)
    frame = pd.read_parquet(results_dir / "manifold_metrics.parquet")
    supercritical = (HumanSubstrateBuilder(scale=scale)
                     .connectome_supercritical_radii(matrix_config.CONDITIONS))
    probe1.write_figures(frame, figures_dir, supercritical)
    return [figures_dir / f"manifold_{metric}_vs_sr.png"
            for metric in probe1._METRIC_FIGURES]


def _probe3_figures(scale: int) -> list:
    """probe3's three `_VARIANT_STYLE` figures from the frozen probe3_deff.parquet.

    Deliberately calls the private `_plot_*` helpers rather than `run_deff`, which
    would rewrite probe3_deff.parquet -- the frozen source F6 reads. See the module
    docstring; the fingerprint guard in `main` is what enforces it.
    """
    from experiments.human.analysis.manifold import common as manifold_common, probe3

    results_dir, figures_dir = manifold_common.scale_dirs(scale)
    deff = pd.read_parquet(results_dir / "probe3_deff.parquet")
    figures_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for plot, name in ((probe3._plot_deff_vs_mc, "probe3_deff_vs_mc"),
                       (probe3._plot_deff_vs_sr, "probe3_deff_vs_sr"),
                       (probe3._plot_two_axis, "probe3_deff_two_axis")):
        path = figures_dir / f"{name}.png"
        plot(deff, path)
        print(f"Saved {path}")     # probe1's write_figures prints its own; match it
        written.append(path)
    return written


PROBE_TARGETS = [
    ("probe1 manifold metrics @ N=448", lambda: _probe1_figures(448)),
    ("probe3 d_eff @ N=448", lambda: _probe3_figures(448)),
]


def main(argv) -> int:
    listing = "--list" in argv
    frozen_before = _parquet_fingerprint()
    failures, written, probe_figures = [], 0, 0
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

    for label, build in PROBE_TARGETS:
        if listing:
            print(f"  [would write] {label} -> probe plotting functions "
                  "(never run_deff/run: those rewrite frozen parquets)")
            continue
        try:
            print(f"  [replot] {label}", flush=True)
            # The builders print their own "Saved" lines, so only count here.
            probe_figures += len(build())
        except Exception as exc:                          # noqa: BLE001
            print(f"  [SKIP] {label}: {exc}")
            failures.append(label)

    n_frozen = _assert_frozen(frozen_before)
    if failures:
        print(f"\n{len(failures)} target(s) skipped: {', '.join(failures)}")
    print(f"\n{'listed' if listing else f'replotted {written} task figure set(s) '
                                        f'and {probe_figures} probe figures'}; "
          f"{len(failures)} skipped.")
    print(f"{n_frozen} frozen parquets under experiments/ unchanged.  [OK]")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
