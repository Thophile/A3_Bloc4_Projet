from pymongo import MongoClient
import pprint
import random


# Connection to MongoDB
client = MongoClient('localhost', 27017)
db = client['DataProject']
graphs = db['graphs']

graph = []
tw = []

DEBUG = False
VERBOSE = True

# Handler method
def heuristic(graph_id, iter, level):
    global graph, tw
    graph = [i["row"] for i in graphs.find({"graph_id" : graph_id})]
    tw = [{"start_time" : i["start_time"], "end_time" : i["end_time"]} for i in graphs.find({"graph_id" : graph_id})]
    if DEBUG : print("Graph loaded")
    
    return local_search(iter,level)

# Local search version
def local_search(iter,level_max):
    best_route = []
    for _ in range(iter):
        route = random_solution()
        route = optimisation(route, level_max)
        best_route =  better(best_route, route)
        if (VERBOSE) :
            print(" Iteration : "+str(_)+" ; Weight : "+str(get_weight(best_route))+ " ; Route : " + str(best_route))
    return best_route
def optimisation(route,level_max):
    level = 1
    while level <= level_max:
        #random n-swap
        route_2 = perturbation(route, level)
        route = better(route,route_2)
        if route == route_2 : 
            level = 1
            if DEBUG : print("Weight : "+str(get_weight(route)) + "Level : "+str(level))
        else: level += 1
    return route
def perturbation(route, level = 1):
    # local random n-shift
    r = list.copy(route)
    for _ in range (level):
        index_1 = random.randrange(len(r))
        index_2 = random.randrange(len(r))
        r[index_1], r[index_2] = r[index_2], r[index_1]
    return r

# Method for graph manipulation

# Return the best route between the two
def better(best_route,route):
    if len(best_route) == 0: return route
    elif len(route) == 0: return best_route
    else : 
        return best_route if get_weight(best_route) < get_weight(route) else route


# Get weight of a route and weight until node i if specified
def get_weight(route, index=False):
    if not index : index = len(route)
    global graph
    weight = 0
    for i in range(index):
        # depature time of the day in minutes
        dep_time = weight%1440
        # Add weight from route[i] to route [i+1] + waiting time for opening
        weight += graph[route[i]][ route[(i+1) % len(route)] ][dep_time // 60]

        # arrival time of the day in minutes
        arv_time =    weight%1440

        # get time windows of next node
        tw = get_tw( route[ (i+1) % len(route) ] )

        # initialize waiting times
        nd_time = wo_time = 0

        # you are late, wait for next day starting
        if arv_time > tw["end_time"] : 
            nd_time = 1440 - arv_time
            # update arrival time to midnight
            arv_time = 0
        #you are early, wait for opening
        if arv_time < tw["start_time"] : wo_time = tw["start_time"] - arv_time

        weight += nd_time + wo_time
    return weight


def get_tw(node):
    global tw
    return tw[node]



def random_solution():
    route = []
    possible = list(range(len(graph)))

    while len(possible) != 0:
        route.append(possible.pop(random.randrange(len(possible))))
    return route