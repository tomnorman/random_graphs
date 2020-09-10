import numpy as np
from itertools import chain, combinations
from collections import deque


######################### classes
class mat_graph:
    '''vertices- starts from zero'''
    def __init__(self,
            ):
        self.reset()
        self.mat = np.array([])

    def reset(self):
        self.cc = [] #connected component
        # for each cc
        self.ps = [] #powerset
        self.max_ind = [] #maximum independent set
        self.max_cliq = [] #maximum clique

    def add_vertex(self,
            x = 1
            ):
        self.reset()
        if self.mat.size == 0:
            self.mat = np.array([x])[:, None]
        else:
            # make matrix bigger
            self.mat = moar(self.mat)
            self.mat[-1,-1] = x
    
    def add_edge(self,
            ver1,
            ver2,
            w = 1
            ):
        self.reset()
        self.mat[ver1, ver2] = w
        self.mat[ver2, ver1] = w

    # connected components
    def ccs(self):
        if self.cc: return

        vertices_num = self.mat.shape[0]
        visited = np.full(vertices_num, False)
        self.ccs_num = 0
        self.cc = []
        for v in range(vertices_num):
            if not visited[v]:
                self.cc += [(bfs(self.mat, v, [v], visited))]

    # powersets of each cc
    def pss(self):
        self.ccs()
        if self.ps: return

        for cc in self.cc:
            self.ps += [list(powerset(cc))]


    def maxes(self,
            l, #list
            t
            ):
        self.pss()
        if l: return

        for ps in self.ps:
            l += [maxes(self.mat, ps, t)]


    def alpha(self,
            debug = False
            ):
        self.maxes(self.max_ind, 'i')
        if debug:   print(self.max_ind)
        max_ind_size = sum([len(ind) for ind in self.max_ind])
        return(max_ind_size)


    def omega(self,
            debug = False
            ):
        self.maxes(self.max_cliq, 'c')
        if debug:   print(self.max_cliq)
        max_cliq_size = max([len(cliq) for cliq in self.max_cliq])
        return(max_cliq_size)


    def __str__(self):
        print(self.mat)
        return('')
    def __repr__(self):
        return(self.__str__())


######################### functions
def bfs(mat,
        v, #current vertex- scalar
        d, #current connected component- list
        visited
        ):
    for j in neighbors(mat, v, visited):
        if not visited[j]:
            d += [j]
            bfs(mat, j, d, visited)
    return(d)


def neighbors(
        mat,
        v, #current vertex- scalar
        visited
        ):
    ns = []
    if not visited[v]:
        visited[v] = True
        for j, e in enumerate(mat[v,:]):
            if visited[j]:
                continue
            if e != 0:
                ns.append(j)
    return(ns)

def powerset(
        iterable
        ):
    "powerset([1,2,3]) --> (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1,len(s)+1))

def maxes(
        mat,
        ps, #powerset- list of tupels
        t #type of max- clique or independent
        ):
    ind = []
    for s in ps:
        sub_mat = mat[s,:][:,s]
        sub_mat[np.diag_indices_from(sub_mat)] = 1 if t == 'c' else 0
        condition = np.all(sub_mat) if t == 'c' else not np.any(sub_mat)

        if condition:
            if len(s) > len(ind):
                ind = s
    return(ind)
                



def moar(
        mat
        ):
    col = np.zeros(mat.shape[0])[:, None]
    row = np.zeros(mat.shape[0] + 1)[None, :]
    mat = np.hstack((mat, col))
    mat = np.vstack((mat, row))
    return(mat)

a=mat_graph()
a.add_vertex(10)
a.add_vertex(10)
a.add_vertex(1)
a.add_vertex(1)
a.add_vertex(3)
a.add_vertex(3)
a.add_vertex(3)
a.add_vertex(3)
a.add_vertex(3)
a.add_edge(2,3)
a.add_edge(2,8)
a.add_edge(8,7)
# cc
a.add_edge(0,1)
a.add_edge(0,8)
a.add_edge(0,6)
a.add_edge(0,5)
a.add_edge(1,8)
a.add_edge(1,5)
a.add_edge(1,6)
a.add_edge(6,8)
a.add_edge(6,5)
a.add_edge(8,5)

#import runpy; a=runpy.run_module("graph"); a['a']; a['a'].omega(True)
