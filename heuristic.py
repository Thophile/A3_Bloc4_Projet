from pymongo import MongoClient
import pprint
import random


# Connection to MongoDB
client = MongoClient('localhost', 27017)
db = client['DataProject']
graphs = db['graphs']

graph = []
tw = []

DEBUG = True
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
        routes = []
        if len(best_route) != 0 : routes.append(best_route) 
        routes.append(route)
        best_route =  best(routes)
        if (VERBOSE) :
            print(" Iteration : "+str(_)+" ; Weight : "+str(get_weight(best_route))+ " ; Route : " + str(best_route))
    return best_route

def optimisation(route,level_max):
    nb = 20
    level = 1
    while level <= level_max:
        old = list.copy(route)
        #Generate neighboorhood
        neighbour = []
        neighbour.append(route)
        for _ in range(nb):
            neighbour.append(perturbation(route, level))

        route = best(neighbour)

        # if no change was made
        if old != route : 
            level = 1
        else: level += 1
        if DEBUG : print("Weight : "+str(get_weight(route)) + " Level : "+str(level))
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

# Return best route in an array of route
def best(routes):
    for _ in range(len(routes)):
        if len(routes[_]) == 0:
            routes.pop(_)
    best = routes[0]
    best_weight = get_weight(best)
    for _ in range(len(routes)):
        cur_weight = get_weight(routes[_])
        if cur_weight < best_weight:
            best = routes[_]
            best_weight = cur_weight

    return best

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