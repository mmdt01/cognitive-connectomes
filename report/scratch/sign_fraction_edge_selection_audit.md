# How the edges to flip are selected — read-only code audit

**Date:** 30 August 2026 · **Scope:** the sign fraction `f` of chapter 6 §6.4 · **Method:** source
reading only. No experiment, sweep, evaluator, builder or verdict was run; no repository file was
written except this one. All 23 files read were SHA-256 hashed before and after and are unchanged.

**Why this exists.** §6.4 introduces `f` as an intervention — a fraction `f` of weights made
negative with magnitudes and topology unchanged — and the chapter needs a footnote saying *how the
edges to flip are chosen*. No document in `report/` describes it: not TIER0, not the fact sheets,
not the act files. The answer had to come from the code, and this records it as implemented.

---

## 1. Which implementation

Three functions in the repo turn a non-negative matrix into a signed one. **Only the first is
§6.4's `f`.**

| # | Location | What it does | Is it §6.4's `f`? |
|---|---|---|---|
| 1 | `src/analysis/sign_composition.py:138-173` `sign_fraction_matrix` (edge, primary); `:175-213` `sign_fraction_matrix_dale` (node) | graded `f`-fraction sign flip, `stratified` / `hub_first` / `periphery_first` targeting | **yes** (the `edge` + `stratified` arm) |
| 2 | `experiments/human/substrates.py:165-178`; `src/reservoir/weights.py:184-201` (`symmetric_empirical_randsign`) | the `human_empirical_signed` **condition**: `rng.choice([-1.0, 1.0], size=n_edges)`, i.i.d. per edge | no — no `f` parameter, fixed at balanced, no strata |
| 3 | `src/connectomes/neurotransmitters.py` | *C. elegans* per-neuron Dale signs from a curated neurotransmitter table | no — empirical assignment, not a fraction |

They do **not** agree. #2 is precisely the uniform i.i.d. scheme that #1's design note describes as
the rejected naive design; it is a separate ladder condition, not a point on the `f` sweep.

**Evidence that #1 produced `criticality_matched/results/`.** `extend_f.py` states it "Reuses
`phase_diagram.capture.capture_cell` unchanged, with only the sigma sweep overridden", and its
`run()` passes `pd_capture.capture_cell` to the cell harness; `capture_cell` calls
`sign_composition.sign_fraction_matrix` at `phase_diagram/capture.py:76`. `manifest_item2.json` and
`manifest_item2_nulls.json` (naming `item2_f_extension_scale_448.parquet` and
`item3_f_extension_nulls_scale_448.parquet`) record `"sign_mode": "edge"`,
`"targeting": "stratified"`, `f_grid` 0 → 0.50 step 0.05, `n_seeds: 10`, `n_draws: 3`, git commit
`d008c5d5`. `manifest_e03_frontier.json` records the same for the four-variant frontier, which is a
reanalysis of those two parquets. `jacobian.py:91-95` and `free_run.py:145-150` independently
reconstruct the identical call and RNG key.

*Caveat:* the parquets themselves were not opened; this rests on the manifests, the code and the
recorded git provenance, not on reading the `targeting` column.

---

## 2. The procedure, point by point

### S1 — Selection unit: **edges**

Individual non-zero upper-triangle entries `i < j`, treated as undirected edges.

```python
# sign_composition.py:82-86  (edge_importance)
rows, cols = np.triu_indices(W.shape[0], k=1)
present = W[rows, cols] != 0.0
rows, cols = rows[present], cols[present]

# sign_composition.py:169-171  (the flip)
signs = np.where(flip, -1.0, 1.0)
out[rows, cols] = W[rows, cols] * signs
out[cols, rows] = W[cols, rows] * signs      # mirror -> stays symmetric
```

One selected edge flips both `(i,j)` and `(j,i)`. The `dale` arm — not §6.4's headline — selects
nodes instead and negates whole outgoing columns.

### S2 — Stratified, not uniform

