from heuristichelper import *

DEBUG = False

# Local search version
def local_search(graph, tw, tour, iter, level_max):
    best_route = []
    for _ in range(iter):
        route = random_solution(tour)
        route = optimisation(graph, tw, route, level_max)
        routes = []
        if len(best_route) != 0 : routes.append(best_route) 
        routes.append(route)
        best_route =  best(graph, tw, routes)
        if (DEBUG) :
            print(" Iteration : "+str(_)+" ; Weight : "+str(get_weight(graph, tw, best_route))+ " ; Route : " + str(best_route))
    return best_route

def optimisation(graph, tw, route, level_max):
    nb = 50
    level = 1
    while level <= level_max:
        old = list.copy(route)
        #Generate neighboorhood
        neighbour = []
        neighbour.append(route)
        for _ in range(nb):
            neighbour.append(perturbation(route, level))

        route = best(graph, tw,neighbour)

        # if no change was made
        if old != route : 
            level = 1
        else: level += 1
        if DEBUG : print("Weight : "+str(get_weight(graph, tw, route)) + " Level : "+str(level))
    return route
def perturbation(route, level = 1):
    # local random n-shift
    r = list.copy(route)
    for _ in range (level):
        index_1 = random.randrange(len(r))
        index_2 = random.randrange(len(r))
        r[index_1], r[index_2] = r[index_2], r[index_1]
    return r