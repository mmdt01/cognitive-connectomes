# Human connectome data (Suárez et al. 2021)

The multi-scale human connectome dataset used by **Suárez, Richards, Lajoie, Mišić
(2021), "Learning function from structure in neuromorphic networks", *Nature Machine
Intelligence* 3:771–786** — the project's connectome-RC anchor paper. Group of **70
healthy individual subjects**, Lausanne multi-scale parcellation (Cammoun et al. 2012),
with both structural and functional connectivity.

## File

- **`Individual_Connectomes.mat`** — MATLAB v5/v7 `.mat`, ~669 MB. **Gitignored**
  (too large for the GitHub 100 MB limit; see the repo `.gitignore`). Download it
  separately from the Suárez et al. (2021) data release and place it here; the loaders
  expect this path.

## Structure

`scipy.io.loadmat(..., struct_as_record=False, squeeze_me=True)` →
`connMatrices` (a MATLAB struct) with two fields, each a length-5 object array
over the five Lausanne parcellation scales:

| field | meaning | per-scale array `(N, N, 70)` — N nodes × N nodes × 70 subjects |
|---|---|---|
| `SC`  | **structural** connectivity (diffusion-MRI streamline-derived) | scales N = **68, 114, 219, 448, 1000** |
| `FC`  | **functional** connectivity (resting-state BOLD correlation)    | same five scales |

So `connMatrices.SC[s]` is the `(N_s, N_s, 70)` stack of structural matrices at scale
`s`, and `[:, :, k]` is subject `k`'s connectome. `SC` is the analogue of the
recurrent matrix `W` for a reservoir; `FC` is a functional target/probe, not the
substrate.

## Notes for use in this project

- **Symmetric / undirected, but non-negative and heavy-tailed → predicted STRONG effect
  (prediction reversed).** dMRI structural connectomes are symmetric → **normal**, unlike
  the directed, non-normal C. elegans connectome. The project's *original* prediction (the
  effect "scales with directedness/non-normality") said the human SC should behave like
  the weak undirected-gaussian case — but the **7-condition factorial reversed this**: the
  robustness is a **weight-SIGN (non-negativity / Perron) effect, essentially independent
  of directedness**. The human SC is non-negative *and* heavy-tailed — i.e. the
  `undirected_empirical` cell, which shows the **full** effect (MC connectome−degree d
  ≈ +9). So it is predicted to show a **strong** robustness crossover. Scoping confirms
  the spectral precondition (its bulk is compressed, `sr_crit` ≈ 2.1–4.0 across
  scales/consensus — *not* undirected-gaussian-like). This dataset is the external test of that sharpened
  prediction. See `PREDICTION_TASKS_INTERPRETATION.md` §6.
- **Macro-scale, held out of the main scale row.** Per `PROJECT_PLAN.md`, the cellular
  scale row (C. elegans → fly → mouse) deliberately excludes the macro-scale human graph
  to avoid confounding organism with scale/resolution; the human connectome is admitted
  only as an **explicit, separate macro-scale generalisation probe**.
- **Scale.** Up to 1000 nodes — ~3× C. elegans (N=300). Dense eigendecomposition is
  actually fine even at N=1000 (~0.1 s), so `sr_crit`/rescaling are cheap; the real costs
  are **null generation** (scales with edge count = density·N²) and **reservoir
  simulation** (O(N²)/step), sharpest in the N=1000 × 70-subject corner.
- **70 individuals, not a group consensus** ("Individual_Connectomes"): a choice to make
  — per-subject runs vs a consensus matrix — and an inference-scope question distinct
  from the single-fixed-connectome C. elegans setup.