Edges are ranked and partitioned first; the uniform draw happens only *within* a stratum. There is
no uniform-over-all-non-zeros option anywhere: `TARGETING_MODES = ("stratified", "hub_first",
"periphery_first")` and `_select_flips` raises `ValueError` on anything else.

### S3 — Stratum definition: deciles of an endpoint-degree **product**

```python
# sign_composition.py:123-124
ranks = np.argsort(np.argsort(escore))
stratum = np.minimum((ranks * n_strata) // n, n_strata - 1)
```

- The quantity is the **product** of the two endpoints' node scores (`escore =
  node_score[rows] * node_score[cols]`) — not sum, min or max.
- The node score is **binary, unweighted degree, not strength**: `sign_composition.py:66-68`,
  `A = np.abs(W)`, diagonal zeroed on a copy, then `(A > 0.0).sum(axis=1)`. Magnitudes are
  discarded. The substrate is symmetric, so source- and target-degree are the same quantity.
- An `eigenvector` score exists as a robustness alternative (writes a separate
  `phase_cells_eigenvector.parquet`); `SCORE_MODE = "degree"` is the headline.
- **10 strata** (`N_STRATA = 10`, `phase_diagram/common.py:52`).
- Boundaries are **rank-based equal-count bins computed per matrix** — quantiles of that matrix's
  own edge-score distribution, not fixed constants. `n` is not divisible by 10, so strata are
  near-equal, not exactly equal.
- **Tie caveat.** `np.argsort` defaults to quicksort, which is not stable, and `escore` is heavily
  tied. `eigenspectrum/bulk95_f.py:19-26` records the measured N=448 numbers: *"5323 edges but only
  695 distinct scores at N=448, largest tie group 42. A different tie order moves ~40 edges between
  strata, and because `rng.choice` is then drawn per stratum the whole downstream selection
  diverges."*

### S4 — Allocation: proportional, with banker's rounding

```python
# sign_composition.py:127-129
k = int(round(f * idx.size))
if k > 0:
    flip[rng.choice(idx, size=k, replace=False)] = True
```

- The realised fraction **is equal within every stratum**, up to rounding.
- The realised **global** `f` is **not exactly `f`, and not `f` in expectation either** — it is the
  deterministic `Σ_s round(f·n_s) / n`, fixed once matrix and strata are fixed. Recomputed by
  `negative_fraction(W)` and stored per row as `neg_frac`.
- Rounding is `int(round(...))` on a Python float, i.e. **half-to-even**, and it bites at the
  balanced end: stratum size 45 at `f = 0.5` gives `round(22.5) = 22`, not 23.
- A stratum with `k = 0` contributes nothing; with small strata and small `f`, every stratum can
  round to 0, giving realised `f = 0` at a nominally non-zero `f`.

### S5 — Seeding: deterministic, and independent across variants and across `f`

```python
# phase_diagram/capture.py:60-68
seed_key = [
    int(seed), int(f_idx), int(draw),
    common.TARGETING_CODE[targeting], common.VARIANT_CODE[variant],
]
if sign_mode == "dale":
    seed_key.append(common.SIGN_MODE_CODE["dale"])
if state["score_mode"] != common.SCORE_MODE:
    seed_key.append(common.SCORE_CODE[state["score_mode"]])
