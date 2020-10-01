import numpy as np

#type hinting
import typing

#c binding
#https://www.geeksforgeeks.org/how-to-call-a-c-function-in-python/
import ctypes
from numpy.ctypeslib import ndpointer

#functions
import utils as u

#viz
from graphviz import Source as gvS


class mat_graph:
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
    
    def draw(self, filename: str = "tmp", cleanup: bool=False):
        filename += ".gv"
        d = "graphs"
        G_str = u.dot_str(self.mat)
        src = gvS(G_str)
        src.view(filename, directory = d, cleanup=cleanup)
        
    def reset(self):
        self.cc = []  # connected component
        self.sub_mat = [] # sub matrix of cc
        self.max_ind = []  # maximum independent set
        self.max_cliq = []  # maximum clique
        self.ks = []

    def add_vertex(self, x: int = 1) -> None:
        self.reset()
        if self.mat.size == 0:
            self.mat = np.array([x])[:, None]
        else:
            # add one row and column
            col = np.zeros(self.mat.shape[0])[:, None]
            row = np.zeros(self.mat.shape[0] + 1)[None, :]
            self.mat = np.hstack((self.mat, col))
            self.mat = np.vstack((self.mat, row))
            self.mat[-1, -1] = x

    def add_edge(self, ver1: int, ver2: int, w=1) -> None:
        self.reset()
        self.mat[ver1, ver2] = w
        self.mat[ver2, ver1] = w

    def ccs(self):
        """ connected components """
        if not self.cc:
            vertices_num = self.mat.shape[0]
            visited = np.full(vertices_num, False)
            for v in range(vertices_num):
                if not visited[v]:
                    cc = u.bfs(self.mat, v, [v], visited)
                    self.cc += [cc]
                    self.sub_mat += [self.mat[cc,:][:,cc].copy(order='C')]

    def maxes(self, t: str, lang: str) -> None:
        self.ccs()

        if t == "i":
            l = self.max_ind
        elif t == "c":
            l = self.max_cliq

        if not l:
            for cc, sub_mat in zip(self.cc, self.sub_mat):
                if lang == 'p':
                    l += [u.maxes(self.mat, cc, t)]
                elif lang == 'c':
                    counter = self.lib.maxes(sub_mat, len(cc), t)
                    ps_bool = bin(counter)[2:].zfill(len(cc))[::-1]
                    ps_list = tuple(cc[i] for i, c in enumerate(ps_bool) if c == '1')
                    l += [ps_list]

    def alpha(self, lang: str = 'p') -> int:
        """ max independent sets """
        self.maxes('i', lang)
        max_ind_size = sum([len(ind) for ind in self.max_ind])
        return max_ind_size

    def omega(self, lang: str = 'p') -> int:
        """ max clique """
        self.maxes('c', lang)
        max_cliq_size = max([len(cliq) for cliq in self.max_cliq])
        return max_cliq_size

    def chi(self, a: float = 0.19903, lang: str = 'p') -> int:
        self.ccs()

        if not self.ks:
            for cc, sub_mat in zip(self.cc, self.sub_mat):
                if lang == 'p':
                    self.ks += [u.chi(sub_mat, a)]
                elif lang == 'c':
                    self.ks += [self.lib.chi(sub_mat, len(cc), a)]

        k = max(self.ks)
        return k

    def __str__(self):
        print(self.mat)
        if self.cc:
            print(self.cc)
        return ""

    def __repr__(self):
        return self.__str__()


