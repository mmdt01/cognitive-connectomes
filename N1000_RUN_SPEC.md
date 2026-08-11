# N=1000 run specification — **for review, not yet launched**

Derived from `TIER0_STATE_OF_PLAY.md`. Nothing here has been run. Numbers in §6 are
estimates and **must be validated by the timing probe (§7) before the full grid is
queued**.

---

## 1. The question this run answers

**Does the connectome's supercritical memory margin scale with N, or is it an N=448
accident?** At N=448 the margin is MC 12.28 vs ER 2.82 (α = 1e-6, σ ≥ 3.05), and
`d_eff` 204.9 vs 49.5 at the top of the matched overlap.

**It is not the ceiling question.** Peak MC is ~15 against N = 448, so MC was never
ceiling-limited. Peak `d_eff` *is* ceiling-limited and will be at any N — no
parcellation makes the peak comparison informative. **Read the decay region.**

---

## 2. Grid

| axis | value |
|---|---|
| task | **MC only** (`d_eff` reported alongside from the same states) |
| sign fraction | **`f = 0`** only |
| variants | connectome, connectome_weight_permuted, degree_rewire, erdos_renyi |
| seeds | 10 (0–9), standard convention |
| σ range | **[0, 10.4]** |
| σ points | **30**, non-uniform (§3) |

**Cells:** 4 × 10 × 30 = **1,200**.

### Why σ_max = 10.4

The comparison happens on `σ·bulk95`, and the connectome has the smallest `bulk95`
(0.2509 at N=1000), so it bounds the overlap.

| σ_max | connectome `σ·bulk95` | verdict |
|---|---|---|
| 6 | 1.505 | far short — misses even the peak |
| 8 | 2.007 | covers the peak with **zero margin**, no post-peak coverage |
| **10.4** | **2.609** | **matches the N=448 coverage (2.599)** |

At N=448 the matched `dD` peaks at `σ·bulk95` = 1.949 and then **turns over**. σ_max = 8
would place that peak at the very edge and make the turnover invisible — reproducing
exactly the censoring Task B was run to remove. σ_max = 10.4 gives the same post-peak
coverage the N=448 result now has.

---

## 3. σ spacing — do not use a uniform grid

The result lives supercritically, so a uniform nominal grid spends most of its points
where nothing happens. At N=1000 the connectome's `sr_crit` is **3.985**; below that
every variant is on the shared rising limb.

Proposed 30 points:

- **6 points** over σ ∈ [0, 3.0] — the shared rise, coarse (0.6 step). Needed only to
  establish the peak and the common limb.
- **18 points** over σ ∈ [3.2, 8.0] — the decay region, fine (~0.28 step). This is
  where the entire result lives.
- **6 points** over σ ∈ [8.4, 10.4] — the post-peak tail, medium (0.4 step).

In matched coordinates that puts ~24 of 30 points above `σ·bulk95` = 0.8 for the
connectome. **Include σ = 0 and the N=448 grid points that fall inside the range**, so
the two scales can be compared on shared nominal σ as well as on the matched axis.

---

## 4. Hyperparameters

| parameter | value | reason |
|---|---|---|
| `T` | **6000** | preserve `T_eff/N`: **5.50** at N=1000 vs **5.58** at N=448 (`T`=3000) |
| `warmup` | 500 | unchanged |
| `max_lag` | 50 | unchanged |
| ridge α (**MC and `d_eff`**) | see below | must be identical in both |
| `input_scaling` | 1.0 | frozen |
| `leak_rate` | 1.0 | frozen |
| `collect_states` | **False** for the run | do not persist states (44 MB/cell) |

### α — keep 1e-6, but reparameterise

`d_eff(α)` showed the supercritical ordering is flat across α from 1e-10 to 1e2, and
MC(α) showed the `d_eff`↔MC correspondence is +0.999 at every α. **So α does not need
changing to escape saturation** — the saturation is confined to the peak.

But α = 1e-6 is *absolute* and `trace(G)` scales with `T`, so doubling `T` halves the
effective regularisation. **Reparameterise as `α = λ · trace(G)/N` and pin λ to
reproduce the N=448 value at `T = 3000`.** Record both the λ and the realised absolute α
per cell.

**Implemented** in `criticality_matched/n1000.py` with **λ = 4.4845e-10**, pinned so the
median realised α over the supercritical region at N=448, `T` = 3000 equals the frozen
1e-6. Calibrated from the *persisted* Gram traces of the Task B sweep (`trace(G)` =
Σ `eig_gram`), so no re-run was needed. `trace(G)` varies only ~4× across the whole σ
sweep, so realised α stays within a factor of a few of 1e-6 everywhere (measured range
2.6e-7 to 1.1e-6).

