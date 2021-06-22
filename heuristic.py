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
def create_tour(graph_id, iter, level, vehicules_nb, depot):
    global graph, tw
    graph = [i["row"] for i in graphs.find({"graph_id" : graph_id})]
    tw = [{"start_time" : i["start_time"], "end_time" : i["end_time"]} for i in graphs.find({"graph_id" : graph_id})]

    tours = []
    for _ in range(vehicules_nb):
        tours.append([])
    # for each node
    for i in range(len(graph)):
        # put it in a random tour if it is not the depot
        if i != depot :
            #ensure every tour as at least 1 node
            index = random.randrange(0,vehicules_nb)
            for _ in range(vehicules_nb):
                if len(tours[_]) == 0 :
                    index = _
                    break
            tours[index].append(i)
        
    if DEBUG : 
        print("Graph loaded & Tours generated : ")
        pprint.pprint(tours)

    solutions = []
    for _ in range(vehicules_nb):
        opt_tour = local_search(tours[_], iter, level)
        solutions.append({"weight": get_weight(opt_tour), "tour" : opt_tour})
    if VERBOSE : print(solutions)
    return solutions

# Local search version
def local_search(tour, iter, level_max):
    best_route = []
    for _ in range(iter):
        route = random_solution(tour)
        route = optimisation(route, level_max)
        routes = []
        if len(best_route) != 0 : routes.append(best_route) 
        routes.append(route)
        best_route =  best(routes)
        if (DEBUG) :
            print(" Iteration : "+str(_)+" ; Weight : "+str(get_weight(best_route))+ " ; Route : " + str(best_route))
    return best_route

def optimisation(route,level_max):
    nb = 50
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
def get_weight(route, index=False, start_at_zero = True):
    # cloning route 
    clone = list.copy(route)
    # adding depot at the start for weight calculation
    if start_at_zero: clone.insert(0,0)
    if not index : index = len(clone)
    global graph
    weight = 0
    for i in range(index):
        # depature time of the day in minutes
        dep_time = weight%1440
        # Add weight from clone[i] to clone [i+1] + waiting time for opening
        weight += graph[clone[i]][ clone[(i+1) % len(clone)] ][dep_time // 60]

        # arrival time of the day in minutes
        arv_time =    weight%1440

        # get time windows of next node
        tw = get_tw( clone[ (i+1) % len(clone) ] )

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



def random_solution(tour):
    route = []
    possible = list.copy(tour)

    while len(possible) != 0:
        route.append(possible.pop(random.randrange(len(possible))))
    return route