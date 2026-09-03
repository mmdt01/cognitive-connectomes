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
  mean of `1/bulk95` is biased upward, by up to **0.0431** within the four-rung ladder,
  at Erdős–Rényi N=1000). **Corrected 25 August 2026:** this clause read "up to 0.087 at
  N=1000", which is the gap for **`random_gaussian`** (0.0868), a rung *outside* the
  ladder and the one `common.SR_CRIT_CONVENTION`'s own source comment names. The
  convention does not change, only the number justifying it. Source:
  `report/act1_structure.md` §5 item 4; `TIER0` §1.3 carries the same correction.
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

- **Variant colours** (never varied), assigned once in `report/figlib/style.py`.
  **Amended once, in session 1: the palette is Okabe-Ito.** The session-0 set put the
  three nulls on purple / pink / light blue, which is weak under deuteranopia and
  collapses in greyscale — a defect in figures whose job is telling four substrates
  apart. Okabe-Ito is safe under all three common dichromacies and separates by
  luminance in greyscale, and it was already the palette of the committed E0.4 figures,
  so the change also ended a split between those and the sweep. `figlib/style.py` and
  `src/experiment/plots._VARIANT_STYLE` moved together in one commit and all 15 sweep
  figures plus the variant-styled per-task figures were re-rendered from frozen
  parquets. [There were 15 sweep figures on that date; the count is **17** as of
  25 August 2026, F17 added 19 August and F18 added 24 August. The sentence is left as
  the record of what was re-rendered then.] **This was a deliberate one-time amendment
  and is not a precedent**: the
  contract below still holds, and a session that wants a different colour reports and
  stops.
  **Four rungs carry almost everything**: `connectome`, `connectome_weight_permuted`,
  `degree_rewire`, `erdos_renyi` are the ladder the criticality-matched programme sweeps
  and the only variants in 12 of the 13 variant-bearing figure sources.
- **Three further rungs exist for exactly one figure.** `random_gaussian`,
  `clustering_rewire` and `modularity_rewire` appear only in `probe3_deff.parquet`, which
  feeds **F6 alone** — Probe 3's ladder is seven rungs and the PR-versus-`d_eff` ordering
  is computed across all of them. They are assigned fixed colours so F6 does not invent
  its own, and for no other reason. **A colour existing is not licence to add a variant to
  a ladder figure**: if one of the three turns up outside F6, that is a scope question,
  not a palette question. (An earlier version of this contract named five variants — the
  ladder plus `random_gaussian` — which was an odd cut, since rung 0 appears in exactly
  the same one figure as rungs 3 and 4.)
- **One substrate, one colour, thesis-wide.** The palette equals
  `src/experiment/plots._VARIANT_STYLE`, so a sweep figure and a committed per-task
  figure put the same substrate in the same colour. `style.check_colour_consistency()`
  asserts it and the smoke entry point runs it, so the two cannot drift silently.
- **Phase boundaries** get their own fixed pair (`style.BOUNDARY_COLOUR`): they are not
  variants, and the memory boundary is one colour everywhere it appears.
- **Non-variant quantities get their own namespace, and adding one is not a palette
  amendment.** The variant palette is amended once and was (session 1, to Okabe-Ito);
  everything else that needs colour gets a *separate* small set, because the thing being
  coloured is not a substrate. There are now five: `BASIS_COLOUR` (bases and measures,
  session 2), `BOUNDARY_COLOUR` (the two phase boundaries), `AXIS_COLOUR` (the two
  matching axes), `REGIME_COLOUR` (smooth against collapsed, session 4) and
  **`UNIT_COLOURS`** (individual reservoir units, added 2 September 2026 for F20).
  **The distinction is the whole point**: a namespace addition leaves `VARIANT_COLOUR`
  and `src/experiment/plots._VARIANT_STYLE` byte-identical and re-renders every existing
  figure unchanged, which an amendment does not. A session may add one; a session that
  wants a *variant* colour changed still reports and stops.

  **`UNIT_COLOURS` = `#3333BB` indigo, `#779955` olive, `#886699` plum**, ordered by the
  rank of the unit a figure highlights, never keyed by node index — which units a figure
  draws is that act's datum, not the contract's. **Off the Okabe-Ito wheel, and forced
  rather than chosen**: the wheel has eight hues, `VARIANT_COLOUR` spends seven and the
  eighth (`#F0E442`) is unusable on white, so any wheel triple *is* three substrate
  colours and sits at dE 0.0 from one. Measured, both plausible wheel triples also fail
  the separation floor — orange/blue/bluish green scores 14.4 among the three and
  orange/sky blue/reddish purple 15.2, the latter with the two lightest 0.011 apart in
  relative luminance, i.e. the same grey. This is `BASIS_COLOUR`'s wall and
  `BASIS_COLOUR`'s answer.

  **Chosen by measurement, on one floor more than `BASIS_COLOUR` had.** Worst-case CIE76
  dE in Lab after Vienot/Brettel dichromacy simulation, over normal vision and all three
  dichromacies:

  | check | `UNIT_COLOURS` | floor | `BASIS_COLOUR`, for reference |
  |---|---|---|---|
  | among the three | **55.5** | 25.0 | 50.8 |
  | against all seven substrate colours | **11.5** | 8.0 | 11.5 |
  | against white | **50.6** | 36.0 | 36.4 (its grey) |
  | greyscale relative-luminance gap | **0.103** | 0.08 | 0.064 |

  The white floor is the new one and it changed the answer: the search's first triple
  carried a pale mauve `#DDBBDD` at dE **23.4** from white, paler than any ink the thesis
  draws (the palest is the chance-baseline grey `#9A9A9A` at 36.4). It was **darkened** to
  `#886699` rather than swapped for a wheel colour, which is what lifts the minimum to
  50.6. All four floors are asserted inside `style.check_colour_consistency()` — the same
  function that guards the variant palette, so the smoke entry point already runs them —
  and all four were injection-tested, 4 of 4 firing on their own condition.
- Panel labels **a, b, c** lower-case bold, top-left.
- Font sizes: axis labels 9pt, ticks 8pt, panel labels 10pt bold.
- **300 dpi**, PDF plus PNG, written to `report/figures/`. PNGs are tracked, vector PDFs
  are gitignored and regenerable in one command.
- Every figure is produced by the shared figure module reading frozen parquets. **No
  hand-tuned one-offs** — when a number moves, everything rebuilds.
  `python -m report.figlib --verify | --smoke | --all | --only F7`.
- **One builder module per act, which is one module per session.** `report/figlib/
  figures/` is a package: the registry and its cap assertion in `__init__.py`, the
  builders in `act1_structure` / `act2_manifold` / `act3_memory` / `act3_prediction` /
  `act4_anchor`. **Edit your own act's module and nothing else** — a session touching
  another act's builders is either a cross-act figure (F3 and F16, whose owners
  `FIGURE_LIST` names explicitly) or a mistake. The registry stays central precisely so
  the cap cannot be raised a module at a time. Genuinely cross-act constants go in
  `figures/common.py`; act-local thresholds stay with the act that uses them.

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

British spelling. No em or en dashes **as punctuation**; a dash inside a proper noun is
that name's own typography and stays, which is why **Erdős–Rényi** keeps its en dash
everywhere, including in `style.VARIANT_TITLE` and therefore in every figure legend.
Guarded string-replacement edits with assertion
checks. Read source files before editing them. Variable names full and readable in code
(`spectral_radius`, not `sr`).