Holding α identical in `d_eff` **and** MC requires **two evaluator passes per cell**:
α depends on `trace(G)`, which depends on the states, so pass 1 harvests the states (the
trajectory is independent of the ridge) and pass 2 re-solves the readout at the implied
α. This reuses the frozen MC evaluator rather than reimplementing the readout.

> **The same α must be used for MC and for `d_eff`.** They are only comparable when
> matched, and the +0.999 correspondence is what licenses reading one through the other.

---

## 5. Controls and pre-flight — all still required

1. **Re-run N=448 under the new `T` and α first.** Without it a null result at N=1000 is
   uninterpretable — you cannot tell whether the margin changed because of N or because
   of the protocol. **DONE — and it passed.** Under the new ridge rule at `T` = 3000 the
   supercritical MC margin is **4.40** against the frozen run's **4.35**; median per-cell
   change 0.32% (MC) and 0.70% (`d_eff`). The protocol change is neutral, so any shift at
   N=1000 is attributable to N. **The comparison baseline is therefore 4.40**; the
   pre-registered "does not scale" threshold of ratio < 3.0 stands as written.
2. **Nulls regenerate deterministically** and are assert-validated at construction;
   already confirmed at N=1000 (degree sequence 10/10, ER edge count 10/10, clustering
   10/10, modularity 10/10 at 10,784 edges / density 0.0216).
3. **`bulk95` at N=1000 already computed** (E0.4) — no eigendecomposition needed at run
   time; join it for the matched axis.
4. **Report `d_eff / N` with the ceiling drawn** on every memory figure.
5. **Overlap gate:** the new N=448 control run must reproduce the existing N=448 result
   at the shared σ under the old `T`/α before the new `T`/α numbers are trusted.

---

## 6. Compute and memory

### Threading — the important one

Set in the worker environment, **before numpy is imported**:

```
OMP_NUM_THREADS=1
MKL_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
```

The Gram eigendecomposition uses multithreaded BLAS by default; 128 workers each
spawning 128 threads will thrash. **Parallelism lives at the cell level.** Note the repo
caps BLAS at 2 threads via `src/reservoir/blas.py`, and `threadpool_limits` only
constrains libraries *already loaded* — hence the environment variables as well as the
in-process cap.

### Estimates — to be replaced by §7's measurements

> **Corrected — this was wrong by ~60×.** An earlier draft gave ~22 min per cell and
> ~440 core-hours. That was mis-scaled from the KB's *whole-matrix* Lorenz wall-clock
> (~90 min at N=1000, which is 12,180 evaluations on 128 cores) as though it were a
> per-cell figure. Recomputed from a measurement taken this session.

> **Superseded — the figures below were wrong, twice over.** They were built from a
> *bare evaluator* timing (0.313 s), which excludes the dense `eigvals` inside
> `build_from_adjacency` and the Gram eigendecomposition that every σ point also pays;
> and they predate the **two-pass** design that holding α identical in `d_eff` and MC
> requires, which doubles the evaluator cost again. Use the measured basis below.

**Measured basis (N=448 control, actually run).** 40 (variant, seed) cells × 21 σ × 2
passes = 1,680 evaluations in 400 s wall on 12 workers = **2.86 core-s per evaluation**,
i.e. **5.7 core-s per σ point**. Scaling the `N³` ridge solves (11.1×) and the doubled
`T`, N=1000 lands at roughly **31–63 core-s per σ point**:

| quantity | measured-basis estimate |
|---|---|
| 1,200 σ points × 2 passes | **10–21 core-hours** |
| wall clock, 128 workers (ada) | **5–10 min** |
| wall clock, 12 workers (laptop) | **1.7–3.5 h** |

The original figures below are kept only to show the size of the error.

MC at N=448, `T`=3000, measured **0.313 s per evaluation** (state capture included,
reservoir build excluded). Scaling to N=1000, `T`=6000: the state loop goes as `T·N²`
(**9.96×**) and the 50 per-lag ridge solves as `N³` (**11.12×**) — so ~**3.3 s**. An
independent basis using the KB's whole-matrix MC wall-clock (~2 min on 128 cores →
1.26 s/eval at N=448, which includes per-cell overheads) gives ~**14 s**.

| quantity | measured basis | overhead-inclusive basis |
|---|---|---|
| per cell | ~3.3 s | ~14 s |
| 1,200 cells | ~1.1 core-hours | ~4.7 core-hours |
| wall clock, 128 workers (ada) | **< 1 min** | **~2 min** |
| wall clock, 12 workers (laptop) | ~6 min | ~23 min |

