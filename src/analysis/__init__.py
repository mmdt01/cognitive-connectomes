"""Substrate analysis library (connectome-agnostic).

Tools for characterising a reservoir's recurrent matrix and topology directly --
independent of any prediction task. Each module operates on a plain weighted
adjacency matrix (or binary mask), so the same analyses apply to any connectome
and its nulls. The first module is ``spectral``; further topological analyses
(degree, clustering, motifs, modularity, reciprocity) slot in alongside it.
"""
