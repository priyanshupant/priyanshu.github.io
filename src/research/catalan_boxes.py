import numpy as np
from math import comb
from itertools import product

def dyck(a, b):                       # paths (x,y)->(b,0) with steps (1,±1), y >= 0
    out = []
    def rec(cur):
        x, y = cur[-1]
        if x == b[0]:
            if y == 0: out.append(tuple(cur))
            return
        for dy in (1, -1):
            if y + dy >= 0 and abs(y + dy) <= b[0] - x - 1: rec(cur + [(x + 1, y + dy)])
    rec([a]); return out

cat = lambda m: comb(2 * m, m) // (m + 1)
for n, shift in ((2, 2), (3, 2), (2, 1), (3, 1)):
    S = [(-2 * i, 0) for i in range(n)]
    E = [(2 * shift + 2 * j, 0) for j in range(n)]
    M = [[len(dyck(s, e)) for e in E] for s in S]
    fams = [f for f in product(*[dyck(S[i], E[i]) for i in range(n)])
            if len({q for p in f for q in p}) == sum(len(p) for p in f)]
    print(f"n={n} shift={shift} M={M} det={round(np.linalg.det(np.array(M, float)))} families={len(fams)}",
          "catalan check:", [[cat(i + j + shift) for j in range(n)] for i in range(n)] == M)

a = b = c = 3
M = [[comb(a + b, a + z - zz) for zz in range(c)] for z in range(c)]
mac = 1
for i in range(1, a + 1):
    for j in range(1, b + 1):
        for k in range(1, c + 1):
            mac = mac * (i + j + k - 1) / (i + j + k - 2)
print("box 3x3x3:", M, "det", round(np.linalg.det(np.array(M, float))), "MacMahon", round(mac))
