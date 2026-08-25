# METHODS: substrate and null construction

**Scope.** This file is **canonical for how the human substrate and its null ladder are
built, and for nothing else.** It records what the code does, sourced line by line to the
implementation. It is **subordinate to `PROJECT_KNOWLEDGE_BASE.md`** wherever the two
overlap: PKB §4–§5 remain the project-level statement of the loader surface and the rung
ladder, and if this file and PKB disagree about scope or naming, PKB governs and this file
should be corrected. It **carries no results**: every number here is a property of a
construction (a node count, an edge count, a density, a tolerance, a seed), never a
measured outcome. No `bulk95`, no `sr_crit`, no memory capacity, no effect size appears
below, and none should be added.

**Method.** Read-only extraction from source, 25 August 2026. Every fact carries a
`path:line`. Where a docstring and the implementation disagree, the **implementation** is
reported and the docstring is flagged — the repo has known stale-docstring cases
(`src/analysis/spectral.py:25` still carries withdrawn "compressed bulk" language), so
prose in the code is not treated as evidence of behaviour. The cross-checks in §C
reconstructed substrates **in memory only**; nothing under `experiments/` or
`eigenspectrum/results/` was written, and no parquet was regenerated.

---

## A. The consensus build

### A.1 Source data and subject count

| what | value | where |
|---|---|---|
| Primary file | `data/human/Individual_Connectomes.mat`, read via `scipy.io.loadmat(..., struct_as_record=False, squeeze_me=True, variable_names=["connMatrices"])` | [human_suarez.py:111-113](src/connectomes/human_suarez.py#L111-L113) |
| Field used | `connMatrices.SC` — a length-5 object array, one `(N, N, S)` stack per Lausanne scale | [human_suarez.py:113-114](src/connectomes/human_suarez.py#L113-L114) |
| Scale selection | by **node count**, not by index order: the stack whose `shape[0] == scale` | [human_suarez.py:115](src/connectomes/human_suarez.py#L115) |
| Subject count | **70** — the third axis of the selected stack. The code reads it live (`stack.shape[2]`) and records it as `n_subjects_in_file`; the build's `construction_notes` interpolate it into the metadata string | [human_suarez.py:140](src/connectomes/human_suarez.py#L140), [human_suarez.py:170](src/connectomes/human_suarez.py#L170), [human_suarez.py:377-383](src/connectomes/human_suarez.py#L377-L383) |
| Subject-count caveat | an inline comment records that **the `.mat` carries 70 subjects while the paper reports 66**, "logged, not reconciled" | [human_suarez.py:169](src/connectomes/human_suarez.py#L169) |
| Cited source | "Suárez et al. 2021, Nat. Mach. Intell. 3:771-786" in the single-subject metadata; the consensus build attributes the SC to "Suárez et al. 2021 individual Lausanne SC (Individual_Connectomes.mat)" | [human_suarez.py:164](src/connectomes/human_suarez.py#L164), [human_suarez.py:376](src/connectomes/human_suarez.py#L376) |

The frozen cache metadata confirms 70 for both scales:
`data/human/built_consensus/consensus_448.meta.json` and `consensus_1000.meta.json` each
record `"Self-built from the 70-subject cortical individual SC at scale N=..."`.

### A.2 What the edge weights are, and what is done to them

- The code labels the modality **"dMRI structural connectivity (streamline fibre
  density)"** ([human_suarez.py:165](src/connectomes/human_suarez.py#L165)) and describes
  the values as **"fibre densities — normalized fractions, not integer counts"**
  ([human_suarez.py:173](src/connectomes/human_suarez.py#L173)).
- **No transform is applied.** The project weight transform is set to `"raw"`, with the
  comment "SC weights are already normalized fractions; project default is `raw`"
  ([matrix_config.py:104-105](experiments/human/matrix_config.py#L104-L105)). The stack is
  cast to `float` and passed to the consensus routine unmodified
  ([human_suarez.py:118](src/connectomes/human_suarez.py#L118),
  [human_suarez.py:373](src/connectomes/human_suarez.py#L373)); no log, no z-score, no
  thresholding, no density normalisation appears anywhere on the path from the `.mat` to
  the substrate.
- The only value-level operation in the whole build is the consensus weighting itself
  (§A.4) and the zeroing of the diagonal (§A.5).
- **What "fibre density" physically means is not defined in the code** — see §D.1.

### A.3 Parcellation, and how N = 448 / N = 1000 are defined

- Parcellation: **Lausanne / Cammoun**, recorded as `f"Lausanne/Cammoun scale N={N}"`
  ([human_suarez.py:166](src/connectomes/human_suarez.py#L166)). The five available scales
  are `SCALES = (68, 114, 219, 448, 1000)`
  ([human_suarez.py:43](src/connectomes/human_suarez.py#L43)).
- **N = 448 and N = 1000 are cortical-only.** The `.mat` stacks are cortical
  ([human_suarez.py:4-6](src/connectomes/human_suarez.py#L4-L6)), and the geometry needed
  by the consensus is **restricted to the cortical subset** before use.
- The geometry lives at the *with-subcortical* scales in the Suárez release, mapped by
  `_MAT_N_TO_RELEASE_TAG = {448: "250", 1000: "500"}`
  ([human_suarez.py:50](src/connectomes/human_suarez.py#L50)). The release's scale250 is
  N = 463 and scale500 is N = 1015; the extra 15 nodes are subcortical.
- Restriction is by **mask, not by slice**: `cidx = np.where(cortical != 0)[0]` and the
  coordinates/hemisphere labels are indexed by `cidx`
  ([human_suarez.py:196-204](src/connectomes/human_suarez.py#L196-L204)). The comment
  states the reason — "the cortical nodes are interspersed (not a leading block)"
  ([human_suarez.py:192-193](src/connectomes/human_suarez.py#L192-L193)).
- A hard guard asserts the restriction produced exactly the expected count:
  `if len(cidx) != scale: raise ValueError(...)`
  ([human_suarez.py:201-202](src/connectomes/human_suarez.py#L201-L202)).
- **What happens to the subcortical parcels in the cortical build: they are never
  present.** They are absent from the `.mat` SC entirely, and they are dropped from the
  geometry by `cidx`. They are not zeroed, not merged, not averaged — the cortical build
  simply never sees them.
- A **separate** with-subcortical build exists (`build_consensus_full`, N = 463/1015,
  [human_suarez.py:389-419](src/connectomes/human_suarez.py#L389-L419)) for the anatomical
  I/O-routing thread. It is **not** the substrate of the null-ladder work: the ladder
  substrate is `source="consensus"` → `load_built_consensus`
  ([matrix_config.py:31-32](experiments/human/matrix_config.py#L31-L32),
  [substrates.py:52-53](experiments/human/substrates.py#L52-L53)).

### A.4 The consensus rule, in full

The rule is the vendored Betzel et al. (2018) distance-dependent structural consensus,
`struct_consensus`, in [src/connectomes/consensus.py](src/connectomes/consensus.py)
(vendored from `netneurotools.networks`, [consensus.py:1-9](src/connectomes/consensus.py#L1-L9)).
It is invoked once, from the shared build helper
([human_suarez.py:334-338](src/connectomes/human_suarez.py#L334-L338)):

```
distance = cdist(coords, coords)
C = struct_consensus(stack, distance, hemiid.reshape(-1, 1), weighted=weighted)
```

**1. Distance.** `distance[i, j]` is the **Euclidean distance between parcel centroids**,
computed by `scipy.spatial.distance.cdist` on the release's MNI coordinates
([human_suarez.py:334](src/connectomes/human_suarez.py#L334); the argument is documented as
"Euclidean distance between parcel centroids" at
[consensus.py:57-58](src/connectomes/consensus.py#L57-L58)).

**2. Hemisphere split — the procedure runs twice.** `for conn_type in range(2)` runs the
whole selection separately for **inter-hemispheric** and **intra-hemispheric** edges
([consensus.py:90](src/connectomes/consensus.py#L90)), each with its own `keep_conn` mask
built from the 0/1 `hemiid` ([consensus.py:91-98](src/connectomes/consensus.py#L91-L98)).
The two results are unioned at the end.

**3. Per-edge statistics across subjects.**
- `pos_data = data > 0` — presence per subject ([consensus.py:82](src/connectomes/consensus.py#L82)).
- `pos_data_count` — **number of subjects expressing each edge**
  ([consensus.py:83](src/connectomes/consensus.py#L83)).
- `average_weights = data.sum(axis=2) / pos_data_count` — the mean weight **over the
  subjects in which the edge is present** ([consensus.py:85-86](src/connectomes/consensus.py#L85-L86)).
  This quantity is used **only as a tie-breaker** (step 6); it is *not* the weight
  assigned to the surviving edge (step 7).

**4. How many edges are kept.** `pos_dist` is the multiset of edge lengths of every
present edge in every subject, restricted to this connection type and to the upper
triangle ([consensus.py:104-106](src/connectomes/consensus.py#L104-L106)). The target
count is
`avg_conn_num = len(pos_dist) / num_sub` — the **mean number of present edges per subject**
of that connection type ([consensus.py:109-114](src/connectomes/consensus.py#L109-L114)).
This is what makes the consensus **mean-binary-density preserving**. It can be overridden
by the optional `conn_num_inter` / `conn_num_intra` arguments; the project's build passes
neither, so both are estimated ([human_suarez.py:335-338](src/connectomes/human_suarez.py#L335-L338)).

**5. The binning — one length bin per edge to be added.** The empirical CDF of `pos_dist`
is taken ([consensus.py:32-39](src/connectomes/consensus.py#L32-L39),
[consensus.py:116](src/connectomes/consensus.py#L116)), then scaled and rounded to integer
bin indices, `cumprob = np.round(cumprob * avg_conn_num).astype(int)`
([consensus.py:117](src/connectomes/consensus.py#L117)). The loop then runs
`for n in range(1, int(avg_conn_num) + 1)`
([consensus.py:121](src/connectomes/consensus.py#L121)) — i.e. **the number of length bins
equals the number of edges to be added, and exactly one edge is selected per bin.**

> **Documented divergence from the paper, and the code is the authority.** The module
> docstring states this explicitly: binning follows the **code** — one length bin per
> edge to be added — "NOT the paper's ambiguous 'sqrt(mean binary density) bins' wording"
> ([consensus.py:18-21](src/connectomes/consensus.py#L18-L21)). The implementation matches
> that statement. Any chapter text describing "√(mean binary density) bins", or "the k
> most frequent edges per bin" with k > 1, describes the paper and not this build.

**6. How the consensus edge in a bin is selected.** Within bin `n`:
- the bin's length window is `[curr_quant.min(), curr_quant.max()]`, and `mask` is every
  upper-triangle node pair of this connection type whose centroid distance falls inside it
  ([consensus.py:122-128](src/connectomes/consensus.py#L122-L128));
- among those candidates, the edge **expressed in the most subjects** wins:
  `indmax = np.argwhere(c == c.max())` where `c = pos_data_count[i, j]`
  ([consensus.py:129](src/connectomes/consensus.py#L129), [consensus.py:131](src/connectomes/consensus.py#L131));
- **ties are broken by the higher mean weight** over the subjects expressing the edge:
  `indmax = indmax[np.argmax(w[indmax])]` with `w = average_weights[i, j]`
  ([consensus.py:130](src/connectomes/consensus.py#L130), [consensus.py:134-136](src/connectomes/consensus.py#L134-L136));
- an empty bin is skipped (`if curr_quant.size == 0: continue`,
  [consensus.py:124-125](src/connectomes/consensus.py#L124-L125)), so the realised edge
  count can fall short of `avg_conn_num`;
- the winner is written into a **binary** matrix: `group_conn_type[...] = 1`
  ([consensus.py:133](src/connectomes/consensus.py#L133), [consensus.py:136](src/connectomes/consensus.py#L136)).
  Because the same node pair can win in more than one bin, the number of *distinct* edges
  set is at most the number of bins.

**7. How the surviving edge's weight is assigned.** The inter/intra binary results are
summed and symmetrised (step 8), and then — and only if `weighted=True` — multiplied
elementwise by the **mean over ALL subjects, with an absent edge counting as 0**:

```
consensus = consensus * np.mean(data, axis=2)          # consensus.py:144-145
```

This is **not** `average_weights` (the present-subjects mean of step 3). The module
docstring calls the distinction out explicitly at
[consensus.py:22-25](src/connectomes/consensus.py#L22-L25), and the implementation matches
it. The project build always passes `weighted=True`
([human_suarez.py:364](src/connectomes/human_suarez.py#L364),
[build_consensus.py:73](experiments/human/build_consensus.py#L73)), and the frozen cache
metadata records `"weighted": true` at both scales.

**8. Symmetrisation.** The two connection types are collapsed and the result is symmetrised
by a logical OR with its transpose, *before* weighting:

```
consensus = consensus.sum(axis=2)
consensus = np.logical_or(consensus, consensus.T).astype(int)   # consensus.py:141-142
```

so the binary mask is exactly symmetric, and multiplying by the symmetric
`np.mean(data, axis=2)` keeps it symmetric. **The matrix is undirected by construction.**
The loader docstring states the downstream consequence: "SC is symmetric (undirected), so
the reservoir orientation `adjacency[i, j] = weight j->i` is moot — the matrix is its own
transpose" ([human_suarez.py:19-21](src/connectomes/human_suarez.py#L19-L21)).

**9. Self-loops.** Two mechanisms, only one of which is load-bearing:
- *Inside* `struct_consensus`, a diagonal entry can never be selected: bin windows are
  built from `pos_dist`, which is filtered to strictly non-zero distances
  (`pos_dist[np.nonzero(pos_dist)]`, [consensus.py:106](src/connectomes/consensus.py#L106)),
  and a node's distance to itself is 0, so `full_dist_conn >= curr_quant.min() > 0` excludes
  it ([consensus.py:126-127](src/connectomes/consensus.py#L126-L127)).
- *After* the call, the diagonal is **explicitly zeroed regardless**:
  `np.fill_diagonal(C, 0.0)` ([human_suarez.py:339](src/connectomes/human_suarez.py#L339)).
  This is the enforcement to cite. The single-subject loader does the same and *counts*
  what it removed ([human_suarez.py:151-153](src/connectomes/human_suarez.py#L151-L153)),
  because the raw per-subject SC does carry self-weights; the consensus path does not
  report a count.
- Verified empirically (§C): the cached consensus has a strictly zero diagonal at both
  scales.

### A.5 Non-negativity, and where it is enforced

**The matrix is non-negative by construction, and the property is additionally asserted.**

- *By construction*: the binary consensus is `{0, 1}`
  ([consensus.py:142](src/connectomes/consensus.py#L142)) and it is multiplied by
  `np.mean(data, axis=2)` ([consensus.py:145](src/connectomes/consensus.py#L145)), a mean of
  dMRI fibre densities, which are non-negative — the single-subject loader asserts exactly
  that on the raw stack ([human_suarez.py:148](src/connectomes/human_suarez.py#L148)).
- *By assertion*: immediately after the build,
  `_assert_symmetric_nonneg(C, "consensus")`
  ([human_suarez.py:340](src/connectomes/human_suarez.py#L340)) checks
  `max|C - C.T| < 1e-9` **and** `C.min() >= 0.0`
  ([human_suarez.py:71-74](src/connectomes/human_suarez.py#L71-L74)). This is the single
  place where symmetry and non-negativity are both enforced on the substrate, and it runs
  on every build.
- Note the assertion runs at **build** time, not at **load** time: the cached loader
  `_load_cached_consensus` reads the `.npy` and does *not* re-assert
  ([human_suarez.py:422-441](src/connectomes/human_suarez.py#L422-L441)). §C confirms the
  cached matrices in fact satisfy both properties exactly.

### A.6 Node count, edge count and density of the built substrate

Counted by `_graph_stats`, which treats any non-zero entry as an edge, halves for
undirected, and divides by `N(N-1)/2`
([human_suarez.py:61-67](src/connectomes/human_suarez.py#L61-L67)):

| scale | N | undirected edges | density | isolated nodes |
|---|---|---|---|---|
| 448 | 448 | **5,323** | **5.3162 %** (`0.0531619527005433`) | 0 |
| 1000 | 1000 | **10,784** | **2.1590 %** (`0.021589589589589588`) | 0 |

Source: the frozen build metadata,
`data/human/built_consensus/consensus_448.meta.json` and
`consensus_1000.meta.json` (`n_edges`, `density`, `n_isolated_nodes`), reproduced live from
the cached `.npy` by `HumanSubstrateBuilder.summary()`
([substrates.py:289-303](experiments/human/substrates.py#L289-L303)) — see §C.

**Check passed.** The N = 1000 edge count recorded elsewhere in the report set as
**10,784 undirected edges** is reproduced exactly, independently, from the code path. The
N = 448 figure — **5,323 undirected edges, density 5.3162 %** — is the one that appears in
no report document (`report/facts/GAPS.md:32`).

One caveat on the counting rule: because `_graph_stats` uses `C != 0`, an edge selected by
the consensus whose mean-over-all-subjects weight were exactly 0 would be invisible to the
count. It cannot arise here — a selected edge is expressed in at least one subject, so its
all-subject mean is strictly positive — but the count is a count of **non-zero weights**,
not of selected mask entries.

### A.7 From consensus to substrate: what the builder derives

`HumanSubstrateBuilder.__init__` ([substrates.py:46-92](experiments/human/substrates.py#L46-L92))
loads the cached consensus (`source="consensus"`,
[substrates.py:52-53](experiments/human/substrates.py#L52-L53)) and derives, once:

| object | definition | where |
|---|---|---|
| `sc_weighted` | the consensus itself, `float` copy — **this is the `connectome` variant under `human_empirical`** | [substrates.py:71](experiments/human/substrates.py#L71), [substrates.py:158-159](experiments/human/substrates.py#L158-L159) |
| `mask` | `(sc_weighted != 0).astype(float)` — the binary symmetric topology every null rewires | [substrates.py:72](experiments/human/substrates.py#L72) |
| `_upper` | strict upper triangle of `mask` (`k=1`) | [substrates.py:73](experiments/human/substrates.py#L73) |
| `empirical_pool` | `sc_weighted[_upper]` — **one entry per undirected edge**: 5,323 at N = 448, 10,784 at N = 1000 | [substrates.py:74](experiments/human/substrates.py#L74) |
| `sign_coverage` | all-excitatory placeholder; there is **no Dale layer** at macro scale | [substrates.py:77-83](experiments/human/substrates.py#L77-L83) |
| `partition` | one fixed undirected Louvain partition of `mask`, `seed = LOUVAIN_SEED = 0`, computed **once** and reused for every modularity-rewire seed | [substrates.py:86-88](experiments/human/substrates.py#L86-L88), [matrix_config.py:107](experiments/human/matrix_config.py#L107) |

Masks are cached per `(variant, seed)` in `_mask_cache`
([substrates.py:90](experiments/human/substrates.py#L90),
[substrates.py:95-97](experiments/human/substrates.py#L95-L97)), so a given
`(variant, seed)` is generated once per process and is bit-identical on every later call.

---

## B. The null ladder, rung by rung

### B.0 How a variant becomes a matrix

Two stages, and the distinction matters for every claim below.

1. **Topology.** `HumanSubstrateBuilder.get_mask(variant, seed)`
   ([substrates.py:94-141](experiments/human/substrates.py#L94-L141)) dispatches to a
   generator in `src/nulls/`, always with `directed=False`. The generators consume and
   return a **binary** mask; they know nothing about weights.
2. **Weights.** `HumanSubstrateBuilder.weighted(condition, variant, seed)`
   ([substrates.py:143-180](experiments/human/substrates.py#L143-L180)) then paints weights
   onto that mask via `apply_weight_scheme`
   ([src/reservoir/weights.py](src/reservoir/weights.py)).

Under the substrate condition **`human_empirical`**
([matrix_config.py:34](experiments/human/matrix_config.py#L34)):

- `variant == "connectome"` returns the **real** consensus untouched,
  `self.sc_weighted.copy()` ([substrates.py:158-159](experiments/human/substrates.py#L158-L159));
- every **null** rung is weighted by `symmetric_empirical`
  ([substrates.py:160-163](experiments/human/substrates.py#L160-L163)), which draws one
  value **per undirected edge, with replacement, from `empirical_pool`** and mirrors it:
  `rng.choice(empirical_weights, size=int(upper_mask.sum()), replace=True)` then
  `weighted + weighted.T` ([weights.py:163-167](src/reservoir/weights.py#L163-L167));
- `connectome_weight_permuted` bypasses the mask ladder entirely
  ([substrates.py:145-147](experiments/human/substrates.py#L145-L147)) — see §B.1.

Three invariants are asserted on every mask before weighting: square, `{0,1}`-valued, and
zero diagonal ([weights.py:77-81](src/reservoir/weights.py#L77-L81)); `symmetric_empirical`
adds a symmetry assertion ([weights.py:156-157](src/reservoir/weights.py#L156-L157)).

**Seeding, stated once.** The **same integer** `seed` drives both the topology draw and
the weight draw for a cell — `get_mask(variant, seed)` and
`apply_weight_scheme(..., seed=seed)` ([substrates.py:148](experiments/human/substrates.py#L148),
[substrates.py:161](experiments/human/substrates.py#L161)). Mask and weights are therefore
**not independently seeded**. Seeds are `range(N_SEEDS)` with `N_SEEDS = 10`
([matrix_config.py:102](experiments/human/matrix_config.py#L102)).

**Does one seed give the same graph across rungs? No — the rungs are effectively
independent.** They do not even share an RNG family: `erdos_renyi` and `degree_rewire`
pass the integer to networkx, whose `@py_random_state` decorator makes a
`random.Random(seed)` (stdlib Mersenne Twister), while `clustering_rewire` and
`modularity_rewire` build `np.random.default_rng(seed)` (numpy PCG64)
([clustering_rewire.py:113](src/nulls/clustering_rewire.py#L113),
[modularity_rewire.py:104](src/nulls/modularity_rewire.py#L104)). Measured at N = 448,
seed 0: the Jaccard overlap of the Erdős–Rényi and degree-rewire edge sets is **0.0284**,
against a chance floor of **0.0273** at this density — i.e. indistinguishable from
independent. Two Erdős–Rényi graphs at seeds 0 and 1 overlap at **0.0314**. The generators
*are* individually deterministic: `erdos_renyi.generate(base, seed=0)` called twice is
bit-identical.

---

### B.1 `connectome_weight_permuted` — the placement control (rung index −1)

It is a **control, not a rung**: `VARIANT_RUNG["connectome_weight_permuted"] = -1`
([matrix_config.py:77](experiments/human/matrix_config.py#L77)), and the comment in the
variant list marks it "placement control (not a rung)"
([matrix_config.py:67](experiments/human/matrix_config.py#L67)).

Implemented by `_weight_permuted`
([substrates.py:182-217](experiments/human/substrates.py#L182-L217)). Under
`human_empirical` ([substrates.py:206-209](experiments/human/substrates.py#L206-L209)):

```
permuted[up] = rng.permutation(self.empirical_pool)
return permuted + permuted.T
```

| property | what happens |
|---|---|
| Node count | **N, unchanged** — the connectome's own index set |
| Edge count | **exactly preserved**, and it is the *same edge set*, not merely the same count: the topology is `self.mask` untouched |
| Density | **exactly the connectome's** |
| Weight multiset | **exactly preserved.** `rng.permutation` of `empirical_pool` is a **permutation** — not a resample with replacement, not a resample without replacement from a larger pool, not a fitted distribution. Verified in §C: the sorted upper-triangle weight multiset is identical to the connectome's |
| Degree sequence | **exactly preserved** (topology untouched) |
| Symmetry | exact — one draw per undirected edge, mirrored by `permuted + permuted.T` |
| Self-loops | none: the permutation is written only into `self._upper`, a strict upper triangle |
| Seeding | `np.random.default_rng(seed)` ([substrates.py:196](experiments/human/substrates.py#L196)) |

**What is randomised: which edge carries which weight, and nothing else.** The docstring's
decomposition is accurate to the implementation — *connectome vs this* isolates weight
**placement**; *this vs `degree_rewire`* isolates **topology**
([substrates.py:183-192](experiments/human/substrates.py#L183-L192)).

**No `validate_null` call is made for this variant** — no recorder fires in `get_mask`,
because the mask ladder is bypassed before `get_mask` is reached
([substrates.py:145-148](experiments/human/substrates.py#L145-L148)).

---

### B.2 `erdos_renyi` — rung 1

**This is a `G(n, m)` construction, not `G(n, p)`.** That is the priority question and the
answer is unambiguous.

The undirected path is three lines
([erdos_renyi.py:34-38](src/nulls/erdos_renyi.py#L34-L38)):

```
n = adjacency.shape[0]
n_edges = int((adjacency != 0).sum() // 2)
graph = nx.gnm_random_graph(n, n_edges, seed=seed)
return nx.to_numpy_array(graph)
```

`nx.gnm_random_graph(n, m)` is documented as returning "a graph chosen uniformly at random
from the set of all graphs with `n` nodes and `m` edges", and its implementation rejects
`u == v` and `G.has_edge(u, v)` before adding, so the output is a **simple graph: no
self-loops, no multi-edges**. `nx.empty_graph(n)` seeds all `n` nodes first, so the node
count is `n` even if some end isolated.

| property | what happens |
|---|---|
| Node count | **N, exactly** |
| Edge count | **exactly preserved** — `m` is read off the input and passed as a hard count, not a probability. Not "in expectation" |
| Density | **exactly the connectome's**, as a consequence of the exact `m` |
| Weight multiset | **not preserved.** The generator produces topology only; under `human_empirical` the weights are **resampled with replacement** from `empirical_pool` ([weights.py:164-166](src/reservoir/weights.py#L164-L166)) |
| Degree sequence | **not preserved** — randomised. Verified in §C |
| Symmetry | exact (an undirected `nx.Graph` → symmetric array) |
| Self-loops | none |
| Seeding | integer → `random.Random(seed)` inside networkx |

**The docstring is correct.** The module docstring is titled "Erdős–Rényi G(N, M) random
graph: matched exact edge count" and says "Preserves N and exact undirected edge count.
Built by picking M of the C(N, 2) possible undirected edges uniformly at random"
([erdos_renyi.py:1-6](src/nulls/erdos_renyi.py#L1-L6)). This matches the implementation.

> **The distinction the chapter has to make.** "Matched edge count" is the correct claim
> and it implies matched density exactly. "Matched density" alone would be the weaker
> `G(n, p)` claim and would be *wrong* here — it is `random_gaussian` (rung 0), not
> `erdos_renyi`, that matches density only in expectation
> ([random_gaussian.py:44-50](src/nulls/random_gaussian.py#L44-L50)); its edge count is
> Binomial across seeds and measurably varies (§C.4).

**`validate_null` call.** `_record_edge_count`
([substrates.py:226-233](experiments/human/substrates.py#L226-L233)) runs
`validate_null(base, mask, "edge_count")`, which compares `int(original.sum())` to
`int(generated.sum())` — the full matrix sums, i.e. twice the undirected edge count for a
symmetric binary mask ([validation.py:60-64](src/nulls/validation.py#L60-L64)) — and
asserts equality. **The test is exact and it is a genuine test of the claim.** But see
§B.6: like every other assertion in this builder, it checks something the generator
guarantees by construction, so it can catch a wiring error but cannot fail on a correctly
wired `gnm_random_graph`.

---

### B.3 `degree_rewire` — rung 2

Undirected path ([degree_rewire.py:44-56](src/nulls/degree_rewire.py#L44-L56)):

```
binary_mask = (adjacency != 0).astype(int)
graph = nx.from_numpy_array(binary_mask.astype(float))
n_swaps = n_swaps_multiplier * graph.number_of_edges()
nx.double_edge_swap(graph, nswap=n_swaps, max_tries=n_swaps * 10, seed=seed)
return nx.to_numpy_array(graph)
```

`n_swaps_multiplier` is supplied by the builder as `config.SWAP_MULTIPLIER = 10`
([substrates.py:106-109](experiments/human/substrates.py#L106-L109),
[matrix_config.py:108](experiments/human/matrix_config.py#L108)). At N = 448 that is
**53,230** target accepted swaps against a cap of 532,300 attempts; at N = 1000,
**107,840** against 1,078,400.

| property | what happens |
|---|---|
| Node count | **N, exactly** |
| Edge count | **exactly preserved** — a double-edge swap removes two edges and adds two |
| Density | **exactly the connectome's** |
| Weight multiset | **not preserved**; resampled with replacement from `empirical_pool` under `human_empirical` |
| Degree sequence | **exactly preserved, per node** — that is what the swap is for. Verified in §C |
| Symmetry | exact |
| Self-loops | none — networkx's swap rejects `ui == xi` and `v == y`, and refuses to create parallel edges |
| Seeding | integer → `random.Random(seed)` inside networkx |

**What is randomised: which nodes connect, subject to every degree being held fixed.**

**Two implementation notes the docstring does not carry.**
- The docstring describes the swap as `(u,v),(x,y) → (u,y),(x,v)`
  ([degree_rewire.py:5-8](src/nulls/degree_rewire.py#L5-L8)); networkx's
  `double_edge_swap` in fact removes `u-v`, `x-y` and adds `u-x`, `v-y`. The two are the
  same move family under relabelling of an undirected edge's endpoints, so this is
  **cosmetic** — no preserved property changes. Reported for accuracy, not as a defect.
- networkx picks the two **source** nodes with probability **weighted by degree**
  (`cumulative_distribution(degrees)`), not uniformly from the edge list. Rungs 3 and 4
  instead draw uniformly from an explicit edge list
  ([clustering_rewire.py:122](src/nulls/clustering_rewire.py#L122),
  [modularity_rewire.py:112-113](src/nulls/modularity_rewire.py#L112-L113)). The proposal
  distributions therefore differ across rungs. This does not change what any rung
  *preserves*.
- The docstring's closing line, "sufficient to decorrelate at N=300 for this density"
  ([degree_rewire.py:12-13](src/nulls/degree_rewire.py#L12-L13)), understates where the
  setting has been checked — `report/act1_structure.md` §5 item 3 records a direct
  convergence test at N = 1000. Flagged as stale scope, not as wrong.

**`validate_null` call — and it is weaker than it looks.** `_record_degree`
([substrates.py:234-243](experiments/human/substrates.py#L234-L243)) runs
`validate_null(base, mask, "degree_sequence")`, which compares **sorted row sums**
([validation.py:66-72](src/nulls/validation.py#L66-L72)). Double-edge swaps preserve every
degree **by construction, after any number of swaps including zero**, so this assertion
passes on a chain that never accepted a single swap. **It is not a convergence test and
must not be quoted as one.** See §B.6.

---

### B.4 `clustering_rewire` — rung 3

Undirected path, [clustering_rewire.py:99-176](src/nulls/clustering_rewire.py#L99-L176).
Constrained double-edge swaps: rung 2's move, accepted only if the graph's **total
triangle count** stays within a relative tolerance of the input's.

- Target accepted swaps `= 10 × n_edges` ([clustering_rewire.py:101](src/nulls/clustering_rewire.py#L101));
  attempt cap `= 100 × target` ([clustering_rewire.py:102](src/nulls/clustering_rewire.py#L102),
  default `max_attempts_multiplier = 100`).
- `T_initial = sum(nx.triangles(graph).values()) // 3`
  ([clustering_rewire.py:104-105](src/nulls/clustering_rewire.py#L104-L105)); a
  triangle-free input raises ([clustering_rewire.py:106-110](src/nulls/clustering_rewire.py#L106-L110)).
- A proposal is rejected outright if the four endpoints are not distinct
  ([clustering_rewire.py:131-132](src/nulls/clustering_rewire.py#L131-L132)) or if either
  new edge already exists ([clustering_rewire.py:133-134](src/nulls/clustering_rewire.py#L133-L134)).
- The swap is applied, the triangle delta computed from common-neighbour counts
  ([clustering_rewire.py:136-152](src/nulls/clustering_rewire.py#L136-L152)), and the
  **acceptance test** is
  `abs(T_new - T_initial) / T_initial <= tolerance`
  ([clustering_rewire.py:154](src/nulls/clustering_rewire.py#L154)); otherwise it is
  reverted edge for edge ([clustering_rewire.py:159-163](src/nulls/clustering_rewire.py#L159-L163)).
- `tolerance` is supplied by the builder as `config.CLUSTERING_TOLERANCE = 0.05`
  ([substrates.py:111-119](experiments/human/substrates.py#L111-L119),
  [matrix_config.py:106](experiments/human/matrix_config.py#L106)).
- The builder wraps the call in `warnings.simplefilter("error", RuntimeWarning)`
  ([substrates.py:112-113](experiments/human/substrates.py#L112-L113)), so the generator's
  "acceptance rate below 1%" warning ([clustering_rewire.py:166-173](src/nulls/clustering_rewire.py#L166-L173))
  becomes a hard failure in this pipeline.

| property | what happens |
|---|---|
| Node count | **N, exactly** |
| Edge count | **exactly preserved** (rung-2 move) |
| Density | **exactly the connectome's** |
| Weight multiset | **not preserved**; resampled with replacement from `empirical_pool` |
| Degree sequence | **exactly preserved, per node** |
| Symmetry | exact |
| Self-loops | none (four-distinct-endpoints test, plus `nx.Graph`) |
| Seeding | `np.random.default_rng(seed)` ([clustering_rewire.py:113](src/nulls/clustering_rewire.py#L113)) |

**What is preserved beyond rung 2: the global clustering coefficient, within 5 % relative.**
The acceptance test is on the raw **triangle count** `T`, whereas the name and the
`validate_null` check are on **transitivity**. These are the same constraint here: with the
degree sequence fixed, transitivity `= 3T / Σᵢ C(dᵢ, 2)` has a denominator invariant under
the swap, so the relative drift in transitivity equals the relative drift in `T` exactly.

> **A measured caveat the chapter should carry.** The chain does not merely stay inside the
> band — it **runs to the edge of it**. At N = 448, all ten seeds land at
> `T_initial = 17,120 → T_final ≈ 16,265`, a relative drift of **4.99 %** against a
> tolerance of 5.00 %. "Clustering preserved within 5 %" is literally true and is what the
> assertion tests; "clustering unchanged" would be false. Measured acceptance rate at
> N = 448 is **10.7–11.5 %** across the ten seeds, comfortably above the 1 % warning floor.

**Docstring flags.**
- The docstring says the input is "Treated as binary via `adjacency != 0`"
  ([clustering_rewire.py:63-64](src/nulls/clustering_rewire.py#L63-L64)). **The undirected
  path does not binarise**: it calls `nx.from_numpy_array(adjacency)` directly
  ([clustering_rewire.py:99](src/nulls/clustering_rewire.py#L99)). The *directed* path does
  binarise ([clustering_rewire.py:235](src/nulls/clustering_rewire.py#L235)). This is
  harmless here — the builder always passes an already-binary mask
  ([substrates.py:99](experiments/human/substrates.py#L99),
  [substrates.py:114-119](experiments/human/substrates.py#L114-L119)) — but the docstring
  overstates what the code guarantees, and a weighted input would flow through.
- The diagnostics dict returned by the **undirected** path carries `T_initial` / `T_final`
  and *not* `clustering_initial` / `clustering_final`
  ([clustering_rewire.py:177-184](src/nulls/clustering_rewire.py#L177-L184)); the builder
  reads those two keys with `.get(...)`
  ([substrates.py:255-256](experiments/human/substrates.py#L255-L256)), so they are
  recorded as `None` for every undirected cell. Only the directed path populates them
  ([clustering_rewire.py:400-401](src/nulls/clustering_rewire.py#L400-L401)).

**`validate_null` call.** `_record_clustering`
([substrates.py:244-259](experiments/human/substrates.py#L244-L259)) runs
`validate_null(base, mask, "clustering", tolerance=0.05)`, which is a relative difference in
`nx.transitivity` against 0.05 ([validation.py:111-120](src/nulls/validation.py#L111-L120)).
This is the **only** rung assertion that is not a pure tautology in form — but it re-tests
the generator's own acceptance criterion under a monotone re-expression, so it cannot fail
on a chain the generator produced, and it passes with zero accepted swaps. See §B.6.

---

### B.5 `modularity_rewire` — rung 4

Undirected path, [modularity_rewire.py:87-157](src/nulls/modularity_rewire.py#L87-L157).
Rung-2 double-edge swaps, accepted only when they leave the **block edge-count matrix** of
a fixed partition unchanged.

- The partition is **passed in, not detected per seed**: the builder computes one Louvain
  partition on `self.mask` at construction, `seed = LOUVAIN_SEED = 0`
  ([substrates.py:86-88](experiments/human/substrates.py#L86-L88)), and hands the same
  object to every call ([substrates.py:121-128](experiments/human/substrates.py#L121-L128)).
  The generator's fallback detection
  ([modularity_rewire.py:92-95](src/nulls/modularity_rewire.py#L92-L95)) is therefore never
  reached in this pipeline. The module docstring asks for exactly this discipline
  ([modularity_rewire.py:24-28](src/nulls/modularity_rewire.py#L24-L28)) and the builder
  follows it. Measured: **6 communities** at N = 448, sizes `[90, 88, 84, 81, 60, 45]`.
- Target swaps and attempt cap as rung 3 (`10 × n_edges`, `100 × target`)
  ([modularity_rewire.py:89-90](src/nulls/modularity_rewire.py#L89-L90)).
- **The acceptance rule is a single block test**, not rejection sampling on a statistic:
  `if node_to_block[v] != node_to_block[y]: continue`
  ([modularity_rewire.py:126-127](src/nulls/modularity_rewire.py#L126-L127)), on top of the
  four-distinct-endpoints and no-existing-edge tests
  ([modularity_rewire.py:122-125](src/nulls/modularity_rewire.py#L122-L125)). Endpoint
  orientations are randomised per draw
  ([modularity_rewire.py:116-120](src/nulls/modularity_rewire.py#L116-L120)) so all four
  endpoint matchings are sampled across draws
  ([modularity_rewire.py:8-14](src/nulls/modularity_rewire.py#L8-L14)).
- Accepted swaps therefore leave the multiset of (block, block) edge labels **identical**:
  `(b(u),b(v)),(b(x),b(y)) → (b(u),b(y)),(b(x),b(v))` is the same multiset when
  `b(v) == b(y)`.

| property | what happens |
|---|---|
| Node count | **N, exactly** |
| Edge count | **exactly preserved** |
| Density | **exactly the connectome's** |
| Weight multiset | **not preserved**; resampled with replacement from `empirical_pool` |
| Degree sequence | **exactly preserved, per node** |
| Symmetry | exact |
| Self-loops | none |
| Seeding | `np.random.default_rng(seed)` ([modularity_rewire.py:104](src/nulls/modularity_rewire.py#L104)) |

**What is preserved beyond rung 2: the intra-/inter-community edge counts of the fixed
partition — and therefore modularity `Q` exactly, not within a tolerance.** `Q` under a
fixed partition is a function of the intra-block edge counts and the per-block degree sums,
both invariant under an accepted swap. Measured at N = 448: `Q_initial == Q_final ==
0.5486175797563443` on **all ten seeds, to the last digit**. Measured acceptance rate
**10.3–10.4 %**, above the generator's 5 % warning floor
([modularity_rewire.py:139-147](src/nulls/modularity_rewire.py#L139-L147)).

**Docstring flags.**
- As with rung 3, the docstring says the input is "Treated as binary via `adjacency != 0`"
  ([modularity_rewire.py:54-55](src/nulls/modularity_rewire.py#L54-L55)) while the
  undirected path calls `nx.from_numpy_array(adjacency)` unbinarised
  ([modularity_rewire.py:87](src/nulls/modularity_rewire.py#L87)); the *directed* path does
  binarise ([modularity_rewire.py:186](src/nulls/modularity_rewire.py#L186)). Harmless
  here, since the builder passes a binary mask.
- `PROJECT_KNOWLEDGE_BASE.md:290-292` describes rung 4 in terms of the **directed** block
  edge-count matrix. The undirected path preserves the **undirected** block edge-count
  matrix by the same argument; the wording is directed-path-specific, not wrong.

**`validate_null` call — weaker than it looks.** `_record_modularity`
([substrates.py:260-271](experiments/human/substrates.py#L260-L271)) runs
`validate_null(base, mask, "modularity", tolerance=0.01, community_partition=self.partition)`,
an **absolute** difference in `nx.community.modularity` against 0.01
([validation.py:122-141](src/nulls/validation.py#L122-L141)). Since `Q` is preserved
*exactly* by the acceptance rule, the measured difference is 0 and a 0.01 band is never
approached. **This assertion has the same shape as the `degree_sequence` one**: it tests a
property the construction guarantees, and it passes with zero accepted swaps. See §B.6.

---

### B.6 What the `validate_null` calls actually test — and where they are weaker than they look

Four calls fire, one per rung (rung 0's recorder makes **no** call at all,
[substrates.py:219-225](experiments/human/substrates.py#L219-L225); the placement control
makes none either). All four are wrapped in `assert check["preserved"]`, so a failure stops
the run rather than warning — `validate_null` itself only prints
([validation.py:200-205](src/nulls/validation.py#L200-L205)).

| rung | call | what it compares | can it fail on a correctly-wired generator? |
|---|---|---|---|
| 1 `erdos_renyi` | `"edge_count"` ([substrates.py:227](experiments/human/substrates.py#L227)) | `int(original.sum())` vs `int(generated.sum())` — full-matrix sums, exact equality ([validation.py:60-64](src/nulls/validation.py#L60-L64)) | **No.** `gnm_random_graph(n, m)` returns exactly `m` edges by construction |
| 2 `degree_rewire` | `"degree_sequence"` ([substrates.py:235](experiments/human/substrates.py#L235)) | sorted row sums, exact equality ([validation.py:66-72](src/nulls/validation.py#L66-L72)) | **No.** Double-edge swaps preserve degree by construction after **any** number of swaps, **including zero** |
| 3 `clustering_rewire` | `"clustering"`, tol 0.05 ([substrates.py:245-246](experiments/human/substrates.py#L245-L246)) | relative diff in `nx.transitivity` ([validation.py:111-120](src/nulls/validation.py#L111-L120)) | **No.** With degree fixed, this is a monotone re-expression of the generator's own accept rule; passes with zero accepted swaps |
| 4 `modularity_rewire` | `"modularity"`, tol 0.01 ([substrates.py:261-262](experiments/human/substrates.py#L261-L262)) | absolute diff in `Q` under the fixed partition ([validation.py:122-141](src/nulls/validation.py#L122-L141)) | **No.** The block test makes `Q` **exactly** invariant; measured difference is 0.0 on every seed |

**The general shape.** Every one of the four checks a property the generator preserves *by
construction*, and **none is a convergence or mixing test.** Each would catch a wiring
error — the wrong generator called, a mask silently transposed or resized, a partition
mismatched to the graph — and that is a real function. None of them can tell you whether the
rewire chain actually explored anything. The `degree_sequence` case is the one already on
record (`report/act1_structure.md` §5 item 3); **the `modularity` case has exactly the same
shape and is not on record**, and the `clustering` case is the same shape once the
denominator invariance is noticed.

The one property genuinely worth a convergence test — how far the accepted chain has moved
from the input — is measured but **not asserted**: `acceptance_rate` is recorded into
`self.diagnostics` for rungs 3 and 4
([substrates.py:250-259](experiments/human/substrates.py#L250-L259),
[substrates.py:266-271](experiments/human/substrates.py#L266-L271)) and the generators warn
below 1 % / 5 %, but no threshold is asserted and edge-set retention is never computed.

### B.7 Rung 0, `random_gaussian`, for completeness

Not one of the four rungs the figures carry
(`report/figlib/sources.py:35` — `LADDER = ["connectome", "connectome_weight_permuted",
"degree_rewire", "erdos_renyi"]`), but it is in `matrix_config.VARIANTS` and it is the rung
that "matched density" correctly describes.

Each strict-upper-triangle pair is an independent Bernoulli draw at the input's undirected
density, then mirrored ([random_gaussian.py:44-50](src/nulls/random_gaussian.py#L44-L50)).
Node count exact; **edge count preserved only in expectation** (Binomial across seeds);
density matched **in expectation only**; degree sequence not preserved; symmetric; no
self-loops (`np.triu(..., k=1)`); seeded by `np.random.default_rng(seed)`
([random_gaussian.py:41](src/nulls/random_gaussian.py#L41)). Its recorder makes **no**
`validate_null` call and records `property="density_in_expectation", preserved=True`
unconditionally ([substrates.py:219-225](experiments/human/substrates.py#L219-L225)) — a
label, not a test.

---

## C. Cross-checks against the frozen artifacts

### C.0 What was done, and what was not

`HumanSubstrateBuilder` was instantiated at both scales and every ladder cell rebuilt **in
memory**, then compared to
`experiments/human/analysis/eigenspectrum/results/scale_{448,1000}/spectra_per_seed.parquet`.
The parquets were opened **read-only**. Nothing under `experiments/` or
`eigenspectrum/results/` was written; no parquet was regenerated; no experiment was run.
The rebuild path is exactly the one that produced the parquet —
`recurrent_spectrum(builder.weighted(condition, variant, seed))`
([spectra.py:139-155](experiments/human/analysis/manifold/spectra.py#L139-L155)) — so the
comparison is like for like.

### C.1 The parquets do not carry node count, edge count or density as columns

The 20 columns are `condition, variant, rung, seed, eig_w_real, eig_w_imag, is_symmetric,
perron_root, base_spectral_radius, bulk95_radius, spectral_gap, n_near_degenerate_10pct,
n_near_degenerate_25pct, top10_eigvec_ipr, bulk95, lambda_max_raw, outlier_bulk_gap,
lambda2_ratio, sr_crit, max_abs_imag`.

- **Node count is directly readable** as `len(eig_w_real)` — the tables driver reads it the
  same way ([tables.py:332](experiments/human/analysis/eigenspectrum/tables.py#L332)).
- **Edge count and density are not recorded anywhere in the parquet**, and cannot be
  recovered from a weighted spectrum. Under `human_empirical` the null weights are
  resampled from the empirical pool, so no spectral invariant returns `m`.

The check was therefore done in the only way it can be done: **rebuild the cell and prove
it is bit-identical to the frozen one**, then report the rebuilt cell's node/edge/density.
If the rebuild reproduces the frozen spectrum exactly, the frozen row *is* that graph, and
its structural counts transfer.

### C.2 Identity of the rebuild with the frozen rows

Compared per cell on `bulk95_radius`, `perron_root`, `spectral_gap`,
`base_spectral_radius`, and on the full stored eigenvalue array `eig_w_real`.

| scale | cells compared | max abs diff, four scalars | max abs diff, stored `eig_w_real` array |
|---|---|---|---|
| 448 | 70 (`condition == "human_empirical"`, all 7 variants × 10 seeds) | **≤ 1.4e-15** | **0.000e+00** (on the 40 rewire/ER cells, 448-long arrays) |
| 1000 | 70 (same) | **≤ 2.0e-15** | **0.000e+00** (on the 40 rewire/ER cells, 1000-long arrays) |

The scalar residuals are float64 round-off. The stored `float32` eigenvalue arrays were
compared element by element for the four rewire/ER rungs (40 cells per scale) and match
**bit for bit**; the other three variants were compared on the four scalars only. The
rebuild is the frozen artifact.

The four-rung figure ladder (`report/figlib/sources.py:35` —
`LADDER = ["connectome", "connectome_weight_permuted", "degree_rewire", "erdos_renyi"]`)
returns exactly **40 rows per scale** under
`condition == "human_empirical"`, 10 seeds each, as `report/FIGURE_LIST.md`'s F1 and S1
rows state. Node count is `448` on all 448-scale rows and `1000` on all 1000-scale rows —
including all 210 rows, not just the ladder's 40. `is_symmetric` is `True` and
`max |Im λ| = 0.0` on every row at both scales.

### C.3 Node count, edge count and density of every constructed substrate

Counted on the constructed matrix, not read from the parquet.

**N = 448** — connectome: **448 nodes, 5,323 undirected edges, density 0.0531620**

| variant | nodes | undirected edges | density | = connectome's? |
|---|---|---|---|---|
| `connectome` | 448 | 5,323 | 0.0531620 | — (reference) |
| `connectome_weight_permuted` | 448 | 5,323 | 0.0531620 | **exact** |
| `erdos_renyi` | 448 | 5,323 (all 10 seeds) | 0.0531620 | **exact** |
| `degree_rewire` | 448 | 5,323 (all 10 seeds) | 0.0531620 | **exact** |
| `clustering_rewire` | 448 | 5,323 (all 10 seeds) | 0.0531620 | **exact** |
| `modularity_rewire` | 448 | 5,323 (all 10 seeds) | 0.0531620 | **exact** |
| `random_gaussian` (rung 0, not in the figure ladder) | 448 | **5,180 – 5,439** across seeds | 0.0517 – 0.0543 | **approximate** |

**N = 1000** — connectome: **1,000 nodes, 10,784 undirected edges, density 0.0215896**

| variant | nodes | undirected edges | density | = connectome's? |
|---|---|---|---|---|
| `connectome` | 1000 | 10,784 | 0.0215896 | — (reference) |
| `connectome_weight_permuted` | 1000 | 10,784 | 0.0215896 | **exact** |
| `erdos_renyi` | 1000 | 10,784 (all 10 seeds) | 0.0215896 | **exact** |
| `degree_rewire` | 1000 | 10,784 (all 10 seeds) | 0.0215896 | **exact** |
| `clustering_rewire` | 1000 | 10,784 (all 10 seeds) | 0.0215896 | **exact** |
| `modularity_rewire` | 1000 | 10,784 (all 10 seeds) | 0.0215896 | **exact** |
| `random_gaussian` (rung 0, not in the figure ladder) | 1000 | **10,625 – 10,887** across seeds | 0.0213 – 0.0218 | **approximate** |

**Answer to the question as posed: no ladder rung's density departs from the connectome's.**
For all four figure-ladder rungs at both scales the match is **exact**, not approximate —
exact node count, exact edge count, exact density, at every one of the ten seeds. Extending
to the two further rungs the ladder carries in Act II (`clustering_rewire`,
`modularity_rewire`) leaves the answer unchanged: also exact.

**The single variant that is only approximate is `random_gaussian` (rung 0)**, and that is
by design — it is the density-in-expectation rung (§B.7). It is not in
`report/figlib`'s `LADDER` and not in the 40-row filter.

### C.4 Structural properties confirmed on every constructed cell

Checked on all 10 seeds of each of the four rewire/ER rungs at both scales (80 masks):

| property | result |
|---|---|
| Binary (`{0,1}`-valued) | true, every cell |
| Symmetric | `max|M − Mᵀ| = 0.0` exactly, every cell |
| Zero diagonal | 0 non-zero diagonal entries, every cell |
| Degree sequence vs connectome | **preserved exactly** for `degree_rewire`, `clustering_rewire`, `modularity_rewire`; **not preserved** for `erdos_renyi` — as each rung claims |
| Isolated nodes | 0 in the connectome at both scales (build metadata `n_isolated_nodes`); spot-checked 0 for `erdos_renyi` and `degree_rewire` at N = 448, seed 0. Not checked on every cell |

The consensus itself, read from the cache: `max|C − Cᵀ| = 0.0`, `min(C) = 0.0`, zero
non-zero diagonal entries, at both scales — §A.5's assertions hold on the cached artifact,
not only at build time.

### C.5 Generator diagnostics measured during the rebuild

Not results — properties of the construction, recorded because §B refers to them.

| | N = 448 | N = 1000 |
|---|---|---|
| Louvain communities (fixed, `seed = 0`) | **6**, sizes `[90, 88, 84, 81, 60, 45]` | **8**, sizes `[165, 163, 145, 127, 112, 102, 97, 89]` |
| `clustering_rewire` acceptance rate | 0.107 – 0.115 | 0.127 – 0.135 |
| `clustering_rewire` triangles `T_initial` | 17,120 | 28,534 |
| `clustering_rewire` relative triangle drift at exit | **4.99 %** (tolerance 5.00 %) | **4.98 – 5.00 %** (tolerance 5.00 %) |
| `modularity_rewire` acceptance rate | 0.103 – 0.104 | 0.095 – 0.096 |
| `modularity_rewire` `Q_initial` vs `Q_final` | `0.5486175797563443` → identical, all 10 seeds | `0.6226282315156425` → identical, all 10 seeds |
| Weight-permuted multiset vs connectome's | identical (sorted upper-triangle weights equal) | identical |
| Empirical pool size | 5,323 | 10,784 |

---

## D. What the code does not answer

Each item was looked for and not found. Nothing below is inferred, computed, or imported
from a document.

**D.1 What "fibre density" physically is.** The code names the modality — "dMRI structural
connectivity (streamline fibre density)"
([human_suarez.py:165](src/connectomes/human_suarez.py#L165)) — and asserts the values are
"normalized fractions, not integer counts"
([human_suarez.py:173](src/connectomes/human_suarez.py#L173)). It **never states what the
streamline count is normalised by.** Searched: all of `src/connectomes/`, the module and
function docstrings of `consensus.py` and `human_suarez.py`, all metadata dictionaries, and
`experiments/human/build_consensus.py`. *For the drafter:* the definition (streamline count
normalised by mean streamline length and by the mean surface area of the two regions) is
stated in `data/human/README.md` under "Edge-weight definition". It is **not** in the code
and is therefore not asserted here.

**D.2 The dMRI acquisition and tractography pipeline.** No sequence, no b-value, no
tractography algorithm, no seeding scheme, no subject demographics anywhere in the code.
The loader records only a citation string
([human_suarez.py:164](src/connectomes/human_suarez.py#L164)). This is upstream of the repo
and the repo does not restate it.

**D.3 Which 70 subjects, and the 70-vs-66 discrepancy.** The code reads 70 off the array
and flags in a comment that "the paper reports 66 (logged, not reconciled)"
([human_suarez.py:169](src/connectomes/human_suarez.py#L169)). **It does not say which
count the substrate should be described by, nor why they differ, nor whether any subject
was excluded.** The consensus uses **all 70** — `struct_consensus` takes `num_sub` from
`data.shape` ([consensus.py:81](src/connectomes/consensus.py#L81)) and no filtering happens
anywhere on the path. A chapter that writes "66 subjects" would be describing the paper,
not this build.

**D.4 The Cammoun parcel definition.** The code names the atlas
("Lausanne/Cammoun scale N=448", [human_suarez.py:166](src/connectomes/human_suarez.py#L166))
but there is no parcel list, no region labels, and no anatomical definition. Node labels are
explicitly placeholders: `f"{stem}{N}_region{i:04d}"`, with the comment "the data has no
labels" ([human_suarez.py:77-78](src/connectomes/human_suarez.py#L77-L78)).

**D.5 How the release's node ordering was verified against the `.mat`.** Two comments
assert node-order correspondence at `r ≥ 0.98`
([human_suarez.py:46-49](src/connectomes/human_suarez.py#L46-L49),
[human_suarez.py:193-195](src/connectomes/human_suarez.py#L193-L195)), but **no code in the
repository computes it.** Searched `src/connectomes/`, `experiments/human/build_consensus.py`
(whose `_validate` compares the self-built consensus to the *published consensus*, not the
orderings, [build_consensus.py:36-56](experiments/human/build_consensus.py#L36-L56)), and
`tests/test_smoke.py`. The claim is a recorded observation, not a reproducible check.

**D.6 Why the intra-hemispheric mask is written the way it is.** `keep_conn` for the
intra-hemispheric pass is `np.logical_or(right_hemi @ right_hemi.T, left_hemi @ left_hemi.T)`
([consensus.py:97-98](src/connectomes/consensus.py#L97-L98)) — an *extra* matrix product on
top of the outer products at [consensus.py:95-96](src/connectomes/consensus.py#L95-L96),
which the inter-hemispheric branch does not have
([consensus.py:92-93](src/connectomes/consensus.py#L92-L93)). Nothing in the code or its
docstrings explains the asymmetry. It is faithful to the vendored upstream
(`netneurotools.networks.struct_consensus`,
[consensus.py:1-9](src/connectomes/consensus.py#L1-L9)) and it is not reported here as a
defect — only as unexplained. **Not investigated further, because doing so would mean
re-running the build.**

**D.7 Whether the realised consensus edge count equals `avg_conn_num`.** The loop can skip
empty bins ([consensus.py:124-125](src/connectomes/consensus.py#L124-L125)) and the same
node pair can win in more than one bin, so the realised count may be **below** the target.
The code neither reports the target nor compares it to the realisation — no counter, no log
line, no metadata field. The realised counts are known (5,323 / 10,784); the targets are
not recorded anywhere, and computing them would require re-running the build.

**D.8 The number of length bins actually used.** Same reason: `avg_conn_num` is a local
([consensus.py:109-114](src/connectomes/consensus.py#L109-L114)), never returned, never
logged, and separately computed for the inter- and intra-hemispheric passes. The
inter/intra split of the final edge count is likewise not recorded.

**D.9 Whether any rewire chain has mixed.** No convergence, mixing, or edge-retention test
exists in `src/nulls/` or in `HumanSubstrateBuilder`. §B.6 sets out why none of the four
`validate_null` calls is one. `acceptance_rate` is recorded for rungs 3 and 4 only
([substrates.py:250-259](experiments/human/substrates.py#L250-L259),
[substrates.py:266-271](experiments/human/substrates.py#L266-L271)); rungs 1 and 2 record
no diagnostic beyond a boolean. Searched `src/nulls/*`, `experiments/human/substrates.py`,
`tests/test_smoke.py`.

**D.10 Why `n_swaps_multiplier = 10`.** `SWAP_MULTIPLIER = 10`
([matrix_config.py:108](experiments/human/matrix_config.py#L108)) carries no comment; the
generator's docstring says only "follows v1"
([degree_rewire.py:12-13](src/nulls/degree_rewire.py#L12-L13)). The justification is not in
the code.

**D.11 Why `CLUSTERING_TOLERANCE = 0.05` and the modularity tolerance `0.01`.** Neither
constant is justified anywhere. The 0.01 is not even a config constant — it is a literal
passed at the call site ([substrates.py:261](experiments/human/substrates.py#L261)), unlike
the clustering tolerance which comes from `matrix_config`
([matrix_config.py:106](experiments/human/matrix_config.py#L106)).

**D.12 Why `LOUVAIN_SEED = 0`, and how partition-dependent rung 4 is.** The seed is fixed
([matrix_config.py:107](experiments/human/matrix_config.py#L107)) and the partition is
computed once ([substrates.py:86-88](experiments/human/substrates.py#L86-L88)), which is the
right discipline and is what the generator's docstring asks for
([modularity_rewire.py:24-28](src/nulls/modularity_rewire.py#L24-L28)). **Nothing tests
sensitivity to that choice** — no alternative-seed sweep, no partition-stability check.

---

## E. Disagreements with the four named documents

Both statements are given with locations. **Nothing is resolved and neither side was
edited.**

### E.1 `report/CONVENTIONS.md` on which rungs appear where

| document | statement | location |
|---|---|---|
| `report/CONVENTIONS.md` | "**Three further rungs exist for exactly one figure.** `random_gaussian`, `clustering_rewire` and `modularity_rewire` appear only in `probe3_deff.parquet`, which feeds **F6 alone**" | `report/CONVENTIONS.md:79-81` |
| The frozen artifact | All three appear in `eigenspectrum/results/scale_448/spectra_per_seed.parquet` **and** `scale_1000/spectra_per_seed.parquet`: 210 rows each = 3 conditions × **7 variants** × 10 seeds, `human_empirical` alone carrying 70 rows over all seven variants | verified read-only, this report §C.2; the variant list is `matrix_config.VARIANTS` ([matrix_config.py:64-72](experiments/human/matrix_config.py#L64-L72)), passed through by `common.VARIANTS` and the tables driver ([common.py:41](experiments/human/analysis/eigenspectrum/common.py#L41), [tables.py:92-97](experiments/human/analysis/eigenspectrum/tables.py#L92-L97)) |

The two are reconcilable if `CONVENTIONS` is read as "appear in only one **figure**" rather
than "appear in only one **parquet**" — F1 and F2 do filter the seven down to
`LADDER`'s four (`report/figlib/sources.py:35`). But as written the sentence names a
parquet, and that sentence is false of the two `spectra_per_seed.parquet` files. Recorded,
not resolved.

### E.2 `report/act1_structure.md` on the scope of the "weaker than it looks" assertion

| document | statement | location |
|---|---|---|
| `report/act1_structure.md` | "the builder's assertion does not test it — `validate_null(..., "degree_sequence")` checks the sorted degree sequence, which double-edge swaps preserve *by construction* after any number of swaps, including zero" — stated of `degree_rewire` alone | `report/act1_structure.md:167-171` (§5 item 3) |
| This report, §B.6 | The same shape holds for **`modularity_rewire`** (`Q` is exactly invariant under the block-constrained swap, so `abs_diff = 0.0` on every seed and a 0.01 band is never approached) and for **`clustering_rewire`** (with degree fixed, transitivity's denominator is invariant, so the `validate_null` test is a monotone re-expression of the generator's own accept rule). All four rung assertions check a by-construction property | [substrates.py:226-271](experiments/human/substrates.py#L226-L271), [validation.py:60-141](src/nulls/validation.py#L60-L141), measured in §C.5 |

This is an **extension**, not a contradiction: A1 §5 item 3 is correct about
`degree_rewire` and says nothing about the other three. It is recorded here because a
chapter drafted from A1 alone would carry the caveat for one rung and imply the other three
are tested, which the code does not support.

### E.3 A number that is *not* a disagreement, recorded so it is not read as one

`report/facts/GAPS.md:32` states the **N = 1000** edge count as "10,784 undirected edges",
attributing it to `report/act1_structure.md:556` — which states it in passing, as the edge
count behind the `107,840` swap setting. This report reproduces **10,784** independently
from the build metadata and from a live rebuild (§A.6, §C.3). **The two agree exactly.**
Recorded because the number arrived here as a check on the reading rather than as an input,
and it passed.

**No disagreement was found with `TIER0_STATE_OF_PLAY.md` or `report/FIGURE_LIST.md`.**
Both were read for substrate and null-construction claims. `FIGURE_LIST`'s F1 and S1 rows
("filter `condition == "human_empirical"` and `variant in LADDER` (40 rows)",
`report/FIGURE_LIST.md:100`, `:167`) reproduce exactly (§C.2), and `FIGURE_LIST:114`'s
description of F15's substrate as "the N=448 self-built consensus … restricted to cortical
nodes" matches §A.3. `TIER0` makes no claim about how the consensus or any null is built —
which is precisely the gap this report fills.

---

## F. Proposed edits to `report/facts/GAPS.md` section A

**Written out, not applied.** Three of section A's open rows are resolved by this report.
Each replacement below is one line, in the existing "~~struck~~ **RESOLVED**" house style
that the 25 August 2026 rows already use, and preserves the row's second and third columns.

**Row at `report/facts/GAPS.md:32`** (the consensus build):

> | ~~**How the N = 448 consensus was built**~~ **RESOLVED 25 August 2026.** Extracted from source into **`report/METHODS_SUBSTRATE.md` §A**: **70 subjects** from `Individual_Connectomes.mat` (the code flags the paper's 66 as unreconciled), untransformed dMRI fibre-density weights (`WEIGHT_TRANSFORM = "raw"`), cortical-only Lausanne/Cammoun N = 448/1000 selected by cortical mask from the release's N = 463/1015 geometry, Betzel-2018 distance-dependent consensus with **one length bin per edge added** (the code's binning, not the paper's), edge chosen by most-subjects-expressed with mean weight as tie-break, weight assigned as the mean over **all** subjects, symmetrised and diagonal-zeroed, non-negativity asserted at `human_suarez.py:340` — giving **5,323 undirected edges, density 5.3162 % at N = 448** and 10,784 / 2.1590 % at N = 1000 | chapter 4 outline **item 2**, "The substrate and the null ladder" | T0 §0 to §6 in full; A1 in full; FL F1, F2, F15 rows and flags; SPINE; A2. **Now sourced from code, not documents** |

**Row at `report/facts/GAPS.md:33`** (`erdos_renyi`):

> | ~~**What `erdos_renyi` preserves.**~~ **RESOLVED 25 August 2026.** **`report/METHODS_SUBSTRATE.md` §B.2**: it is `nx.gnm_random_graph(n, m)` — a **`G(n, m)`** construction on `m` read off the connectome, so **N and the exact undirected edge count are preserved, and density exactly with them**; degree sequence and weight multiset are not (nulls resample the empirical pool **with replacement**). "Matched edge count" is the correct claim; "matched density" alone is the weaker `G(n, p)` claim and belongs to `random_gaussian` (rung 0), not to this rung | chapter 4 outline item 2, "the four rungs and what each holds fixed" | T0 (all); A1 (all, including §2.6's null-generation audit); FL; CONV; A2. **Now sourced from `src/nulls/erdos_renyi.py:34-38`** |

**Row at `report/facts/GAPS.md:34`** (`clustering_rewire` / `modularity_rewire`):

> | ~~**What `clustering_rewire` and `modularity_rewire` preserve.**~~ **RESOLVED 25 August 2026.** **`report/METHODS_SUBSTRATE.md` §B.4–§B.5**: both are degree-preserving double-edge-swap rewires (rung 2's move) with an added acceptance rule — rung 3 accepts only swaps keeping the **total triangle count within 5 % relative** (equivalently transitivity, the degree-fixed denominator being invariant; measured, the chain runs to **4.99 %**, i.e. to the edge of the band), rung 4 accepts only swaps with `block(v) == block(y)` under a **fixed Louvain partition** (`seed = 0`, 6 communities at N = 448 / 8 at N = 1000), which holds the block edge-count matrix and hence **`Q` exactly** — measured identical to the last digit on all 10 seeds. Both preserve N, exact edge count, exact density and the exact degree sequence; neither preserves the weight multiset | chapter 5 outline item 5, which quotes the seven-rung range | T0 §3.12; A2 §2.2; FL F6 row and flag; CONV. **Now sourced from `src/nulls/clustering_rewire.py` and `src/nulls/modularity_rewire.py`** |

---

*End. Nothing in this file was written to `TIER0_STATE_OF_PLAY.md`, `report/CONVENTIONS.md`,
`report/FIGURE_LIST.md`, `report/facts/GAPS.md`, any act file, or anything under
`report/figlib/`. No experiment was run and no parquet was regenerated.*
