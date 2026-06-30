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

- **Symmetric / undirected.** dMRI structural connectomes are symmetric → **normal**
  matrices (bulk ≈ top), unlike the *directed, non-normal* C. elegans connectome. By
  this project's own falsifiable prediction (the operating-point / robustness effect
  scales with directedness/non-normality), the human connectome should behave like the
  **v2a** undirected analogue — a *weaker* effect. This dataset is the natural test of
  that prediction.
- **Macro-scale, held out of the main scale row.** Per `PROJECT_PLAN.md`, the cellular
  scale row (C. elegans → fly → mouse) deliberately excludes the macro-scale human graph
  to avoid confounding organism with scale/resolution; the human connectome is admitted
  only as an **explicit, separate macro-scale generalisation probe**.
- **Scale.** Up to 1000 nodes — ~3× C. elegans (N=300); null generation and dense
  eigendecomposition (`sr_crit`, rescaling) need sparse/iterative handling at the larger
  scales.
- **70 individuals, not a group consensus** ("Individual_Connectomes"): a choice to make
  — per-subject runs vs a consensus matrix — and an inference-scope question distinct
  from the single-fixed-connectome C. elegans setup.
