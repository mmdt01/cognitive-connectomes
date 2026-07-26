"""CLI dispatch for the sign-composition x spectral-radius phase diagram.

    python -m experiments.human.analysis.phase_diagram --capture [--scale N] [--jobs N]
        [--smoke] [--targeting stratified[,hub_first,periphery_first]]
        [--sign-mode edge[,dale]]
        [--tasks mc[,narma10,lorenz]] [--n-draws N] [--score degree|eigenvector]
    python -m experiments.human.analysis.phase_diagram --analyse [--scale N]
    python -m experiments.human.analysis.phase_diagram --plots   [--scale N]

--capture (default): run the grid, write results/scale_<N>/phase_cells.parquet.
--analyse: order parameters, boundaries, predictors, cross-panel, placement f*.
--plots: the phase-diagram figures.

Multiple modes may be combined (e.g. --capture --analyse --plots). --analyse and
--plots are imported lazily so capture works before they are implemented.
"""

import sys

from experiments.human.analysis.phase_diagram import common, capture


def _list_flag(argv, name, default):
    raw = common.flag(argv, name, None, str)
    return [x.strip() for x in raw.split(",") if x.strip()] if raw else default


if __name__ == "__main__":
    argv = sys.argv
    scale = common.flag(argv, "--scale", None, int)
    jobs = common.flag(argv, "--jobs", 1, int)
    smoke = "--smoke" in argv

    modes = [m for m in ("--capture", "--analyse", "--plots") if m in argv]
    if not modes:
        modes = ["--capture"]

    if "--capture" in modes:
        capture.run(
            smoke=smoke, jobs=jobs, scale=scale,
            targetings=_list_flag(argv, "--targeting", None),
            sign_modes=_list_flag(argv, "--sign-mode", None),
            tasks=_list_flag(argv, "--tasks", None),
            n_draws=common.flag(argv, "--n-draws", None, int),
            score_mode=common.flag(argv, "--score", None, str),
        )
    if "--analyse" in modes:
        from experiments.human.analysis.phase_diagram import analysis
        analysis.run(smoke=smoke, scale=scale)
    if "--plots" in modes:
        from experiments.human.analysis.phase_diagram import plots
        plots.run(smoke=smoke, scale=scale)
