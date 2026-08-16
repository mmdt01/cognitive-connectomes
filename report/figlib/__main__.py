"""Entry point for the shared figure module.

    python -m report.figlib --verify          # source existence + the exact filters
    python -m report.figlib --smoke           # every figure on placeholder data
    python -m report.figlib --all             # every figure on the frozen data
    python -m report.figlib --only F7 F12     # a subset on the frozen data

``--smoke`` writes to ``report/figures/_smoke/`` so a placeholder render can never be
mistaken for a real one, and it needs no frozen artifact present. It is the check to run
before an act session starts: it proves every layout builds and that the palette has not
drifted from the committed task figures.
"""

import sys
import time
import traceback

from report.figlib import style
from report.figlib.figures import ALL_FIGURES, FIGURES, WORKSHOP
from report.figlib.sources import Context, verify


def _render(ids, placeholder: bool, subdir=None) -> int:
    context = Context(placeholder=placeholder)
    mode = "placeholder" if placeholder else "frozen"
    print(f"Rendering {len(ids)} figures on {mode} data -> "
          f"{(style.FIGURES_DIR / subdir) if subdir else style.FIGURES_DIR}\n")
    failures = 0
    for figure_id in ids:
        chapter, name, builder = ALL_FIGURES[figure_id]
        start = time.time()
        try:
            written = style.save(builder(context), figure_id, subdir=subdir)
            workshop = " [W]" if figure_id in WORKSHOP else ""
            label = f"ch{chapter}" if chapter else "appx"
            print(f"  {figure_id:4s} {label:4s} {name}{workshop}"
                  f"   {time.time() - start:.1f}s  -> {written[0].name}, {written[1].name}")
        except Exception:
            failures += 1
            print(f"  {figure_id:4s} {f'ch{chapter}' if chapter else 'appx':4s} "
                  f"{name}   FAILED")
            traceback.print_exc(limit=6)
    print(f"\n{len(ids) - failures}/{len(ids)} rendered"
          + (f", {failures} FAILED" if failures else ""))
    return failures


def _verify() -> int:
    report = verify()
    missing = report[~report.exists]
    print(f"{report.exists.sum()}/{len(report)} sources present\n")
    for row in report.itertuples():
        print(f"  [{'ok ' if row.exists else 'MISSING'}] {row.source:22s} {row.path}")
        print(f"          filter: {row.filter}")
    if len(missing):
        print(f"\n{len(missing)} MISSING: " + ", ".join(missing.source))
    return len(missing)


def main(argv) -> int:
    style.apply_rcparams()
    if "--verify" in argv:
        return _verify()

    style.check_colour_consistency()
    if "--smoke" in argv:
        return _render(list(ALL_FIGURES), placeholder=True, subdir="_smoke")
    if "--only" in argv:
        ids = [a for a in argv[argv.index("--only") + 1:] if not a.startswith("-")]
        unknown = [i for i in ids if i not in ALL_FIGURES]
        if unknown or not ids:
            print(f"unknown or empty figure ids: {unknown or '(none given)'}. "
                  f"Known: {', '.join(ALL_FIGURES)}")
            return 1
        return _render(ids, placeholder=False)
    if "--all" in argv:
        return _render(list(ALL_FIGURES), placeholder=False)
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
