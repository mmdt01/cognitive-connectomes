"""Distance-dependent structural consensus (Betzel et al. 2018).

Vendored from ``netneurotools.networks.consensus`` (the ``struct_consensus`` +
``_ecdf`` pair) so the project does not depend on the whole netneurotools
library. Only the STRUCTURAL consensus is kept; the functional-consensus
bootstrap (``func_consensus``) is omitted -- FC is out of scope; re-add it if FC
becomes a readout target. The two ``sklearn.utils.validation`` helpers used
upstream are inlined so this module is numpy-only.

Reference: Betzel, R. F., Griffa, A., Hagmann, P., & Mišić, B. (2018).
Distance-dependent consensus thresholds for generating group-representative
structural brain networks. Network Neuroscience 2(1), 66-95.

This is the reference implementation for the Suárez 2021 group consensus (see
``data/human/README.md`` -> "Consensus construction" for the data provenance and
the verbatim paper procedure). Two conventions to keep in mind:
  * Binning follows the CODE (one length bin per edge to be added; within each
    bin the edge expressed in the most subjects is chosen, ties broken by mean
    weight) -- NOT the paper's ambiguous "sqrt(mean binary density) bins" wording.
  * ``weighted=True`` multiplies the binary consensus by ``data.mean(axis=2)``,
    i.e. the mean weight over ALL subjects (absent edge counts as 0), not the
    mean over only the subjects in which the edge is present.
It needs external Cammoun/Lausanne geometry (``distance`` from parcel centroids,
``hemiid`` hemisphere labels) that is NOT in Individual_Connectomes.mat. Verify
the output against Appendix A's targets: whole-brain density ~2.5%, symmetric,
non-negative, edge-length distribution tracking the group.
"""

import numpy as np


def _ecdf(data):
    """Empirical CDF of ``data``; returns ``(prob, quantiles)`` (upstream form)."""
    sample = np.atleast_1d(data)
    quantiles, counts = np.unique(sample, return_counts=True)
    prob = np.cumsum(counts).astype(float) / sample.size
    # prepend 0 to prob and the smallest quantile (match MATLAB / upstream)
    prob, quantiles = np.append([0], prob), np.append(quantiles[0], quantiles)
    return prob, quantiles


def struct_consensus(data, distance, hemiid, conn_num_inter=None,
                     conn_num_intra=None, weighted=False):
    """Distance-dependent group-consensus structural connectivity graph.

    Estimates the average edge-length distribution and builds a group matrix that
    approximates it, at the mean binary density across subjects, choosing per
    length bin the edge most consistently expressed across subjects (ties broken
    by mean weight). Runs separately on intra- and inter-hemispheric links.

    Parameters
    ----------
    data : (N, N, S) array_like
        Weighted per-subject connectivity (ideally continuous weights such as
        fibre density), ``N`` nodes x ``S`` subjects.
    distance : (N, N) array_like
        ``distance[i, j]`` = Euclidean distance between parcel centroids i, j.
    hemiid : (N, 1) array_like
        Hemisphere label per node (0 / 1; the two hemispheres, either assignment).
    conn_num_inter, conn_num_intra : int, optional
        Number of inter-/intra-hemispheric edges to include; estimated from the
        mean subject density when None.
    weighted : bool
        If True, return the mean-weighted consensus (binary mask * data.mean).

    Returns
    -------
    consensus : (N, N) numpy.ndarray
        Binary (default) or mean-weighted symmetric group connectivity matrix.
    """
    data = np.asarray(data)
    distance = np.asarray(distance)
    hemiid = np.asarray(hemiid)
    if not (len(data) == len(distance) == len(hemiid)):
        raise ValueError("data, distance and hemiid must share the same first "
                         "dimension (number of nodes).")
    if hemiid.ndim != 2:
        raise ValueError("hemiid must be a 2D (N, 1) array; reshape with "
                         "hemiid.reshape(-1, 1) and try again.")

    num_node, _, num_sub = data.shape        # info on connectivity matrices
    pos_data = data > 0                       # location of + values in matrix
    pos_data_count = pos_data.sum(axis=2)     # num sub with + values at each node

    with np.errstate(divide='ignore', invalid='ignore'):
        average_weights = data.sum(axis=2) / pos_data_count

    consensus = np.zeros((num_node, num_node, 2))

    for conn_type in range(2):  # 0 = inter-hemisphere, 1 = intra-hemisphere
        if conn_type == 0:
            inter_hemi = (hemiid == 0) @ (hemiid == 1).T
            keep_conn = np.logical_or(inter_hemi, inter_hemi.T)
        else:
            right_hemi = (hemiid == 0) @ (hemiid == 0).T
            left_hemi = (hemiid == 1) @ (hemiid == 1).T
            keep_conn = np.logical_or(right_hemi @ right_hemi.T,
                                      left_hemi @ left_hemi.T)

        # mask the distance array to only the edges of this connection type
        full_dist_conn = distance * keep_conn
        upper_dist_conn = np.atleast_3d(np.triu(full_dist_conn))

        # distance-weighted positive edges across subjects
        pos_dist = pos_data * upper_dist_conn
        pos_dist = pos_dist[np.nonzero(pos_dist)]

        # mean number of positive edges across subjects -> number of length bins
        if conn_type == 0:
            avg_conn_num = (len(pos_dist) / num_sub if conn_num_inter is None
                            else conn_num_inter)
        else:
            avg_conn_num = (len(pos_dist) / num_sub if conn_num_intra is None
                            else conn_num_intra)

        cumprob, quantiles = _ecdf(pos_dist)
        cumprob = np.round(cumprob * avg_conn_num).astype(int)

        group_conn_type = np.zeros((num_node, num_node))

        for n in range(1, int(avg_conn_num) + 1):  # one edge per length bin
            curr_quant = quantiles[np.logical_and(cumprob >= (n - 1),
                                                  cumprob < n)]
            if curr_quant.size == 0:
                continue
            mask = np.logical_and(full_dist_conn >= curr_quant.min(),
                                  full_dist_conn <= curr_quant.max())
            i, j = np.where(np.triu(mask))
            c = pos_data_count[i, j]   # num subjects expressing each edge
            w = average_weights[i, j]  # mean weight of each edge
            indmax = np.argwhere(c == c.max())
            if indmax.size == 1:
                group_conn_type[i[indmax], j[indmax]] = 1
            else:  # break ties by higher mean weight
                indmax = indmax[np.argmax(w[indmax])]
                group_conn_type[i[indmax], j[indmax]] = 1

        consensus[:, :, conn_type] = group_conn_type

    # collapse inter/intra and symmetrise
    consensus = consensus.sum(axis=2)
    consensus = np.logical_or(consensus, consensus.T).astype(int)

    if weighted:
        consensus = consensus * np.mean(data, axis=2)
    return consensus
