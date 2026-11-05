"""Find and verify a domino -> Schröder-path rule for Aztec diamond tilings."""
from itertools import product
from fractions import Fraction as Fr

def cells(n):
    return {(x, y) for x in range(-n, n) for y in range(-n, n) if abs(x + 0.5) + abs(y + 0.5) <= n}

def tilings(n):
    C = cells(n); out = []
    order = sorted(C, key=lambda c: (c[0], c[1]))
    def rec(cov, cur):
        free = next((c for c in order if c not in cov), None)
        if free is None:
            out.append(tuple(cur)); return
        x, y = free
        for o in ((x + 1, y), (x, y + 1)):
            if o in C and o not in cov:
                rec(cov | {free, o}, cur + [(free, o)])
    rec(frozenset(), []); return out

def seg(d, kind):
    (x, y), (x2, y2) = d
    if kind == "F":   # horizontal domino [x,x+2]x[y,y+1]
        return ((x, y + Fr(1, 2)), (x + 2, y + Fr(1, 2)))
    if kind == "U":   # vertical [x,x+1]x[y,y+2]
        return ((x, y + Fr(1, 2)), (x + 1, y + Fr(3, 2)))
    if kind == "D":
        return ((x, y + Fr(3, 2)), (x + 1, y + Fr(1, 2)))

def dtype(d):
    (x, y), (x2, y2) = d
    return ("H" if y2 == y else "V", (x + y) % 2)

def paths_from(t, rule):
    segs = []
    for d in t:
        k = rule[dtype(d)]
        if k: segs.append(seg(d, k))
    # build chains left -> right
    nxt = {}; starts = set(); ends = set()
    for a, b in segs:
        if a in nxt: return None
        nxt[a] = b
    pts_in = {b for a, b in segs}
    heads = [a for a in nxt if a not in pts_in]
    paths = []
    for h in heads:
        p = [h]
        while p[-1] in nxt: p.append(nxt[p[-1]])
        paths.append(tuple(p))
    # vertex-disjoint
    allpts = [q for p in paths for q in p]
    if len(allpts) != len(set(allpts)): return None
    return tuple(sorted(paths))

def check(n, rule):
    T = tilings(n); fams = set()
    for t in T:
        f = paths_from(t, rule)
        if f is None or len(f) != n: return None
        fams.add(f)
    return len(T), len(fams)

kinds_H = [None, "F"]; kinds_V = [None, "U", "D"]
for h0, h1, v0, v1 in product(kinds_H, kinds_H, kinds_V, kinds_V):
    rule = {("H", 0): h0, ("H", 1): h1, ("V", 0): v0, ("V", 1): v1}
    ok = True; res = []
    for n in (1, 2, 3):
        r = check(n, rule)
        if r is None or r[0] != r[1]: ok = False; break
        res.append(r)
    if ok:
        print("VALID", rule, res)

# ---- LGV side: path counts between endpoints, inside the region the paths use
import numpy as np
RULE = {("H", 0): "F", ("H", 1): None, ("V", 0): "U", ("V", 1): "D"}
for n in (1, 2, 3, 4):
    T = tilings(n) if n <= 3 else None
    fams = [paths_from(t, RULE) for t in T] if T else None
    if n <= 3:
        starts = sorted({p[0] for f in fams for p in f}); ends = sorted({p[-1] for f in fams for p in f})
        pts = {q for f in fams for p in f for q in p}
    # region: lattice points (x integer, y half-integer) strictly inside the diamond
    Cn = cells(n)
    region = {(x, y + Fr(1, 2)) for x in range(-n, n + 1) for y in range(-n, n)
              if (x - 1, y) in Cn or (x, y) in Cn}
    S = sorted([(-n + i, Fr(1, 2) - i) for i in range(n)][::-1]) if n > 3 else starts
    if n <= 3:
        assert pts <= region, "paths leave region"
    E = [(-x, y) for (x, y) in S]          # mirror image on the right
    def count(a, b):
        memo = {}
        def f(p):
            if p == b: return 1
            if p in memo: return memo[p]
            x, y = p; tot = 0
            for q in ((x + 1, y + 1), (x + 1, y - 1), (x + 2, y)):
                if q in region and q[0] <= b[0]:
                    tot += f(q)
            memo[p] = tot; return tot
        return f(a)
    M = [[count(a, b) for b in E] for a in S]
    d = round(np.linalg.det(np.array(M, float)))
    msg = f"n={n}: starts {[(x, str(y)) for x, y in S]}  det={d}  2^(n(n+1)/2)={2 ** (n * (n + 1) // 2)}"
    if n <= 3:
        # all non-touching families in the region between these endpoints
        from itertools import product as P
        def allp(a, b):
            out = []
            def rec(cur):
                if cur[-1] == b: out.append(tuple(cur)); return
                x, y = cur[-1]
                for q in ((x + 1, y + 1), (x + 1, y - 1), (x + 2, y)):
                    if q in region and q[0] <= b[0]: rec(cur + [q])
            rec([a]); return out
        fam_all = [f for f in P(*[allp(S[i], E[i]) for i in range(n)])
                   if len({q for p in f for q in p}) == sum(len(p) for p in f)]
        msg += f"  non-touching families={len(fam_all)}  from tilings={len(set(fams))}  same set={set(map(lambda f: tuple(sorted(f)), fam_all)) == set(fams)}"
        msg += f"  matrix={M}"
    print(msg)
