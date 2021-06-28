from heuristichelper import *

DEBUG = False

# Local search version
def ants(params, graph, tw, tour, iter, level_max):
    best_route = []
    
    if (DEBUG) :
        print(" Iteration : "+str(_)+" ; Weight : "+str(get_weight(params, graph, tw, best_route))+ " ; Route : " + str(best_route))
    return best_route