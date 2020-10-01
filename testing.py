import graph

#profiling
import timeit


a = graph.mat_graph()
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
a.ccs()
a.draw()

print(a)
print("p:")
print(a.alpha(lang='p'))
print(a.omega(lang='p'))
print(a.chi(lang='p'))
a.reset()
print("\nc:")
print(a.alpha(lang='c'))
print(a.omega(lang='c'))
print(a.chi(lang='c'))

n=10000
print("\np:",timeit.timeit(lambda: a.chi(lang = 'p'), number=n))
a.reset()
print("c:",timeit.timeit(lambda: a.chi(lang = 'c'), number=n))
a.reset()

# import runpy; a=runpy.run_module("graph"); a['a']; a['a'].omega(True)
