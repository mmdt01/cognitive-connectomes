"""CLI dispatch for E0.4 -- eigenspectra, ``bulk95`` and ``sr_crit``.

    python -m experiments.human.analysis.eigenspectrum --tables   [--scale N] [--jobs N]
    python -m experiments.human.analysis.eigenspectrum --bulk95-f [--scale N] [--jobs N]
                                                                  [--sign-mode edge[,dale]]
    python -m experiments.human.analysis.eigenspectrum --figures  [--scales 448,1000]
    python -m experiments.human.analysis.eigenspectrum --all      [--jobs N]

--tables:   per-seed eigendecomposition of every (condition, variant, seed) at one
            scale -> spectra_per_seed.parquet + bulk95_summary.{csv,md}. Runs the
            reproduction and headline gates.
--bulk95-f: bulk95 across the sign-fraction grid -> bulk95_vs_f.parquet + summary.
            Gated against the frozen phase_cells.parquet at N=448.
--figures:  the paper figures, read from the above (no recomputation).
--all:      --tables and --bulk95-f at every scale in common.SCALES, then --figures.

Modes may be combined. No reservoir simulation anywhere in this package; every
output carries a manifest with the config and the git commit that produced it.
"""

import sys

from experiments.human.analysis.eigenspectrum import common


def _list_flag(argv, name, default):
    raw = common.flag(argv, name, None, str)
    return [x.strip() for x in raw.split(",") if x.strip()] if raw else default


if __name__ == "__main__":
    argv = sys.argv
    jobs = common.flag(argv, "--jobs", 1, int)
    scale = common.flag(argv, "--scale", None, int)
    sign_modes = _list_flag(argv, "--sign-mode", None)
    scales = [int(s) for s in _list_flag(argv, "--scales", [])] or None

    modes = [m for m in ("--tables", "--bulk95-f", "--figures", "--summary", "--all")
             if m in argv]
    if not modes:
        modes = ["--all"]
    run_all = "--all" in modes

    from experiments.human.analysis.eigenspectrum import (
        tables, bulk95_f, figure1, summary)

    if run_all or "--tables" in modes:
        for s in (common.SCALES if run_all or scale is None else [scale]):
            print(f"\n{'=' * 70}\nE0.4 tables -- scale {s}\n{'=' * 70}")
            tables.run(scale=s, jobs=jobs)

    if run_all or "--bulk95-f" in modes:
        for s in (common.SCALES if run_all or scale is None else [scale]):
            print(f"\n{'=' * 70}\nE0.4 bulk95(f) -- scale {s}\n{'=' * 70}")
            bulk95_f.run(scale=s, jobs=jobs, sign_modes=sign_modes)

    if run_all or "--figures" in modes:
        print(f"\n{'=' * 70}\nE0.4 figures\n{'=' * 70}")
        figure1.run(scales=scales)

    if run_all or "--summary" in modes:
        print(f"\n{'=' * 70}\nE0.4 summary\n{'=' * 70}")
        summary.run(scales=scales)
