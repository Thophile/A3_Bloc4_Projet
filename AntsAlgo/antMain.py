from graph import Graph
from AntsAlgo.const import RHO
from AntsAlgo.ants import Ant
DEBUG = False

def antAlgo(param, graph, tw, tour, iter_max, level):
    nb_fourmis = 10 # number of ants
    ants = list() # list of ants
    starting_node = 0 #  node from where the ants
    for i in range(nb_fourmis):
        ants.append(Ant())  # instanciate ants
    phero = [] # the amount of pheromones in each node of the graph

    for i in range(len(graph)):
        node = []
        for i in range(len(graph)):
            node.append(10)
        phero.append(node)
    
    verif = 0 # counter of convergence
    it= 0 # number of iteration
    while True and it < 150: # iterate for 150 iterations
        it += 1
        for ant in ants: # initialize the ants
            ant.toVisit = list.copy(tour)
            ant.visited = [starting_node]
            ant.travel(graph, phero, tw, param) # start the travel of the ants

        for i in range(len(phero)):         #Evaportaion of the pheromones
            for j in range(len(phero)):
                phero[i][j] = phero[i][j] * RHO

        for ant in ants :
            phero = ant.spittingPheromone(phero, graph, param) # deposit of pheromones

        if DEBUG : print(verif,tour,ants[0].visited) # debug

        same = True
        for ant in ants: # check if all the ants have the same solution
            if ants[0].visited != ant.visited:
                same = False
        if same:
            verif += 1
        else : verif = 0
        if verif >= 3: # verif of the ants have the same solution for 3 times in a row
            break
    solution = list.copy(ants[0].visited) # get the solution (array of city)
    solution.pop(0)
    solution.pop(len(solution)-1)
    return solution

    