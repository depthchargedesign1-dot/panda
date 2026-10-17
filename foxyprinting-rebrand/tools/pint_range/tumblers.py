"""Matching whisky tumbler versions of the pint range designs (owner, 16 Oct 2026: "Yes make them" – the pairings).

Tumbler print area (owner, 8 Oct 2026): 50 x 50 mm, kept 10 mm below the rim, UV DTF, clear glass all round.
Each pint design is scaled (uniformly, about its own artwork bounds) to fit 46 x 46 mm in the middle of the
50 x 50 area. No prom tumbler: prom glasses are for school leavers, so no whisky glass for that range.
"""
import copy

import numpy as np

import designs as D

A = D.A
TW, TH = A.TUMBLER
FIT = 46.0


def bounds(els):
    """artwork bounds in mm from a raster of the pint design"""
    r = np.asarray(A.raster(els, D.W, D.H, pxmm=10, transparent=True))[..., 3]
    ys, xs = np.nonzero(r > 8)
    return xs.min() / 10, ys.min() / 10, (xs.max() + 1) / 10, (ys.max() + 1) / 10


def scale_els(els, s, dx, dy):
    out = []
    for e in copy.deepcopy(els):
        k = e["k"]
        if k == "clip":
            e["els"] = scale_els(e["els"], s, dx, dy)
        if "pts" in e:
            e["pts"] = [(x * s + dx, y * s + dy) for x, y in e["pts"]]
        for a in ("x", "x1", "x2"):
            if a in e:
                e[a] = e[a] * s + dx
        for a in ("y", "y1", "y2"):
            if a in e:
                e[a] = e[a] * s + dy
        for a in ("w", "h", "r", "rx", "ry", "size", "sp", "sw"):
            if a in e and e[a] is not None:
                e[a] = e[a] * s
        if e.get("dash"):
            e["dash"] = (e["dash"][0] * s, e["dash"][1] * s)
        out.append(e)
    return out


def to_tumbler(els):
    x0, y0, x1, y1 = bounds(els)
    s = min(FIT / (x1 - x0), FIT / (y1 - y0))
    dx = TW / 2 - (x0 + x1) / 2 * s
    dy = TH / 2 - (y0 + y1) / 2 * s
    return scale_els(els, s, dx, dy)


def min_pt(els):
    return min(e["size"] / 25.4 * 72 for e in els if e["k"] == "text")
