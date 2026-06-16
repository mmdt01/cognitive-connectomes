"""Experiment instances, grouped by connectome then task.

Each connectome (``celegans/``, ``drosophila/``, ...) holds its
connectome-specific substrate builder and shared matrix config; each task
subdir (``celegans_narma10/``, ``celegans_mackey_glass/``, ...) holds only its
task config, a thin run wiring, an intuition demo, and its outputs. The generic
runner/stats/plots live in ``src/experiment/``.
"""
