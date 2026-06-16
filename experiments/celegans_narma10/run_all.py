"""Orchestrator: run the matrix, then statistics, then figures.

    python experiments/celegans_narma10/run_all.py           # full pipeline
    python experiments/celegans_narma10/run_all.py --smoke    # tiny end-to-end check
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_experiment
import stats
import plots


def main(smoke: bool = False) -> None:
    if smoke:
        run_experiment.run(spectral_radii=[0.0, 0.95, 1.5], n_seeds=2)
    else:
        run_experiment.run()
    stats.main()
    plots.main()
    print("\nPipeline complete.")


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
