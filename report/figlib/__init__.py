"""The shared figure module for the §4b front-to-back sweep.

Every figure in the thesis is produced here, from the frozen parquets, under the style
contract in ``report/CONVENTIONS.md``. No hand-tuned one-offs: when a number moves, the
whole set rebuilds.

    python -m report.figlib --verify          # do the sources exist, and what filters?
    python -m report.figlib --smoke           # render all 14 on placeholder data
    python -m report.figlib --all             # render all 14 on the frozen data
    python -m report.figlib --only F7 F12     # render a subset

Layout:

* ``style``   -- colours, fonts, panel labels, dpi, output paths. The contract.
* ``sources`` -- one loader per frozen artifact, each carrying its exact filter.
* ``figures`` -- one builder per entry on ``report/FIGURE_LIST.md``.
"""

from report.figlib import figures, sources, style

__all__ = ["figures", "sources", "style"]
