# Act III (prediction arm) — geometry gates predictive capacity

**Session 4 of the §4b sweep.** Read `report/CONVENTIONS.md` first. Canonical results
live in `TIER0_STATE_OF_PLAY.md`; canonical claims in `ACTION_PLAN_JOURNAL_ROADMAP.md` §1.

---

## 1. Claims register

Every claim this chapter makes, each with a figure and a source. The chapter is written to
this register, not the other way round.

| # | claim (one sentence, as it will appear) | figure | TIER0 § | artifact |
|---|---|---|---|---|
| A3P.1 | | | | |
| A3P.2 | | | | |

**Claims deliberately NOT made here** (and why):

-

---

## 2. Reproduction gate

Run before any figure work. A failed reproduction is the finding and stops the act.

| quantity | TIER0 value | recomputed | agrees to | verdict |
|---|---|---|---|---|
| | | | | |

**Functions audited:** VPT definition and horizon, `mean_curvature`, closed-loop rollout, `sigma_eff`

**Findings:**

-

---

## 3. Figures

One block per figure ID from `FIGURE_LIST.md`. **Caption written before the figure.**

### F12 — <short name>

- **Claim carried:** A3P.x
- **Source:** <parquet path, columns, filter>
- **Panels:**
- **Caption (final wording):**

---

## 4. Section outline

Structure only, at the level of section headings and the argument each carries. Prose is
written by hand, not generated (see the roadmap §4b note on drafting).

1.
2.

---

## 5. Audit log and open issues

Anything that did not reproduce, any number that moved, any claim that had to be weakened,
and anything a later session needs to know.

-

---

## 6. Inherited specifications — two manifold-trajectory experiments

**Handed down from session 2 (17 Aug), roadmap §4d.** Written as specifications rather
than ideas, so this session can accept, reduce or reject each on stated grounds instead of
re-deriving it. **Neither is a sanctioned figure**: the cap is 15 and full, and the two
compete for the same slot.

> **Read this first — the decision rule.** **E2 resolves first.** If a cap slot remains
> after E2 is settled, E1 may take it; if not, **E1 is dropped and the reason is written
> here**. The ranking is deliberate and not a matter of taste: E2 produces evidence the
> thesis does not have, E1 illustrates a result it already carries in F12. If only one
> lands it should be E2. Both are bounded by the **20 Aug experiment freeze**, and both
> need the `FIGURE_LIST` decision **before** any capture (`CONVENTIONS` working rule 4).

### 6.1 E2 — closed-loop faithful geometry (first priority)

**The gap it fills.** Every state matrix in the repository is **teacher-forced**.
`readout_config.json` is explicit for Lorenz — the states are "the post-washout
TEACHER-FORCED driven states the readout is fit on, not the autonomous free-run". So
nothing in Probes 1 to 3, the phase diagram, or the criticality-matched sweep has ever
looked at the trajectory the reservoir produces **when it is driving itself**, which is
the regime the entire prediction arm is about. `climate_error` scores that trajectory's
statistics; no artifact shows its shape.

**Pre-stated claim, before any code.** *The connectome's free-run attractor retains the
true Lorenz climate to a higher `f` than the nulls do, and the collapse when it comes is
a change of shape rather than a drift of scale.* Falsifiable, and it is the geometric
reading of a number already on record. **"Interesting latent dynamics" is not a claim**
and must not become the framing.

**Capture.** Free-run rollout states from the closed-loop path in `src/tasks/lorenz.py`,
alongside the teacher-forced states already captured for the same cell, at matched
`(variant, f, sigma, seed)`. States are not persisted (`CONVENTIONS` working rule 5), so
this is a new capture; it is small, since the interesting cells are a handful either side
of each substrate's collapse, not a sweep.

**Analysis.** PCA on the time-centred free-run states; compare the generated attractor to
the true one in the same projection. Report against `climate_error`, which is the existing
scalar this visualises — the figure earns its place by showing *what* a given
`climate_error` looks like, not by introducing a rival metric.

**Four constraints that come with it.**

1. **Do not caption it as the computational subspace.** The top-3 PCs hold 96 to 99% of
   the fluctuation variance but are nearly identical across substrates (PCs-to-95% is 3
   for every rung; `d_eff` over the same rungs spans 75 to 413). The discriminating signal
   must come from the attractor's **shape**, not its dimensionality — state that in
   advance so a null result is legible rather than disappointing. Captioning a PCA
   trajectory as "the manifold the readout uses" contradicts F6.
2. **Rotation and sign.** Each substrate's PCs are its own coordinate system, so
   "connectome looks different from ER" can be a basis artifact. Project all substrates
   into one common basis, or compare basis-free shape statistics, and say which.
3. **Lorenz only.** MC is white-noise driven and its trajectory is a hairball; there is
   nothing to see and no claim to make there.
4. **Governance.** A new figure needs a cap slot, and `CONVENTIONS` working rule 4 permits
   a run only if a listed figure needs it — so the `FIGURE_LIST` decision comes **before**
   the capture, not after.

**If it is dropped**, say so here with the reason. A specification declined on stated
grounds is a result; one that quietly evaporates is not.

### 6.2 E1 — the two curvature regimes made visible (second priority, conditional)

**Build only if a cap slot remains once E2 is settled.** Otherwise drop it and record the
reason in §5.

**What it is.** A trajectory plot showing a smooth orbit against an antiparallel zig-zag —
what curvature's two spikes actually look like. It answers a gap this session inherits:
`report/act2_manifold.md` §5 item 15 records that Act II characterises only the *spatial*
axis of the manifold and hands the temporal one over as a boundary rather than a result,
so F12 currently introduces curvature to a reader with no run-up.

**Why session 4 owns a chapter-5 figure.** The claim is F12's — curvature is bimodal,
contribution 4 — so by the house convention the **act decides the module**: it belongs in
`figures/act3_prediction.py`, built here, while **printing in chapter 5** where the
intuition is needed. That is the F3 and F16 arrangement (F3 prints in chapter 3, session 1
builds it), and `FIGURE_LIST` must name the owner explicitly, as it does for those two.
This was originally scoped to Act II, which left it with no owner at all once session 2
closed; the correction is recorded in roadmap §4d.

**Where it must not be drawn from.** Not `f` = 0 on the all-positive substrate — the
condition every Act II figure uses — where curvature is **flat at 0.26 rad across the
whole σ sweep** and there is nothing to see. It needs the **signed or gaussian** columns
of the Probe 1 capture, which do transition, or `f` > 0 from the phase diagram.

**Two constraints inherited from the E2 work-up.**

1. **It shows a regime, not a capacity.** The top-3 PCs are nearly substrate-invariant
   (PCs-to-95% is 2 on MC and 3 on Lorenz for every rung, while `d_eff` spans 75 to 413),
   so this figure may not be captioned as the subspace the readout computes in — that
   contradicts F6, Act II's own contribution.
2. **It is an illustration of an existing claim, not a new one.** If it cannot be scoped
   to the *manifold* reading rather than the VPT one, it duplicates F12 and should not be
   built at all.
