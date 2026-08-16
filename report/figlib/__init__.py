"""The shared figure module for the §4b front-to-back sweep.

Every figure in the thesis is produced here, from the frozen parquets, under the style
contract in ``report/CONVENTIONS.md``. No hand-tuned one-offs: when a number moves, the
whole set rebuilds.

    python -m report.figlib --verify          # do the sources exist, and what filters?
    python -m report.figlib --smoke           # render every figure on placeholder data
    python -m report.figlib --all             # render every figure on the frozen data
    python -m report.figlib --only F7 F12     # render a subset

Layout:

* ``style``   -- colours, fonts, panel labels, dpi, output paths. The contract.
* ``sources`` -- one loader per frozen artifact, each carrying its exact filter.
* ``figures`` -- a package: the registry in ``figures/__init__.py``, and the builders
  in one module per act, which is also **one module per sweep session**
  (``act1_structure``, ``act2_manifold``, ``act3_memory``, ``act3_prediction``,
  ``act4_anchor``). A session edits its own act module and nothing else. Split out of a
  single 1006-line module on 16 August 2026, verified byte-identical across all 16
  figures.
"""

from report.figlib import figures, sources, style

__all__ = ["figures", "sources", "style"]