flip_rng = np.random.default_rng(seed_key)
```

- **Separate stream from the network draw.** The substrate comes from
  `builder.weighted(condition, variant, seed)`, seeded on `seed` alone; the flip generator's entropy
  is `seed` *plus four more entries*. Same integer, different streams.
- **The four ladder variants get INDEPENDENT draws**, not a shared pattern — `VARIANT_CODE` is in
  the key (`connectome` 0, `degree_rewire` 1, `erdos_renyi` 2, `connectome_weight_permuted` 3).
  This includes `connectome` vs `connectome_weight_permuted`, which share topology exactly and
  could in principle have shared a pattern. They do not.
- **`f = 0.10` is NOT a superset of `f = 0.05`.** `f_idx` is in the key, so each `f` is an
  independent draw. Not nested.
- **Not keyed on task or spectral radius.** MC and Lorenz cells at the same
  `(seed, f_idx, draw, targeting, variant)` get the identical matrix, and the flip is applied to
  the base before rescaling, so it is fixed across the whole σ sweep.
- Salts keep the `edge` + `degree` headline stream exactly as committed; `dale` and `eigenvector`
  get independent streams.
- **Portability.** Because of the S3 tie-order issue the pattern is not reproducible across
  machines. TIER0 §6.4 records this and its 12 Aug 2026 refinement: re-running on ada, the
  originating machine, reproduced all 19,200 shared `f > 0` cells exactly.

### S6 — What is preserved

- **Magnitudes: exactly.** Multiplication by `±1.0` only.
- **Sparsity pattern: exactly.** Only entries with `W[rows,cols] != 0.0` are candidates, so a
  structural zero can never become non-zero and a present edge can never become zero.
- **Diagonal: never touched.** The transform works on `triu(k=1)`; `out = W.copy()` carries the
  diagonal through. `node_importance` zeroes a diagonal only on its own `np.abs()` copy, for
  scoring.
- **Symmetry: enforced on input** (raises unless `np.allclose(W, W.T, atol=1e-9)`) **and preserved
  on output** by mirroring.
- Non-negativity is validated **off-diagonal only** — the check runs on `off`, a copy with the
  diagonal zeroed, so a negative diagonal would pass the guard. Not a live concern for this
  substrate (zero diagonal); noted because it is what the code does.
- The `dale` arm deliberately breaks symmetry; irrelevant to the `edge` arm §6.4 uses.

### S7 — `f = 0` is the identity

```python
# sign_composition.py:160-161
if f <= 0.0:
    return W.copy()
