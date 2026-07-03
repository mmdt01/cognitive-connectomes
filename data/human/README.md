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
  expect this path. **Cortical-only** parcellations (no subcortical nodes).

## Supplementary release — `Suarez2021_Data/`

The reproducibility bundle uploaded by Suárez et al. alongside the paper. **Gitignored**
(kept locally; download-documented here). As downloaded it was 728 MB; **trimmed to
~10 MB** — the 665 MB per-subject `connectivity/individual/` stacks and the 53 MB
`spin_test/` spatial-null CSVs were deleted (the individual data is redundant with the
`.mat`; spin tests are out of scope), leaving:

| subdir | contents |
|---|---|
| `connectivity/consensus/` | **The published distance-dependent group consensus** (Betzel 2018), weighted + symmetric + zero-diagonal. `human_250.npy` (N=463, density 6.19%), `human_500.npy` (N=1015, density 2.47% ≈ the paper's 2.5%). |
| `coords/` | Parcel-centroid MNI coordinates `(N, 3)` — edge length for `struct_consensus`. |
| `hemispheres/` | `hemiid` (0/1) hemisphere label per node. |
| `cortical/` | Cortical mask (`1`=cortical): 448 of 463 / 1000 of 1015. |
| `rsn_mapping/` | Yeo resting-state-network label per node (+ `subctx`). |

**Scale naming (important):** the release uses Cammoun **scale250 = 463 nodes** (448
cortical **+ 15 subcortical**) and **scale500 = 1015** (1000 + 15) — *with* subcortical,
unlike the cortical-only `.mat`. The release has **no N=219** (Cammoun scale125, a
distinct coarser parcellation), so the matched-to-*C. elegans* scale is unavailable here.

**Consensus substrate — self-built, published used only to validate.** We build our OWN
distance-dependent consensus (Betzel 2018) from the **`.mat` individual SC** (the raw
source) at **cortical N=448 and N=1000**, via `src/connectomes/consensus.py` +
`src/connectomes/human_suarez.build_consensus` (driver:
`experiments/human/build_consensus.py`), using this release's `coords`/`hemiid` for the
geometry (cortical subset; node order verified against the `.mat`, r≥0.98). It reproduces
the published consensus in **density** (5.3% vs 5.1% @448), **node-level hub structure**
(r=0.99) and **edge weights** (r=0.999 on shared edges), with **~52–58% edge overlap** —
the residual edge differences trace to the distance metric (Euclidean centroid distance vs
the original's surface-based distance). The published `human_250.npy`/`human_500.npy`
therefore serve as a **validation anchor**, not the substrate. Built consensus is cached
(gitignored, regenerable) at `data/human/built_consensus/consensus_{448,1000}.npy`.
**N=219 dropped** (no release geometry; the *C. elegans* node-count match is deprioritised).

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
