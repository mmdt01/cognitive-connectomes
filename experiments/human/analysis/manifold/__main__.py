"""CLI dispatch for the human manifold-geometry probes.

    python -m experiments.human.analysis.manifold --probe {1,2,3} [--scale N] [--jobs N] [--smoke] [--sr-max V]

--probe 1 (default): dimensionality + shape (+ validation gate).
--probe 2: structural-mode alignment.
--probe 3: geometry -> performance link (reads Probe 1's parquet; no reservoir runs).
"""

import sys

from experiments.human.analysis.manifold import common, probe1, probe2, probe3

if __name__ == "__main__":
    probe = common.flag(sys.argv, "--probe", 1, int)
    opts = dict(smoke="--smoke" in sys.argv,
                jobs=common.flag(sys.argv, "--jobs", 1, int),
                scale=common.flag(sys.argv, "--scale", None, int))
    if probe == 2:
        probe2.run(**opts)
    elif probe == 3:
        probe3.run(**opts)
    else:
        probe1.run(**opts, sr_max=common.flag(sys.argv, "--sr-max", None, float))
