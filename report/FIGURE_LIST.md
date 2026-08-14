# Master figure list

**Fixed in session 0. Hard cap 14.** No session creates a figure that is not here; if one
seems missing, report and stop. `W` marks the workshop subset (5pp, ~4 figures).

Status: `draft` = proposed here, to be confirmed or cut in session 0.

| id | ch | claim it carries | source | status | W |
|----|----|------------------|--------|--------|---|
| F1 | 4 (Act I) | The spectrum is one large real Perron eigenvalue separated from a bulk that is essentially the nulls' bulk | `w_spectra.parquet` `eig_w_real` | draft | W |
| F2 | 4 | The difference is a **gap**, not a bulk: absolute bulk near-identical (4.4% spread), gap ratio 3.08 vs 1.81-1.92, holds at both N | `w_spectra.parquet`, E0.4 | draft | W |
| F3 | 4 | `\|lambda_1\|` is an extreme-value statistic (tracks max sampled weight, Hill alpha ~2.3), so the nominal axis is anchored to one draw | E0.4 §5 | draft | |
| F4 | 5 (Act II) | The Perron mode carries the mean and is removed by time-centring (top-mode fluctuation variance ~0) | Probe 2 | draft | |
| F5 | 5 | Sign selects the basis: balanced -> W-eigenmodes, all-positive -> low-frequency graph harmonics | Probe 2 | draft | |
| F6 | 5 | PR misses readout-relevant structure: PR orders the ladder +0.11, `d_eff` +0.998 | Probe 3 | draft | |
| F7 | 6 (III-mem) | **The crossing**: connectome peaks lowest yet retains most; matched-axis `d_eff` decay by variant, ceiling drawn | E0.2, `phase_cells.parquet` | draft | W |
| F8 | 6 | The two axes give different answers: nominal vs `sigma·bulk95` side by side, same data | E0.2 §4.1 | draft | |
| F9 | 6 | The supercritical margin is scale-invariant: N=448 vs N=1000 matched curves, ratio 4.40 -> 4.42 | N=1000 run | draft | |
| F10 | 6 | Peak parity, not deficit: paired per-seed differences with CIs across the alpha grid | Task B | draft | |
| F11 | 6 | Rescue from Perron domination: `\|mean_state\|` 0.759 vs 0.949-0.989; bulk95 absorbs only 26% of the f=0 gap | E0.3 §3.7 | draft | |
| F12 | 6 (III-pred) | Curvature is **bimodal**: 98% of cells in two spikes, 0.56% between — the figure that licenses the switch framing | 38,280 Lorenz cells | draft | W |
| F13 | 6 | Generation read as VPT: +1.0 to +2.2 Lyapunov times from f~0.20, clearing the placement control; f=0 collapse-rate inset (ER 5/10 vs 0/10) | E0.3 | draft | |
| F14 | 6 | `sigma_eff` as locator not criterion: transition at 0.77-0.90, variant offsets ordered by gap, CV 0.209 vs 0.667 | E0.1 | draft | |
| F15 | 7 (Act IV) | Which Yeo networks load the Perron mode (minimal Act IV) | Perron eigenvector + Yeo partition | draft | |

**Over cap at 15 — session 0 must cut one.** F3 and F8 are the candidates: both serve
contribution 5 (the methodological critique) and could merge into a single two-panel
figure.

## Claim-to-primary-task mapping

Declared before any data is inspected, so that "there is always a task where it holds"
cannot be said.

| claim | primary | corroborating |
|---|---|---|
| memory capacity, ladder ordering, decay-rate advantage | **MC** | NARMA-10 |
| closed-loop generation, regime switch, resistance margin | **Lorenz** | Mackey-Glass |
| the two capacities are one axis read with opposite sign | **MC + Lorenz jointly** | MG (interior optimum, pre-registered) |
| readout dimensionality vs PR | **MC** | NARMA-10 |

NARMA-10 also carries the **bridge paragraph**: it sits between pure memory and pure
prediction, and one paragraph showing the trade-off varies continuously across
MC -> NARMA -> Lorenz strengthens Act III at almost no cost.

## Inline manifold measures for NARMA and MG

Gram spectra are persisted and give `d_eff` at any alpha forever. Curvature and PR
**cannot** be recovered afterwards, so decide here what is computed inline:

- [ ] `mean_curvature` on NARMA driven states
- [ ] `mean_curvature` on MG driven states  (**needed for the MG pre-registration test**)
- [ ] `participation_ratio` on both
- [ ] `mean_gain` / `sigma_eff` on both

Tick these in session 0. This is the one thing a re-run would be needed for.
