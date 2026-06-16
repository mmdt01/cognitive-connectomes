"""Generic, task- and connectome-agnostic experiment infrastructure.

The connectome x null-ladder x spectral-radius matrix, its statistics, and its
figures are identical across tasks (NARMA-10, Mackey-Glass, Lorenz, ...). They
are parameterised by an ``ExperimentConfig`` (assembled per experiment from a
connectome's shared matrix config and a task config) and a ``SubstrateBuilder``
(connectome-specific). Only the task evaluator and a handful of config values
change between experiments.
"""
