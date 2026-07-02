# C. elegans connectome data

Source: Cook et al. (2019), *Whole-animal connectomes of both
Caenorhabditis elegans sexes*. Nature 571, 63–71.
DOI: 10.1038/s41586-019-1352-7

Downloaded from WormWiring: https://wormwiring.org/pages/adjacency.html
File: SI 5 Connectome adjacency matrices, corrected July 2020.

For v1 we use the hermaphrodite chemical synapse matrix, binarised
and symmetrised. Future versions will incorporate gap junctions,
weights, and direction.

## Neurotransmitter / sign table (`celegans_neurotransmitters.csv`)

Per-neuron-class transmitter annotation used to build the directed_empirical_dale Dale-sign
vector (the `asymmetric_empirical_signed` weight scheme). One row per
explicitly-classified neuron class; columns: `neuron_class`,
`neurotransmitter`, `category`, `sign`.

**Sign model (Dale's principle, one sign per presynaptic neuron):**
- **GABAergic → −1 (inhibitory).** The bona fide GABA-*synthesizing*
  classes (express `unc-25`/GAD and `unc-47`/VGAT): **DD, VD, RME, AVL,
  DVB, RIS** — the classical 26 GABAergic neurons (McIntire et al. 1993,
  *Nature* 364:337), confirmed by the neurotransmitter atlas below.
  GABA-*uptake-only* neurons (SMD, AVA, AVB, AVJ, ALA, AVF; anti-GABA⁺
  but `unc-25`⁻) clear GABA rather than release it and are **excluded**
  from the inhibitory set.
- **Everything else → +1 (excitatory).** Acetylcholine and glutamate
  (the majority) are treated as excitatory; under this binary fast-E/I
  model the ACh-vs-Glu distinction does not affect the sign, so it is not
  enumerated here. Monoaminergic classes (dopamine: ADE, CEP, PDE;
  serotonin: NSM, ADF, HSN; tyramine: RIM; octopamine: RIC) are listed
  for transparency as `modulatory` but signed +1. Unclassified neurons
  default to +1 (logged).

**Source.** Neurotransmitter identities from the *C. elegans*
neurotransmitter atlas: Wang et al. (2024), *A neurotransmitter atlas of
the nervous system of C. elegans males and hermaphrodites*, eLife
(reviewed preprint 95402, https://elifesciences.org/articles/95402),
which consolidates and updates Pereira et al. 2015 (ACh), Gendrel et al.
2016 (GABA), and Serrano-Saiz et al. 2017 (Glu). The GABA-synthesizing
set matches the classical McIntire et al. 1993 assignment.

Sign convention recorded for reviewers: this is a deliberate Dale-principle
simplification (one sign per neuron from its primary fast transmitter); it
does not capture receptor-dependent sign reversals (e.g. inhibitory
glutamate-gated chloride channels).
