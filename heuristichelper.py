import random

# Method for graph manipulation

# Return best route in an array of route
def best(params, graph, tw, routes):
    for _ in range(len(routes)):
        if len(routes[_]) == 0:
            routes.pop(_)
    best = routes[0]
    best_weight = get_weight(params, graph, tw, best)
    for _ in range(len(routes)):
        cur_weight = get_weight(params, graph, tw, routes[_])
        if cur_weight < best_weight:
            best = routes[_]
            best_weight = cur_weight

    return best

# Get weight of a route and weight until node i if specified
def get_weight(params, graph, tw, route, index=False, depot = 0):

    # cloning route 
    clone = list.copy(route)
    # adding depot at the start for weight calculation
    clone.insert(0,depot)
    if not index : index = len(clone)
    weight = 0
    for i in range(index):
        # depature time of the day in minutes
        dep_time = weight%1440
        # Add weight from clone[i] to clone [i+1] + waiting time for opening
        weight += graph[clone[i]][ clone[(i+1) % len(clone)] ][dep_time // 60 if params["has_traffic"] else 0]

        # arrival time of the day in minutes
        arv_time =    weight%1440

        # get time windows of next node
        tw = get_tw(tw, clone[ (i+1) % len(clone) ] )

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


def get_tw(tw, node):
    return tw[node]



def random_solution(tour):
    route = []
    possible = list.copy(tour)

    while len(possible) != 0:
        route.append(possible.pop(random.randrange(len(possible))))
    return route