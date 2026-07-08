# Human connectome data (Suárez et al. 2021)

The multi-scale human connectome dataset used by **Suárez, Richards, Lajoie, Mišić
(2021), "Learning function from structure in neuromorphic networks", *Nature Machine
Intelligence* 3:771–786** — the project's connectome-RC anchor paper. Group of **70
healthy individual subjects**, Lausanne multi-scale parcellation (Cammoun et al. 2012),
with both structural and functional connectivity.

## File

- **`Individual_Connectomes.mat`** — MATLAB `.mat`, 700.9 MB (668 MiB). **Gitignored**
  (exceeds GitHub's 100 MB limit). The **primary Lausanne dataset**: Griffa, Alemán-Gómez,
  Hagmann, *Structural and functional connectome from 70 young healthy adults*, **Zenodo
  record 2872624** (2019) — Suárez et al. 2021 built on it. Download the single file from
  that record and place it here (our copy is byte-exact with the release). **Cortical-only:**
  `connMatrices.SC`/`FC` hold scales N = 68/114/219/448/1000 with no subcortical nodes. (The
  Zenodo *description* mentions an 83-region cortical+subcortical FreeSurfer parcellation —
  that is the atlas, not the delivered matrices.) Subcortical individual SC is therefore
  **unavailable from this primary file**; only the Suárez release's `connectivity/individual/`
  has it (below).

## Supplementary release — `Suarez2021_Data/`

The reproducibility bundle uploaded by Suárez et al. alongside the paper. **Gitignored**
(kept locally; download-documented here). As downloaded it was 728 MB. The 53 MB
`spin_test/` spatial-null CSVs were deleted (out of scope). The 665 MB per-subject
`connectivity/individual/` stacks were initially deleted (thought redundant with the `.mat`)
but have since been **restored and kept** — they are **not** redundant: the `.mat` is
cortical-only, whereas these stacks are **with-subcortical** (N=463/1015) and are the only
source of subcortical individual SC (Suárez had a fuller version than the public Griffa
`.mat`). Contents:

| subdir | contents |
|---|---|
| `connectivity/consensus/` | **The published distance-dependent group consensus** (Betzel 2018), weighted + symmetric + zero-diagonal. `human_250.npy` (N=463, density 6.19%), `human_500.npy` (N=1015, density 2.47% ≈ the paper's 2.5%). Used only as a **validation anchor**. |
| `connectivity/individual/` | **With-subcortical** per-subject SC stacks `(N, N, 70)`: `human_250.npy` (N=463, 120 MB), `human_500.npy` (N=1015, 577 MB). Raw source for the self-built **with-subcortical** consensus (`build_consensus_full`). Kept (gitignored); **transient** — only needed to (re)build the cached consensus, not at run time. |
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

**With-subcortical consensus (I/O-routing substrate).** The anatomical I/O-routing thread
(`experiments/human/human_mc_routing/`) needs subcortical *input* nodes, absent from the
cortical-only `.mat`. So a parallel **with-subcortical** self-built consensus (N=463/1015)
is built by `human_suarez.build_consensus_full` (driver
`experiments/human/build_consensus.py --full`) from the restored `connectivity/individual/`
stacks + the **full** (all-node) release geometry — the same Betzel procedure, just not
cortical-restricted. Validated vs the published with-subcortical consensus
(`connectivity/consensus/human_{250,500}.npy`): node-strength r = 0.997/0.993, shared-edge
weight r = 0.999, density matches, 0 isolated nodes — same quality as the cortical build.
Cached at `built_consensus/consensus_full_{448,1000}.npy` (gitignored). **Provenance
asymmetry:** the cortical substrate's SC is primary-source (the Griffa `.mat`); the
with-subcortical substrate's SC is necessarily Suárez-derived, since `connectivity/individual/`
is the only available with-subcortical individual source.

## Consensus construction (Betzel 2018 / Suárez 2021 procedure)

The substrate is a **distance-dependent group consensus** (Betzel et al. 2018) built from
the per-subject `.mat` SC — implemented in `src/connectomes/consensus.py`
(`struct_consensus`, vendored from `netneurotools`), driven by
`src/connectomes/human_suarez.build_consensus`. That module's docstring is the
authoritative algorithm description; the provenance is summarised here.

**Edge-weight definition (already in the data — not re-normalized).** Each individual SC
edge weight is a **fibre density**: the streamline count between two regions, normalized by
the **mean streamline length** and the **mean surface area of the two regions** (correcting
the bias toward longer fibres and for region-size differences). This is why the raw weights
are normalized fractions (median ~1e-3, max ~0.18), not integer counts.

**Procedure.** Preserve (1) the mean binary density and (2) the edge-length distribution of
the individuals: collate every edge present in ≥1 subject, bin by length (Euclidean
centroid distance), and per bin keep the `k` edges expressed in the most subjects (`k` = the
mean per-bin edge count across subjects); run intra- and inter-hemispheric edges separately
and union them; weight each surviving edge by its **mean across all subjects** (absent = 0).
Whole-brain binary density ≈ 2.5% (the paper's figure at N=1000). **Binning follows the
code**, not the paper's ambiguous "√(mean binary density) bins" wording (see the module
docstring).

**Geometry dependencies** (not in `Individual_Connectomes.mat`): parcel-centroid
coordinates (`coords/`) and hemisphere labels (`hemispheres/hemiid`) from the
`Suarez2021_Data/` release. **Verify** any rebuild against: density ≈ the paper's,
symmetric, non-negative, and an edge-length distribution tracking the group (our N=448/1000
builds validate vs the published consensus at density/hubs/weights r ≈ 0.99).

> *Suárez et al. 2021, verbatim:* "In constructing a consensus adjacency matrix, we sought
> to preserve (1) the density and (2) the edge length distribution… We first collated the
> extant edges… and binned them according to length. The number of bins was determined
> heuristically as the square root of the mean binary density across participants. The most
> frequently occurring edges were then selected for each bin. If the mean number of edges
> across participants in a particular bin is equal to k, we selected the k-edges of that
> length occurring most frequently across participants. We performed this procedure
> separately for inter- and intrahemispheric edges… The binary density for the final
> whole-brain matrix was 2.5% on average. The weight associated with each edge was then
> computed as the mean weight across all participants."

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
