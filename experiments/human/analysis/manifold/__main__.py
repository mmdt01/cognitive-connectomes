"""CLI dispatch for the human manifold-geometry probes.

    python -m experiments.human.analysis.manifold --probe {1,2,3} [--scale N] [--jobs N] [--smoke] [--sr-max V]
    python -m experiments.human.analysis.manifold --spectra [--scale N] [--jobs N] [--smoke]

--probe 1 (default): dimensionality + shape (+ validation gate).
--probe 2: structural-mode alignment.
--probe 3: geometry -> performance link (reads Probe 1's parquet; no reservoir runs).
--spectra: raw spectra behind the Probe 1 to 3 summary metrics (readout_config.json,
    covariance_spectra / w_spectra / saturation_diagnostics parquets); a follow-up
    extraction, not a new probe.
"""

import sys

from experiments.human.analysis.manifold import common, probe1, probe2, probe3, spectra

if __name__ == "__main__":
    opts = dict(smoke="--smoke" in sys.argv,
                jobs=common.flag(sys.argv, "--jobs", 1, int),
                scale=common.flag(sys.argv, "--scale", None, int))
    if "--spectra" in sys.argv:
        spectra.run(**opts)
    else:
        probe = common.flag(sys.argv, "--probe", 1, int)
        if probe == 2:
            probe2.run(**opts)
        elif probe == 3:
            probe3.run(**opts)
        else:
            probe1.run(**opts, sr_max=common.flag(sys.argv, "--sr-max", None, float))
