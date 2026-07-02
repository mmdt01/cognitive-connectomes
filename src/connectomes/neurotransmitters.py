"""Per-neuron Dale sign vector for the ``directed_empirical_dale`` (``asymmetric_empirical_signed``) scheme.

Maps each *C. elegans* cell label to its neuron class, looks the class up in
the curated neurotransmitter table (``data/celegans/celegans_neurotransmitters.csv``),
and returns a length-N vector of signs (+1 excitatory / -1 inhibitory) aligned
to ``node_labels``.

Sign model (Dale's principle; see ``data/celegans/README.md`` for provenance):
GABA-synthesizing neurons (DD, VD, RME, AVL, DVB, RIS) are inhibitory (-1);
every other neuron — acetylcholine, glutamate, monoamine, or unclassified — is
excitatory (+1). The table lists the GABAergic and monoaminergic classes
explicitly; any class not in the table defaults to +1 (``unknown_sign``).
"""

from pathlib import Path

import numpy as np
import pandas as pd

_REPO_ROOT = Path(__file__).resolve().parents[2]
_TABLE_PATH = _REPO_ROOT / "data" / "celegans" / "celegans_neurotransmitters.csv"

# Suffixes that turn a neuron-class name into a cell name: positional labels
# (left/right, dorsal/ventral and their combinations) or a member number.
_POSITIONAL_SUFFIXES = {"L", "R", "D", "V", "DL", "DR", "VL", "VR"}


def _cell_in_class(cell: str, neuron_class: str) -> bool:
    """True if cell label ``cell`` belongs to neuron class ``neuron_class``.

    A cell belongs to a class if it is the class name itself (singletons such
    as ``AVL``), the class name plus a positional suffix (``RME`` -> ``RMED``;
    ``ADF`` -> ``ADFL``), or the class name plus a member number (``DD`` ->
    ``DD01``; ``VD`` -> ``VD13``).
    """
    if cell == neuron_class:
        return True
    if not cell.startswith(neuron_class):
        return False
    suffix = cell[len(neuron_class):]
    return suffix in _POSITIONAL_SUFFIXES or suffix.isdigit()


def load_neuron_signs(
    node_labels: list[str],
    table_path: Path | str | None = None,
    unknown_sign: int = 1,
) -> tuple[np.ndarray, dict]:
    """Build the per-neuron sign vector aligned to ``node_labels``.

    Parameters
    ----------
    node_labels
        The connectome's cell labels, in node order. The returned sign vector
        has the same length and order, so it can be passed straight to
        ``apply_weight_scheme(..., scheme="asymmetric_empirical_signed",
        neuron_signs=signs)`` for the connectome and (unchanged) for its nulls.
    table_path
        Override for the neurotransmitter CSV; defaults to
        ``data/celegans/celegans_neurotransmitters.csv``.
    unknown_sign
        Sign for any cell whose class is not listed in the table (+1 by the
        Dale excitatory-default policy).

    Returns
    -------
    (signs, coverage)
        ``signs`` is a float array of shape ``(N,)`` with entries in {-1, +1}.
        ``coverage`` is a dict logging the assignment (per-category counts,
        the inhibitory cell labels, the default-excitatory count, and the
        unknown policy) for the experiment audit trail.
    """
    table_path = Path(table_path) if table_path is not None else _TABLE_PATH
    table = pd.read_csv(table_path)

    classes = list(table["neuron_class"])
    class_sign = dict(zip(table["neuron_class"], table["sign"].astype(int)))
    class_category = dict(zip(table["neuron_class"], table["category"]))
    class_nt = dict(zip(table["neuron_class"], table["neurotransmitter"]))

    signs = np.full(len(node_labels), float(unknown_sign))
    inhibitory_labels: list[str] = []
    modulatory_labels: list[str] = []
    matched_class_counts: dict[str, int] = {}
    nt_counts: dict[str, int] = {}
    n_default = 0

    for index, cell in enumerate(node_labels):
        matches = [c for c in classes if _cell_in_class(cell, c)]
        if len(matches) > 1:
            raise ValueError(
                f"cell {cell!r} matches multiple table classes {matches!r}; "
                "the neurotransmitter table is ambiguous."
            )
        if not matches:
            n_default += 1
            nt_counts["acetylcholine/glutamate (default)"] = (
                nt_counts.get("acetylcholine/glutamate (default)", 0) + 1
            )
            continue

        neuron_class = matches[0]
        signs[index] = float(class_sign[neuron_class])
        matched_class_counts[neuron_class] = matched_class_counts.get(neuron_class, 0) + 1
        nt_counts[class_nt[neuron_class]] = nt_counts.get(class_nt[neuron_class], 0) + 1
        if class_category[neuron_class] == "inhibitory":
            inhibitory_labels.append(cell)
        elif class_category[neuron_class] == "modulatory":
            modulatory_labels.append(cell)

    coverage = {
        "n_nodes": len(node_labels),
        "n_excitatory": int((signs > 0).sum()),
        "n_inhibitory": int((signs < 0).sum()),
        "inhibitory_labels": inhibitory_labels,
        "modulatory_labels": modulatory_labels,
        "matched_class_counts": matched_class_counts,
        "neurotransmitter_counts": nt_counts,
        "default_excitatory_count": n_default,
        "unknown_sign": unknown_sign,
        "table_path": str(table_path),
    }
    return signs, coverage
