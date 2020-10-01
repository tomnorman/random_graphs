import numpy as np

#type hinting
import typing

#powerset
from itertools import chain, combinations

def dot_str(mat: np.ndarray) -> str:
    # https://graphs.grevian.org/example
    n = mat.shape[0]
    s = "graph {\n"
    for i in range(n):
        for j in range(i + 1, n):
            if mat[i,j] != 0:
                w = f"\"{mat[i,j]}\""
                e = f"{i} -- {j}"
                s += f"{e}[label={w},weight={w}];\n"

    s += "}"
    return s


def degree(mat: np.ndarray, v: int) -> int:
    d = -1 #mat[v,v] != 0
    for i in range(mat.shape[0]):
        if mat[v,i] != 0:
            d += 1
    return d

def bfs(
    mat: np.ndarray,
    v: int,  # vertex
    cc: typing.List[int],  # connected component
    visited: typing.List[bool],
) -> typing.List[int]:
    for j in neighbors(mat, v, visited):
        if not visited[j]:
            cc.append(j)
            bfs(mat, j, cc, visited)
    return cc


def neighbors(
    mat: np.ndarray, v: int, visited: typing.List[bool]  # vertex
) -> typing.List[int]:
    ns = []
    if not visited[v]:
        visited[v] = True
        for j, e in enumerate(mat[v, :]):
            if (not visited[j]) and (e != 0):
                ns.append(j)
    return ns


def powerset(iterable: typing.Iterable[int]) -> typing.Iterator[typing.Tuple[int]]:
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))


def maxes(
    mat: np.ndarray,
    cc: typing.List[int],  # powerset
    t: str,  #'c'- clique, 'i'- independent
) -> typing.Tuple[int]:
    ans = (0,)
    for s in powerset(cc):
        sub_mat = mat[s, :][:, s]
        if t == "i":
            diag = 0
        elif t == "c":
            diag = 1
        # change the diagonal
        sub_mat[np.diag_indices_from(sub_mat)] = diag

        cond1 = (t == 'i' and not np.any(sub_mat))
        cond2 = (t == 'c' and np.all(sub_mat))

        if cond1 or cond2:
            if len(s) > len(ans):
                ans = s

    return ans


def maximal(a, b, c):
    return []


def chi(mat: np.ndarray, a: float = 0.19903) -> int:
    k = n = mat.shape[0]
    ps = powerset(range(n))
    for s in ps:
        sub_mat = mat[s, :][:, s]
        not_s = np.setdiff1d(np.arange(n), s)
        mat_not_s = mat[not_s, :][:, not_s]
        if (len(s) >= a * n) and (not np.any(sub_mat)):
            tmp = chi(mat_not_s, a)
            if k > 1 + tmp:
                k = 1 + tmp
        if (n - a * n) / 2 <= len(s) <= n / 2:
            tmp = chi(sub_mat, a) + chi(mat_not_s, a)
            if k > tmp:
                k = tmp
    return k


