"""Cap BLAS threads to avoid oversubscription on small matrices.

The default OpenBLAS configuration spawns one thread per core. For
N=300 reservoirs the per-call overhead dominates, and the experiment
loop runs ~30× slower than it should. Setting a low limit fixes this
(v1 saw 10+ min → 66 s).

Import this module once at the top of a notebook for the side effect:

    from src.reservoir import blas  # noqa: F401

Implementation note: ``threadpool_limits`` only constrains BLAS
libraries that are *already loaded*. We import numpy first to force
OpenBLAS to load, then apply the limit. Without this, importing this
module before numpy is a no-op and the loop runs ~15× slower.
"""

import numpy as _np  # noqa: F401 — force-load BLAS

from threadpoolctl import threadpool_limits

threadpool_limits(limits=2)
