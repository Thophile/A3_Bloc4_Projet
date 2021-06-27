from const import RHO
from ants import Ant
import pprint
#import numpy as np
#import matplotlib.pyplot as plt
import time

nb_fourmis = 10 # number of ants
ants = list() # list of ants
strating_node = 0 #  node from where the ants
iter = 0 # number of interation (time)

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
dic = {
    0:"0",
    1:"1",
    2:"2",
    3:"3",
    4:"4",
    5:"5",
    6:"6",
    7:"7",
    8:"8",
    9:"9",
    10:"10",
    11:"11",
    12:"12",
    13:"13"
}

phero = [] # the amount of pheromones in each node of the graph
for i in range(len(graph)):
    node = []
    for i in range(len(graph)):
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
toVisit = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

for _ in range(50000):

    for ant in ants:
        ant.toVisit = [1, 2, 3, 4]
        ant.visited = [0]
        ant.travel(graph, phero)
        #time.sleep(2)
    print("----------------------------------------------------")
    for i in range(len(phero)):         #Evaportaion
        for j in range(len(phero)):
            phero[i][j] = phero[i][j] * RHO
    for ant in ants :
        phero = ant.spittingPheromone(phero, graph)
    print (phero)
        