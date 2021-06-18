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

# OK
def heuristic(graph_id, iter_max, level_max):
    global graph, tw
    graph = [i["row"] for i in graphs.find({"graph_id" : graph_id})]
    tw = [{"start_time" : i["start_time"], "end_time" : i["end_time"]} for i in graphs.find({"graph_id" : graph_id})]
    if DEBUG : print("Graph loaded")

    return