"""Constants shared across more than one act's figures.

Only genuinely cross-act values live here. Act-local constants stay in the act
module that uses them -- `OVERLAP_TOP` in `act3_memory`, `CURVATURE_GAP` and
`COLLAPSE_BIT` in `act3_prediction` -- so a reader of one act sees its own
thresholds rather than a shared bag of numbers.
"""

N_NODES = 448
