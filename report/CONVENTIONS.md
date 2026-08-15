# Sweep conventions — read this first, every session

Shared constitution for the §4b front-to-back sweep. Every session loads this before
doing anything else.

---

## Canonical sources, in precedence order

1. **`TIER0_STATE_OF_PLAY.md`** — canonical for every *result*, number, withdrawal and
   artifact path. Where anything disagrees with it, it wins.
2. **`ACTION_PLAN_JOURNAL_ROADMAP.md` §1** — canonical for what is *claimed*: the six
   contributions and the "what must NOT be claimed" list.
3. **`PROJECT_KNOWLEDGE_BASE.md`** — canonical for what is *implemented* (repo layout,
   evaluators, ladder, hyperparameters).
4. **`report/FIGURE_LIST.md`** — canonical for which figures exist.

Anything predating 8 August 2026 may encode withdrawn claims. Treat it as suspect until
checked against `TIER0`.

## Withdrawn language — never write these

| do not write | write instead |
|---|---|
| "compact bulk", "compressed bulk" | "large spectral gap" (the absolute bulk is everyone's) |
| "the connectome is subcritically worse than ER" | "parity below criticality, advantage above" — and name the axis |
| "hub inhibition collapses memory" | "hub-targeted inhibition closes the advantage fastest; nothing collapses, the null moves" |
| "`sigma_eff` crosses 1 at the transition" | "`sigma_eff` is the best empirical **locator**"; the criterion is falsified |
| "generation tracks trajectory straightness" | "capacity is gated by which dynamical regime the manifold is in" |
| the crossing, quoted bare | always with its axis: the **first crossing inside full replicate coverage**, at (`sigma·bulk95` = 2.938, f = 0.153); five more sit past the coverage edge and must not be read; absent on the nominal axis |
| "the connectome is a better reservoir" | it is not, at the peak; the advantage is supercritical robustness |

## Numerical conventions

- **`sr_crit` = 1 / median_over_seeds(`bulk95`).** Median, not mean (Jensen: the per-seed
  mean of `1/bulk95` is biased upward by up to 0.087 at N=1000).
- **Two axes, always both.** `sigma·W/|lambda_1|` has spectral radius exactly sigma, so
  nominal matching fixes the Perron root and `sigma·bulk95` matching fixes the bulk.
  Neither is neutral toward the Perron-mode hypothesis. Report both, state what each holds
  fixed.
- **`bulk95` is a function of f.** Any (f, sigma) reindex needs per-(variant, f) `bulk95`
  from **the cell file's own column**, not one constant per variant. Take it from whichever
  file supplied the cells: `item2_f_extension_*` / `item3_f_extension_*` (sigma to 11.2,
  four variants) for anything new. `phase_cells.parquet` is censored at sigma = 6 and is
  the frozen historical capture — the extension reproduces it bit-for-bit, so prefer the
  extension unless reproducing a published number (`TIER0` §2.3, §6.4).
- **Ridge `alpha`** must be identical in `d_eff` and MC, or the +0.999 correspondence that
  licenses reading one through the other is void. Reparameterised as
  `alpha = lambda·trace(G)/N` at N=1000.
- **Report `d_eff / N` with the ceiling drawn** on every memory figure.

## Figure style contract

Fixed in session 0 and held across every figure so the chapters sit together.

- **Variant colours** (never varied), assigned once in `report/figlib/style.py`. **All
  seven rungs**, not five: the criticality-matched programme sweeps four
  (`connectome`, `connectome_weight_permuted`, `degree_rewire`, `erdos_renyi`) but
  Probe 3's ladder is seven, so `random_gaussian`, `clustering_rewire` and
  `modularity_rewire` need fixed colours too or F6 invents its own.
- **One substrate, one colour, thesis-wide.** The palette equals
  `src/experiment/plots._VARIANT_STYLE`, so a sweep figure and a committed per-task
  figure put the same substrate in the same colour. `style.check_colour_consistency()`
  asserts it and the smoke entry point runs it, so the two cannot drift silently.
- **Phase boundaries** get their own fixed pair (`style.BOUNDARY_COLOUR`): they are not
  variants, and the memory boundary is one colour everywhere it appears.
- Panel labels **a, b, c** lower-case bold, top-left.
- Font sizes: axis labels 9pt, ticks 8pt, panel labels 10pt bold.
- **300 dpi**, PDF plus PNG, written to `report/figures/`. PNGs are tracked, vector PDFs
  are gitignored and regenerable in one command.
- Every figure is produced by the shared figure module reading frozen parquets. **No
  hand-tuned one-offs** — when a number moves, everything rebuilds.
  `python -m report.figlib --verify | --smoke | --all | --only F7`.

## Working rules

1. **Reproduction gate before figures.** Recompute the act's headline numbers from frozen
   artifacts, check against `TIER0` to a stated precision, log the result in the act file.
   **A failed reproduction is the finding and it stops the act.** Do not regenerate the
   artifact to make a mismatch go away.
2. **Caption first.** If the caption cannot be written defensibly against `TIER0`, the
   figure should not exist in that form.
3. **No figure that is not on `FIGURE_LIST.md`.** If one seems missing, report and stop.
4. **A run happens only if a listed figure needs it** — except the four-task collection,
   which is banked deliberately.
5. **All runs collect MC, NARMA-10, Mackey-Glass and Lorenz.** Persist Gram eigenvalue
   spectra (N floats per cell), never states (10 to 44 MB per cell).
6. **Do not inspect Mackey-Glass results** until `PREREG_MACKEY_GLASS.md` sections 1 to 3
   are written and committed.
7. **Audit budget does not scale with tasks.** Reproduction gates on the primary task only;
   for NARMA and MG validate integrity (completion, no NaNs, seeds present, hyperparameters
   recorded) and stop.
8. **Negative results get figures**, placed where the claim they bound is made, not in an
   appendix.

## House style

British spelling. No em or en dashes. Guarded string-replacement edits with assertion
checks. Read source files before editing them. Variable names full and readable in code
(`spectral_radius`, not `sr`).
