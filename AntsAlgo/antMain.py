from graph import Graph
from AntsAlgo.const import RHO
from AntsAlgo.ants import Ant


def antAlgo(param, graph, tw, tour, iter, level):
    nb_fourmis = 10 # number of ants
    ants = list() # list of ants
    starting_node = 0 #  node from where the ants
    for i in range(nb_fourmis):
        ants.append(Ant())  
    phero = [] # the amount of pheromones in each node of the graph
    for i in range(len(graph) - 1):
        node = []
        for i in range(len(graph) - 1):
            node.append(10)
        phero.append(node)
    
    while True:
        verif = 0
        for ant in ants:
            ant.toVisit = tour
            ant.visited = [starting_node]
            ant.travel(graph, phero, tw, param)
        for i in range(len(phero)):         #Evaportaion
            for j in range(len(phero)):
                phero[i][j] = phero[i][j] * RHO
        for ant in ants :
            phero = ant.spittingPheromone(phero, graph, param)

        #print(verif,tour,ants[0].visited)

        same = True
        for ant in ants:
            if ants[0].visited != ant.visited:
                same = False
        if same:
            verif += 1
        else : verif = 0
        if verif >= 5:
            break
    return ants[0].visited

    