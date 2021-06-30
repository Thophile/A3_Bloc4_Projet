import random
from heuristichelper import *

tw = []
TABOU_SIZE = 30
tabou_list = []


def start_tabou(params, graph, tw, tour, iter, level_max):

    route = random_solution(tour)
    for _ in range(iter):
        print('iter : '  + str(_))
        print("route actuelle" + str(route))
        tabou_list, best_weight, best_route, best_route_voisin = tabou_research(params, route,tw, graph)
       
        print("----------------------------------------------------------------------------------------------")
        route = best_route_voisin
    return tabou_list, best_weight, best_route, tw


def tabou_research(params, current_route,tw , graph):
    best_weight = 9999999999

    best_route_voisin = best_neighbour(params, current_route,tw, graph)
    print("route voisin" + str(best_route_voisin))
    print("tabou list" + str(tabou_list))
    
    if(check_tabou(best_route_voisin)):
        update_tabou(best_route_voisin)
        current_weight = get_weight(params, graph, tw, best_route_voisin, index=False, depot = 0)
        print("poids" + str(current_weight))
        if(current_weight < best_weight):
            best_weight = current_weight
            best_route = best_route_voisin
    return tabou_list, best_weight, best_route, best_route_voisin



def best_neighbour(params, route,tw, graph):
    list_neighbours = []
    list_weight_neighbour = []
    best_list_route = [] 


    for i in route:
        if i != 0:
            neighbour = list(route)
            if i == (len(route)-1):
                neighbour[i] = neighbour[1]
                neighbour[1] = route[i]
            else :
                neighbour[i] = neighbour[i+1]
                neighbour[i+1] = route[i]
            list_neighbours.append(neighbour)
    

    for i in list_neighbours:
        list_weight_neighbour.append(get_weight(params, graph, tw, i, index=False, depot = 0))

    best_neighbour = list_neighbours[list_weight_neighbour.index(min(list_weight_neighbour))]
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
   

def check_tabou(route):
    return route not in tabou_list

def update_tabou(route):
    if (len(tabou_list) == TABOU_SIZE) :
        del tabou_list[0]
    tabou_list.append(route)
