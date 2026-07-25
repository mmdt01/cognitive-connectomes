"""Sign-composition x spectral-radius phase diagram (human N=448).

The headline phase-diagram experiment: vary the negative-weight fraction ``f``
(graded sign composition) against the spectral radius, and map where network
topology controls the manifold geometry that computation reads out. Two mirrored
panels -- memory (ridge effective rank ``d_eff``) and generative (trajectory
straightness / curvature). See ``PHASE_DIAGRAM_EXPERIMENT.md``.

Mirrors the ``manifold`` probe package: a fork-parallel capture driver
(``capture.py``) writes one tidy parquet of per-cell measurements, then
``analysis.py`` computes the order parameters / boundaries and ``plots.py`` renders
the figures. The one piece of new science code is the graded sign transform in
``src/analysis/sign_composition.py``; everything else reuses the reservoir builder,
the task evaluators' ``collect_states`` hook, and the manifold / spectral analysis
tiers.
"""
