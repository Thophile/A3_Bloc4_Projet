import random
from heuristichelper import *
DEBUG = False

# Size of the taboo list
TABOU_SIZE = 30
tabou_list = []


def start_tabou(params, graph, tw, tour, iter, level_max):
    best_route = []
    # Generation of a random solution
    route = random_solution(tour)
    # For each iteration:
    for _ in range(iter):
        if DEBUG :
            print(_, route)
        # Taboo research
        best_route, best_route_voisin = tabou_research(params, route, best_route, tw, graph)
        # We take as new road the best neighboring road 
        route = best_route_voisin
    return best_route


def tabou_research(params, current_route, best_route, tw , graph):
    best_weight = 9999999999

    # Search for the best neighboring road
    best_route_voisin = best_neighbour(params, current_route,tw, graph)
    if DEBUG : 
        print("route voisin" + str(best_route_voisin))
        print("tabou list" + str(tabou_list))
    
    # We check that the road is not taboo
    if(check_tabou(best_route_voisin)):
        # We update the taboo list
        update_tabou(best_route_voisin)
        # We calculate the weight of the road
        current_weight = get_weight(params, graph, tw, best_route_voisin, index=False, depot = 0)
        if DEBUG : print("poids" + str(current_weight))
        # If the calculated weight is the best ever
        if(current_weight < best_weight):
            # The weight becomes the best weight
            best_weight = current_weight
            best_route = best_route_voisin
    return best_route, best_route_voisin


# Recovery of the best neighboring solution
def best_neighbour(params, route,tw, graph):
    list_neighbours = []
    list_weight_neighbour = []
    best_list_route = [] 

    # Generation of all neighboring solutions
    for i in range(len(route)):
        neighbour = list.copy(route)
        neighbour[i], neighbour[(i+1)%len(neighbour)] = neighbour[(i+1)%len(neighbour)], neighbour[i]
        list_neighbours.append(neighbour)
    
    # Weight calculation for each solution
    for neighbour in list_neighbours:
        list_weight_neighbour.append(get_weight(params, graph, tw, neighbour, index=False, depot = 0))

    # Recovery of the road with minimum weight
    best_neighbour = list_neighbours[list_weight_neighbour.index(min(list_weight_neighbour))]

    # Loop to take another solution if the best one is taboo
    while(True):
        if not list_weight_neighbour:
            best_list_route = best_neighbour
            break
        else:
            best_list_route = list_neighbours[list_weight_neighbour.index(min(list_weight_neighbour))]
            if(check_tabou(best_list_route)):
                break
            else:
                list_weight_neighbour.remove(min(list_weight_neighbour))
                list_neighbours.remove(best_list_route)

    return best_list_route
   
# Check if a road is taboo
def check_tabou(route):
    return route not in tabou_list

# Update the taboo list
def update_tabou(route):
    if (len(tabou_list) == TABOU_SIZE) :
        del tabou_list[0]
    tabou_list.append(route)