```

The early return fires before the RNG is consumed, for every targeting mode and every draw. Two
corroborations: `validate_f0` (`phase_diagram/capture.py:145-197`) hard-asserts that `f = 0` rows
reproduce the committed `human_empirical` runs (median relative difference < 1e-5, zero gross); and
`report/act3b_prediction.md:90-94` records the consequence — *"At `f` = 0 the sign transform is the
identity, so the draws are literally identical — checked here, and 100% of (variant, σ, seed)
groups return the same `mean_curvature` and the same `vpt` across all three draws."*

### S8 — The recorded reason, and where it is

**One place: `PHASE_DIAGRAM_EXPERIMENT.md` §3, lines 62-72** — an untracked design note at the repo
root, *not* in `report/`:

> "A naive design would flip `f * nnz` edges chosen uniformly at random, but that is confounded: it
> lets *where* the negative weights land vary with the luck of the draw, and where they land matters
> enormously. The mechanism is spectral — the common mode is the Perron eigenvector, and the leading
> eigenvalue of a non-negative graph is dominated by high-degree / rich-club nodes — so flipping an
> edge incident on a hub perturbs the Perron structure far more than flipping a peripheral edge.
> **Under uniform flipping, the *effective* spectral perturbation at a fixed `f` would depend on hub
> coverage, injecting uncontrolled noise into exactly the axis whose spectral meaning the phase
> diagram is trying to read.** The design below removes that confound as the primary, and then
> promotes placement to a deliberate secondary axis."

That is an explicit claim that the scheme removes a source of uncontrolled variability relative to
uniform selection — argued from the mechanism, **stated as design rationale, not as a measured
result**. Restated briefly in the module docstring (`sign_composition.py:20-30`: *"Placement
matters, so it is controlled"*; *"`f` means 'how much sign, holding where fixed'"*), in the
self-test comment at line 291 (*"the confound fix"*), and in commit `667e9a7`.

**No file under `report/` describes it.** TIER0's only mention of `_select_flips` is §6.4, which is
about `np.argsort` tie-order portability, not about how edges are selected.

### S9 — Never tested against uniform

**No artifact, test, notebook or results file compares stratified against uniform selection.** It
cannot: no uniform mode is implemented. What exists instead:

- **A placement study** — stratified vs `hub_first` vs `periphery_first`
  (`phase_diagram/results/scale_448/phase_eigcheck_summary.md`, `plots.py:420-433`). That contrasts
  placement-neutral with *deliberately targeted* selection, not with uniform. For the record, its
  headline ordering `hub < strat < peri` fails on the `edge` arm at both scores and holds only on
  `dale`.
- **A synthetic self-test only** (`sign_composition.py:288-296`), asserting the stratified
  flipped-set mean score stays within 15% of the overall mean at `f` = 0.1, 0.25, 0.5 — reachable
  only via `python -m src.analysis.sign_composition`. `tests/` holds only `test_smoke.py`, which
  does not touch this module.
- **One descriptive measurement of the selection-only variance component**
  (`report/act3b_prediction.md:88-94`): holding seed fixed and varying only the flip pattern, all
  three draws are identical at `f = 0` (100% of groups); at `f = 0.25` curvature differs across
  draws in 96.6% of groups while `vpt` is still identical in 45.1%. It isolates flip-selection
  variation from network draw but benchmarks it against nothing. Downstream, draws are always
  averaged within seed and the seed is the unit (`manifest_e03_frontier.json`:
  `"unit": "seed (draws averaged within seed)"`).

---

## 3. Synthetic-input observations

`sign_composition.py` imports only numpy, performs no I/O, and its self-test sits behind
`if __name__ == "__main__"`, so importing it is inert. The table below is from a matrix constructed
**in memory** (N=120, 448 upper-triangle edges, Pareto-driven degree spread). **No connectome or
repository artifact was loaded. These are not repository values.**

| `f` | realised neg. fraction | identity? | magnitudes | sparsity | symmetric | diagonal | same seed → same result |
|---|---|---|---|---|---|---|---|
| 0.00 | 0.000000 (0/448) | **yes** | preserved | preserved | yes | unchanged | yes |
| 0.05 | 0.044643 (20/448) | no | preserved | preserved | yes | unchanged | yes |
| 0.20 | 0.200893 (90/448) | no | preserved | preserved | yes | unchanged | yes |
| 0.50 | 0.491071 (220/448) | no | preserved | preserved | yes | unchanged | yes |

Per-stratum realised fractions at `f = 0.5`: `0.4889 ×8`, `0.5000 ×2` — the banker's-rounding effect
of S4. Edge scores were tied on the synthetic matrix too: 448 edges, 148 distinct scores, largest
tie group 11. Same-seed calls are bit-identical; different seeds at the same `f` differ; and with
the *same* generator seed the `f = 0.10` selection shares only 1 of 20 edges with `f = 0.05` — not
nested.

---

## 4. The procedure in plain language

Each undirected edge of the all-positive base matrix — one non-zero upper-triangle entry `i < j` —
is given an importance score equal to the product of its two endpoints' **binary, unweighted
degrees** computed once on that variant's fixed base topology, and the edges are rank-ordered by
that score and cut into ten near-equal-count strata (deciles). Within each stratum,
`round(f × stratum_size)` edges are drawn uniformly without replacement and have their sign flipped,
so the flipped set mirrors the hub-to-periphery composition of the graph at every `f`; there is no
uniform-over-all-edges option in the code. Flipping negates the entry and its mirror, so magnitudes,
the sparsity pattern, the diagonal and the symmetry of the matrix are all left exactly as they were
and only signs change; the realised negative fraction is therefore not exactly `f` but
`Σ_s round(f·n_s)/n`, a deterministic quantity recorded per cell as `neg_frac` (Python's round is
half-to-even, so `f = 0.5` typically realises just below 0.5). The draw is seeded by
`np.random.default_rng([seed, f_index, draw, targeting_code, variant_code])`, a stream distinct from
the one that generates the network, which means each of the four ladder variants receives an
**independent** selection, each value of `f` receives an **independent** selection rather than a
nested one, and the pattern is held fixed across the whole spectral-radius sweep and shared between
the MC and Lorenz cells of the same seed. At `f = 0` the function returns the input unchanged before
consuming any randomness, so the three draws per seed are exact duplicates there. One caveat is
load-bearing: the ranking uses an unstable sort over a heavily tied score, so stratum membership at
tie boundaries — and hence the whole selection — is reproducible on the machine that produced a
given capture but not across machines.

---

## Appendix — files read, SHA-256 (identical before and after)

```
9161bc374819c8287d9ac9c2c4513cc9933801f95354bc37cf66b18241702477  src/analysis/sign_composition.py
a03c99e1f563cff5f3d3ad88fab8cd653cad95ebddeabc6527ca8aa27a8f9682  src/reservoir/weights.py
a23dd7e58f429b53f26db9e96a1ad3b73ca6f918cd3ef7b641a97012cdf202a1  src/connectomes/neurotransmitters.py
2512840f07f0d11c8cbdf36a717c1e0695169418498d92a755d7a516d8de9f2f  experiments/human/substrates.py
95908cd4d67af6e0247a1e9425fc720390d235a6c15bd18128666e11435367d2  experiments/human/matrix_config.py
46741bc804edd67034b25a58f509dd8b777cb956130cf82250924f0a1943a726  experiments/human/analysis/realizations.py
dd66cd07281faed8b64c39f6536377bb85428dd4ac0d457ff15a186d14466737  experiments/celegans/analysis/realizations.py
441034f26fe78f8fe8e405313dd356ad5e0cb2467f339199fe96a0a73d9a0899  experiments/human/analysis/phase_diagram/capture.py
d07c3fa094e83f11c954dcec8db8837933891f3affa370c5da5a2b79f829fb52  experiments/human/analysis/phase_diagram/common.py
db9fdfb55e98535d471d430f99936626923c9ac1273002afeac3e6584f33785a  experiments/human/analysis/eigenspectrum/bulk95_f.py
5439eba4444b9f7049f29ef8b49169dc77b34ed16a889e77a8fcd6a81a61af69  experiments/human/analysis/criticality_matched/common.py
842bd4a48d7935471670a688431e3363ffd391c9988025417d0cd66a44300f6f  experiments/human/analysis/criticality_matched/extend_f.py
c31f881ea6505ab02a39a24a1b4a7d939a6fa23c086ca59b5907b0f9fe071c65  experiments/human/analysis/criticality_matched/jacobian.py
5580003fb3f0b0b5166bdec3f740ed08f2ed9f3699650a8995d22ba8d624ca25  experiments/human/analysis/criticality_matched/free_run.py
488fb3137fac5b13d5a0d1939021f3fc31c9f3f6eda322eba0657ed7df630c83  .../results/manifest_item2.json
b750beaaf81896c75603781b77e16adb2071d672e8521f80b24d28d24dd4200a  .../results/manifest_item2_nulls.json
7d115101e04dd3263929b49c735b4b9273adcba3df6f1eab41cd0b5edb5889b6  .../results/manifest_e03_frontier.json
559c6d16786fd95a5828b269436aa8ba809fc3d2be3f558a857600218ea4c4e2  .../results/manifest_free_run_scale_448.json
7c5b1141e9ed3d44c6f0f0487047e442b8ee6e44c77d71db90e7465c29cda571  .../results/manifest_taskB.json
19fdbe13960a0ba823d577b93ef86c3c1b4510b675540ddd91f52a2dfeaaaa0b  .../phase_diagram/results/scale_448/phase_eigcheck_summary.md
32a2acc418e05169f185f2352370eb3befcf3e115283a19013b0bbf88afcc612  report/act3b_prediction.md
5888c5c29d2e9db54feaa7bd0e68373c4bc46079e1df7b13c668e12ba46b3514  TIER0_STATE_OF_PLAY.md
72d1b073bb0bdb837b60b1b02ca211f825e2bce1992c37c4a72bbb806161b919  PHASE_DIAGRAM_EXPERIMENT.md
```
