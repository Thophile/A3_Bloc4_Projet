import random

# poids = [
 #   [0, 170, 130, 20, 180],
##    [170, 0, 100, 230, 55],
 #   [130, 100, 0, 165, 125],
 #   [20, 230, 165, 0, 175],
 #   [180, 55, 125, 175, 0]
 #   ]

tw = []
tour = []
poids = []
#traffic = [1, 1, 1, 1, 1, 1, 1, 2, 7, 8, 3, 2, 1, 1, 1, 2, 3, 5, 7, 5, 1, 1, 1, 1, 1]



TABOU_SIZE = 1000
tabou_list = []

best_route = []
best_weight = 999999999999



def start_tabou(params, graph, tw_list, list_ville, iter, level_max):
    global poids
    global tour
    global tw

    poids = graph
    
    tour = list_ville
    tw = tw_list

    route = random_solution()
    for _ in range(iter):
        print('iter : '  + str(_))
        print("route actuelle" + str(route))
        tabou_list, best_weight, best_route, best_route_voisin = tabou_research(route)
       
        print("----------------------------------------------------------------------------------------------")
        route = best_route_voisin
    return tabou_list, best_weight, best_route


def tabou_research(current_route):
    global best_weight
    global best_route

    best_route_voisin = best_neighbour(current_route)
    print("route voisin" + str(best_route_voisin))
    print("tabou list" + str(tabou_list))
    
    if(check_tabou(best_route_voisin)):
        update_tabou(best_route_voisin)
        current_weight = calcul_weight(best_route_voisin)
        print("poids" + str(current_weight))
        if(current_weight < best_weight):
            best_weight = current_weight
            best_route = best_route_voisin
    return tabou_list, best_weight, best_route, best_route_voisin


def random_solution():
    route = []
    possible = list(range(len(tour)))

    route.append(possible.pop(0))

    while len(possible) != 0:
        route.append(possible.pop(random.randrange(len(possible))))
    return route


def best_neighbour(route):
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
        list_weight_neighbour.append(calcul_weight(i))

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
   

def  calcul_weight(route):
    weight = 0
    for x in range(len(route)):
        
        i = route[x]

        if(weight != 0):
            tranche_horaire = int(weight%24)
        else:
            tranche_horaire = 0

        

        if(x < (len(route)-1)):
            j = route[x+1]
        else:
            j = route[0]

        traffic = poids[i][j]       
        weight += traffic[tranche_horaire]

        tw_i = tw[j]
        time_start = tw_i['start_time']
        time_end = tw_i['end_time']
    

        if(time_start <= weight  and time_end >= weight):
            waiting_time = 0
        elif(time_start >= weight  or time_end <= weight):
            waiting_time = (time_start-weight) % 1440

        weight += waiting_time

    return weight


def check_tabou(route):
    return route not in tabou_list

def update_tabou(route):
    if (len(tabou_list) == TABOU_SIZE) :
        del tabou_list[0]
    tabou_list.append(route)

def generate_Tw(n):
    global tw
    for i in range(0, n):
        start = random.randrange(30,1440, 30) 
        end = (start + random.randrange(60,180, 30)) % 1440
        tw.append({"start_time": start, "end_time": end})
    return tw