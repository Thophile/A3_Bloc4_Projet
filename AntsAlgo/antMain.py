from graph import Graph
from AntsAlgo.const import RHO
from AntsAlgo.ants import Ant


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
    isok = False
    while not(isok):
        verif = 0
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
        firstant = ants[0]
        same = False
        for ant in ants:
            if firstant.visited != ant.visited:
                same = False
            else:
                same = True
        if same:
            verif += 1
        if verif >= 5:
            isok = True
    return ants[0].visited

    