import vertex
import edge
import numpy as np
from collections import deque


######################### classes
class mat_graph:
    '''vertices- starts from zero'''
    def __init__(self,
            x
            ):
        self.mat = np.array([1])[:,None]
        self.vertices = [x]
        self.ccs_num = 1
        self.cc = [set([0])]

    def add_vertex(self,
            x
            ):
        self.vertices.append(x)
        # make matrix bigger
        self.mat = moar(self.mat)
        self.ccs_num = 0
    
    def add_edge(self,
            ver1,
            ver2,
            w
            ):
        self.mat[ver1, ver2] = w
        self.mat[ver2, ver1] = w
        self.ccs_num = 0

    def ccs(self):
        if not self.ccs_num:
            vertices_num = self.mat.shape[0]
            visited = [0 for _ in range(vertices_num)]
            self.ccs_num = 0
            self.cc = []
            for v in range(vertices_num):
                if not visited[v]:
                    self.ccs_num += 1
                    self.cc += [set(bfs(self.mat, v, [v], visited))]
        return({"ccs_num":self.ccs_num, "ccs":self.cc})

    def __str__(self):
        print(self.mat)
        return(str(self.vertices))
    def __repr__(self):
        return(self.__str__())


######################### functions
def bfs(mat, v, d, visited):
    ns = neighbors(mat, v, visited)
    d += ns
    for j in ns:
        bfs(mat, j, d, visited)
    return(d)


def neighbors(mat, v, visited):
    ns = []
    if not visited[v]:
        visited[v] = 1
        for n, e in enumerate(mat[v,:]):
            if visited[n]:
                continue
            if e > 0:
                ns.append(n)
    return(ns)


def moar(
        mat
        ):
    col = np.zeros(mat.shape[0])[:, None]
    row = np.zeros(mat.shape[0] + 1)[None, :]
    mat = np.hstack((mat, col))
    mat = np.vstack((mat, row))
    mat[-1, -1] = 1
    return(mat)

a=mat_graph(1)
a.add_vertex(1)
a.add_vertex(1)
a.add_vertex(1)
a.add_vertex(1)
a.add_edge(0,1,1)
a.add_edge(0,2,1)
a.add_edge(1,2,1)
#a.add_edge(1,4,1)
a.add_edge(3,4,1)

b=mat_graph(1)
b.add_vertex(1)
#import runpy; a=runpy.run_module("graph"); a['a']; a['bfs'](a['a'].mat,0,[0],[0 for _ in range(5)])