> **Hardware caveat — the per-core rate is a *laptop* measurement.** The 0.313 s/eval
> above was timed on the development laptop (Intel Core Ultra 7 155U, WSL2, AVX2, single
> core boosting to ~4.8 GHz). **ada's per-core rate is not that**, and is plausibly
> **1.5–2× slower**: server parts run a lower all-core clock, and with 128 workers loaded
> the memory bandwidth per core is contended. The core-hour figures are therefore
> laptop-referenced and should be treated as a lower bound until §7 measures ada.
>
> | basis | core-hours | wall @128 |
> |---|---|---|
> | laptop rate | 1.1–4.7 | <1–2 min |
> | ×2 ada penalty | 2.2–9.4 | 1–4.5 min |
>
> **The conclusion survives either way: minutes, not hours.** A 2× hardware penalty on
> top of the wider basis is still under 5 minutes on 128 cores.

**The run is minutes, not hours.** The two bases bracket the truth and the probe
settles it. Even a 5× miss leaves it under 30 minutes on 128 cores.
| state matrix per worker | **44 MB** (5500 × 1000 float64, transient) |
| Gram + eigendecomposition workspace | ~24 MB (3 × 8 MB for a 1000×1000) |
| **total per worker** | **~68 MB** |
| peak RAM, 64 workers | **~4.4 GB** |
| peak RAM, 128 workers | **~8.7 GB** |

> **Corrected.** An earlier draft carried ~107 MB per worker and ~14 GB at 128 workers.
> That came from an estimate at `T` = 13392, before `T` = 6000 was settled, and was not
> recomputed when `T` changed. The state matrix is `5500 × 1000 × 8 B` = **44 MB**,
> consistent with §4. **128 workers is comfortable** at ~8.7 GB; there is no memory
> reason to drop to 64. Still confirm **ada's** actual RAM ceiling before setting the
> worker count. Note the workers are **fork**-based, so the inherited substrate, the
> cached null masks and numpy itself are shared copy-on-write and are *not* paid per
> worker — the ~68 MB is the genuine marginal cost of a worker, and ~8.7 GB is the
> marginal total at 128. Add the parent's footprint once, not 128 times.

---

## 7. Timing probe — run this **on ada**, before queueing the grid

> **Run the probe on the machine that will run the grid.** §6's bracket is
> laptop-referenced; measuring it again on the laptop would only re-measure the laptop
> and would leave the hardware assumption untested. The probe exists to replace a
> laptop extrapolation with an ada measurement.

**5 cells**, spanning the cost range, with the production `T`, α and threading, on ada:

| cell | σ | why |
|---|---|---|
| connectome, seed 0 | 0.0 | floor — no recurrence |
| connectome, seed 0 | 4.0 | just above `sr_crit` |
| connectome, seed 0 | 10.4 | top of range |
| erdos_renyi, seed 0 | 4.0 | null at the same σ |
| erdos_renyi, seed 0 | 10.4 | null at the top |

Record wall time, peak RSS and realised α per cell — **and record ada's core count and
per-core clock alongside them**, so the figure is reusable for costing later runs
instead of being another one-off. **Extrapolate to the full grid and compare against
§6's bracket (3.3–14 s per cell, laptop-referenced; expect ada to land at or above the
top of it).** If the measured figure lands inside
it, queue the grid. If per-cell time exceeds ~60 s — 4× the top of the bracket — stop
and re-derive before queueing rather than scaling the grid down; at these costs a
surprise that large means something is wrong (most likely BLAS threading, §6), not that
the grid is too big.

Given the corrected cost, **there is no reason to trim the grid.** If anything the σ
grid could be denser; 30 points is chosen for analysis clarity, not for budget.

---

## 8. Analysis plan (fixed in advance)

1. Reindex onto `σ·bulk95` using the N=1000 `bulk95` values, **per seed then aggregate**,
   no extrapolation, overlap clipped to common coverage.
2. Report `dD` peak, its location, whether it turns over, and the retained fraction —
   the same four numbers as N=448, directly comparable.
3. Report the **decay-region margin** (MC and `d_eff`, σ ≥ `sr_crit` = 3.985) — this is
   the actual question.
4. Report `d_eff/N` with the ceiling drawn, and the peak-height crossing table.
5. Compare the N=448 and N=1000 matched curves on one axis.

**Pre-register the prediction before running**, as for E0.2, in
`results/N1000_verdict.md`.

---

## 9. What this run does *not* settle

- The `f > 0` censoring (still σ = 6 at N=448) and therefore the memory/generation
  boundary crossing. Separate, cheaper run.
- Whether the peak comparison is meaningful — it is not, at any N.
- The Dale non-normality confound.
