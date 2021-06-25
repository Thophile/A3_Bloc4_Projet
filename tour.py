from pymongo import MongoClient
import pprint
import random
from heuristichelper import *


# Connection to MongoDB
client = MongoClient('localhost', 27017)
db = client['DataProject']
graphs = db['graphs']

graph = []
tw = []

DEBUG = False

# Handler method
def create_tour(params, graph_info, iter, level, vehicules_nb, depot=0, callback = None):
    global graph, tw
    rows = graphs.find({"has_traffic": params["has_traffic"], "is_oriented": params["is_oriented"], "graph_id" : graph_info["graph_id"], "n": graph_info["n"]})
    graph = [i["row"] for i in rows]
    tw = [{"start_time" : i["start_time"], "end_time" : i["end_time"]} for i in rows]

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
    if(callback):
        solution = []
        for _ in range(vehicules_nb):
            opt_tour = callback(params, graph, tw, tours[_], iter, level)
            solution.append({"weight": get_weight(params,graph,tw,opt_tour), "tour" : opt_tour})
        return solution, quality(params,graph_info,sum(extract_field(solution,"weight")))
    else:
        return tours

