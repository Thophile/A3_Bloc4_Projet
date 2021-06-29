from graph import Graph
from const import RHO
from ants import Ant


def antAlgo(param, graph, tw, tour, iter, level):
    nb_fourmis = 10 # number of ants
    ants = list() # list of ants
    strating_node = 0 #  node from where the ants
    for i in range(nb_fourmis):
        ants.append(Ant())  
    phero = [] # the amount of pheromones in each node of the graph
    for i in range(len(graph) - 1):
        node = []
        for i in range(len(graph) - 1):
            node.append(10)
        phero.append(node)
    toVisit = []
    for i in range(1, len(graph) - 1):
        toVisit.append(i)
    for _ in range(iter):
        print(_, "/", iter)
        for ant in ants:
            ant.toVisit = tour
            ant.visited = [strating_node]
            ant.travel(graph, phero, tw)
        print("----------------------------------------------------")
        for i in range(len(phero)):         #Evaportaion
            for j in range(len(phero)):
                phero[i][j] = phero[i][j] * RHO
        for ant in ants :
            phero = ant.spittingPheromone(phero, graph)
    sol = [0]
    for i in range((len(phero) - 1)):
        sol.apprend(i.indexof(max(i)))
    return sol