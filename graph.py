import numpy as np

#profiling
import timeit

#type hinting
import typing

#powerset
from itertools import chain, combinations

#c binding
#https://www.geeksforgeeks.org/how-to-call-a-c-function-in-python/
import ctypes
from numpy.ctypeslib import ndpointer


######################### classes
class mat_graph:
    """vertices- starts from zero"""

    def __init__(self):
        self.reset()
        self.mat = np.array([])
        self.lib = ctypes.cdll.LoadLibrary("./libnp.so")
        self.lib.maxes.restype = ctypes.c_uint
        self.lib.maxes.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                ctypes.c_uint,
                ctypes.c_wchar]
        self.lib.chi.restype = ctypes.c_uint
        self.lib.chi.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                ctypes.c_uint,
                ctypes.c_float]


    def reset(self):
        self.cc = []  # connected component
        self.sub_mat = [] # sub matrix of cc
        self.ps = []  # powerset
        self.max_ind = []  # maximum independent set
        self.max_cliq = []  # maximum clique
        self.ks = []

    def add_vertex(self, x: int = 1) -> None:
        self.reset()
        if self.mat.size == 0:
            self.mat = np.array([x])[:, None]
        else:
            # add one row and column
            self.mat = moar(self.mat)
            self.mat[-1, -1] = x

    def add_edge(self, ver1: int, ver2: int, w=1) -> None:
        self.reset()
        self.mat[ver1, ver2] = w
        self.mat[ver2, ver1] = w

    def ccs(self, debug: bool = False):
        """ connected components """
        if self.cc:
            return

        vertices_num = self.mat.shape[0]
        visited = np.full(vertices_num, False)
        for v in range(vertices_num):
            if not visited[v]:
                cc = bfs(self.mat, v, [v], visited)
                self.cc += [cc]
                self.sub_mat += [self.mat[cc,:][:,cc].copy(order='C')]
        if debug:
            print(self.cc)

    def maxes(self, t: str, lang: str, debug: bool) -> None:
        self.ccs()

        if t == "i":
            l = self.max_ind
        elif t == "c":
            l = self.max_cliq

        if l:
            return

        for cc, sub_mat in zip(self.cc, self.sub_mat):
            if lang == 'p':
                l += [maxes(self.mat, cc, t)]
            elif lang == 'c':
                counter = self.lib.maxes(sub_mat, len(cc), t)
                ps_bool = bin(counter)[2:].zfill(len(cc))[::-1]
                ps_list = tuple(cc[i] for i, c in enumerate(ps_bool) if c == '1')
                l += [ps_list]

        if debug:
            print(l)

    def alpha(self, lang: str = 'p', debug: bool =False) -> int:
        """ max independent sets """
        self.maxes('i', lang, debug)
        max_ind_size = sum([len(ind) for ind in self.max_ind])
        return max_ind_size

    def omega(self, lang: str = 'p', debug: bool =False) -> int:
        """ max clique """
        self.maxes('c', lang, debug)
        max_cliq_size = max([len(cliq) for cliq in self.max_cliq])
        return max_cliq_size

    def chi(self, a: float = 0.19903, lang: str = 'p', debug: bool =False) -> int:
        self.ccs()

        if self.ks:
            return

        for cc, sub_mat in zip(self.cc, self.sub_mat):
            if lang == 'p':
                self.ks += [chi(sub_mat, a)]
            elif lang == 'c':
                self.ks += [self.lib.chi(sub_mat, len(cc), a)]

        if debug:
            print(self.ks)

        k = max(self.ks)
        return k

    def __str__(self):
        print(self.mat)
        return ""

    def __repr__(self):
        return self.__str__()


######################### functions
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


def powerset(iterable: list) -> typing.List[typing.Tuple[int]]:
    "powerset([1,2,3]) --> (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1)))


def maxes(
    mat: np.ndarray,
    cc: typing.List[int],  # powerset
    t: str,  #'c'- clique, 'i'- independent
) -> tuple:
    ans = []
    for s in powerset(cc):
        sub_mat = mat[s, :][:, s]
        if t == "i":
            diag = 0
        elif t == "c":
            diag = 1
        # change the diagonal
        sub_mat[np.diag_indices_from(sub_mat)] = diag

        if t == "i":
            condition = not np.any(sub_mat)
        elif t == "c":
            condition = np.all(sub_mat)

        if condition:
            if len(s) > len(ans):
                ans = s

    return ans


def lawler(mat: np.ndarray, ps: typing.List[typing.Tuple]) -> int:  # powerset
    n = mat.shape[0]
    X = np.zeros(2 ** n)

    def f(s: tuple) -> int:
        return sum([2 ** i for i in s]) - 1

    for S in ps:
        s = f(S)
        X[s] = float("inf")
        mat_S = mat[S, :][:, S]
        ps_S = powerset(S)
        for I in maximal(mat_S, ps_S, "i"):
            S_wo_I = list(set(S) - set(I))
            i = f(S_wo_I)
            if X[i] + 1 < X[s]:
                X[s] = X[i] + 1
    return X[-1]


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


def moar(mat):
    col = np.zeros(mat.shape[0])[:, None]
    row = np.zeros(mat.shape[0] + 1)[None, :]
    mat = np.hstack((mat, col))
    mat = np.vstack((mat, row))
    return mat


a = mat_graph()
a.add_vertex(10)
a.add_vertex(10)
a.add_vertex(1)
a.add_vertex(1)
a.add_vertex(3)
a.add_vertex(3)
a.add_vertex(3)
a.add_vertex(3)
a.add_vertex(3)
#a.add_edge(2, 3)
a.add_edge(2, 8)
a.add_edge(4, 7)
# clique
a.add_edge(0, 1)
a.add_edge(0, 8)
a.add_edge(0, 6)
a.add_edge(0, 5)
a.add_edge(1, 8)
a.add_edge(1, 5)
a.add_edge(1, 6)
a.add_edge(5, 8)
a.add_edge(5, 6)
a.add_edge(6, 8)
print("p:",timeit.timeit(lambda: a.alpha(lang = 'p', debug = True), number=1000))
print("p:",timeit.timeit(lambda: a.chi(lang = 'p', debug = True), number=1000))
a.reset()
print("c:",timeit.timeit(lambda: a.alpha(lang = 'c', debug = True), number=1000))
print("c:",timeit.timeit(lambda: a.chi(lang = 'c', debug = True), number=1000))
a.reset()


# import runpy; a=runpy.run_module("graph"); a['a']; a['a'].omega(True)
