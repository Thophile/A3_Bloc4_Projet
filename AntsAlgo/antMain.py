from timeWindow import generate_Tw
from graph import Graph
from const import RHO
from ants import Ant
import pprint
#import numpy as np
#import matplotlib.pyplot as plt
import time

nb_fourmis = 10 # number of ants
ants = list() # list of ants
strating_node = 0 #  node from where the ants
iter = 5000 # number of interation (time)

n = 5000
has_traffic = True
is_complete = True
is_oriented = False

graph = [
    [0, 170, 130, 20, 180],
    [170, 0, 100, 230, 55],
    [130, 100, 0, 165, 125],
    [20, 230, 165, 0, 175],
    [180, 55, 125, 175, 0]]
"""
graph = [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
]# the grap which represent the map
"""

phero = [] # the amount of pheromones in each node of the graph
for i in range(n):
    node = []
    for i in range(n):
        node.append(10)
    phero.append(node)

#Generate the ants
for i in range(nb_fourmis):
    ants.append(Ant())

"""
pprint.pprint(phero)
A = np.array(graph)
G = nx.from_numpy_array(A)
G = nx.relabel_nodes(G, dic)
nx.draw(G, with_labels=True, font_size=8)
plt.show()
"""

toVisit = []
for i in range(1, n):
    toVisit.append(i)


tw = generate_Tw(n)
matrice = Graph(n, has_traffic, is_complete, is_oriented).matrice
print("Graph generated")
for _ in range(iter):
    print(_, "/", iter)
    for ant in ants:
        ant.toVisit = toVisit
        ant.visited = [strating_node]
        ant.travel(matrice, phero, tw)
    print("----------------------------------------------------")
    for i in range(len(phero)):         #Evaportaion
        for j in range(len(phero)):
            phero[i][j] = phero[i][j] * RHO
    for ant in ants :
        phero = ant.spittingPheromone(phero, matrice)

        