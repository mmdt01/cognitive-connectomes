# The chain, in one page

*Structure to geometry to capacity in fixed recurrent networks. Not canonical for numbers;
`TIER0_STATE_OF_PLAY.md` is. This is the argument the thesis makes, written to be held in
the head while drafting.*

---

## The single mechanism

The gap does **one** thing. Memory and prediction are two consequences of that one thing,
so there is one chain and it forks at the end.

Every substrate here has a leading eigenvalue that is real, positive and separated from the
rest of the spectrum. Because macro connectome weights are non-negative, Perron-Frobenius
makes the leading eigenvector all-positive and hub-loaded: a **common mode** that drives
every unit in the same direction at once.

The hinge is counterintuitive. What matters is not how large the leading eigenvalue is but
**how far it sits above the bulk**, because that ratio decides whether the bulk follows it
up as the operating point rises. The substrate with much the largest Perron root turns out
to be the **least** dominated by it.

> **A large gap lets the leading mode be driven hard while the bulk stays put.** In the
> nulls the leading mode and the bulk are close together, so raising the gain drags
> everything into saturation together and the network synchronises. `|mean_state|` 0.759 for
> the connectome against 0.949 to 0.989 for every null, at sigma = 6.

That is the whole geometric consequence of structure. Everything below is about what the
surviving fluctuations are good for.

---

## Why this is a claim about geometry

Time-centre the states and the Perron mode vanishes: after centring the top eigenmode
carries 0.0001 of the remaining variance, **below** a random direction's 0.0023. The
decomposition is clean.

- **The Perron mode carries the mean.** One position, where the network sits.
- **The bulk carries the fluctuations.** A cloud around that position, spanning some number
  of directions, and the only thing a readout can act on.

When the common mode dominates, the network is pinned at a point and the cloud is crushed.
When it does not, the cloud stays wide. The measurable version of "wide" is where the
fluctuation directions sit relative to the ridge readout's noise floor: supercritically
**89.0%** of the connectome's directions stand more than a decade clear of it against
Erdos-Renyi's **11.4%**, with 73.2% of Erdos-Renyi's spectrum already at or below the floor.
That is what `d_eff` 412.9 against 74.8 counts, and it is why a variance-weighted count
cannot see the difference: the separating directions carry almost none of the variance.

---

## The fork: one fact, two demands

**Memory needs the cloud.** Recovering input from k steps ago means reading a combination of
state directions, so the number clearing the floor bounds how many delays survive. The
connectome retains **47%** of its peak where the nulls retain 28, 22 and 11%.

**But it does not buy a higher peak.** At the optimal operating point every cloud is wide
and the connectome is 2 to 6% behind: parity, not deficit. What the gap buys is a **slower
decay away from the peak**, which is the quantity that matters if the operating point is not
free to be tuned.

**Prediction needs the mean.** Running on its own output compounds errors, so what matters
is whether the dynamics stay on a smooth branch. Each unit is a tanh with an effective gain:
above +1 a stable fixed point, below −1 a period-2 orbit, **nothing stable between**.
Perron-Frobenius pins a non-negative matrix to the fixed-point branch, which is a guarantee
of smoothness, and smoothness is what closed-loop rollout needs.

**So the same domination that ruins memory protects generation.** One axis, read from
opposite ends.

---

## Why this is causal and not a story

Take the common mode away. Flipping edge signs breaks the Perron guarantee: the spectrum
becomes symmetric about zero and `|mean_state|` falls two orders of magnitude. Both
consequences follow at once, in opposite directions, as the account requires.

- **Memory rises for everyone.** The connectome's advantage closes from +9.01 to +1.07 not
  because it degrades but because the nulls gain roughly four times as much from a far lower
  start. Their clouds were crushed by domination; removing it releases them. The connectome
  had less to release because it was never crushed.
- **Generation becomes a switch.** The period-2 branch is now reachable, so capacity is
  gated by which dynamical regime the manifold is in rather than graded by how straight its
  trajectories are.

One intervention, two opposite effects, both stated in advance. That is what separates a
mechanism from a correlation.

---

## The chain in one line

**Weight placement → large spectral gap → the common mode is driven without the bulk
following → the fluctuation cloud survives above the readout floor → the wide cloud sustains
memory while the pinned mean sustains generation → the two trade against each other, and the
advantage is range rather than peak.**

---

## The takeaway

**The connectome is not organised for capacity. It is organised for not needing to be
tuned.**

This is a claim about what to measure as much as about brains. A brain does not find an
optimal gain and hold it; neuromodulation, arousal and plasticity move the operating point
continuously. If retained capacity across a range is the quantity that matters rather than
peak capacity at a tuned point, then peak-matched benchmarking measures the wrong thing, and
a substrate can lose the standard comparison precisely because it is built for the harder
problem.

---

## The honest seam, which is part of the contribution

Everything above about generation concerns the **counterfactual**, the substrate with signs
restored. At f = 0, which is what tractography produces, the geometry does not move at all
as capacity falls roughly tenfold: curvature sits flat at 0.26 across the whole sweep while
prediction degrades.

So **the memory half of the chain is established on the substrate the instrument produces,
and the generation half on the counterfactual in which the missing half of the biology is
restored.** What sets generation on the non-negative substrate is named as an open problem,
with the candidate explanations ruled out on the data and no further one offered.

Three things a reader must not take away, and saying so is part of the contribution: the
connectome is not a better reservoir; the unifying account is consistent with everything
measured but is not a derivation and has no out-of-sample test here; and it does not explain
generation at f = 0.
