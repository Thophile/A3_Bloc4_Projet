from graph import Graph 
from heuristic import create_tour
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pprint
import random
import time

# Constants
FLUSH = True
GENERATE = True
PRINT = False
SEARCH = True
STATS = True

# Connection to MongoDB
client = MongoClient('localhost', 27017)
db = client['DataProject']
graphs = db['graphs']

if(FLUSH):
    graphs.delete_many({})
if(GENERATE):

    n_min = 10
    n_max = 15
    n_step = 1
    graph_per_size = 5
    has_traffic = True
    is_complete = True
    is_oriented = False

    graph_id = 0
    for n in range(n_min, n_max, n_step) :
        for _ in range(graph_per_size):
            
            # Generate a graph with parameters
            matrice = Graph(n, has_traffic, is_complete, is_oriented).matrice
            if(PRINT): 
                # Print graph using pprint , using normal print for 3 dimension array
                print(matrice) if has_traffic else pprint.pprint(matrice) 

            # Generate the row that will be saved in MongoDB 
            for node in range(len(matrice)) :       

                
                # Opening time between 60 and 120 minutes
                time_window = random.randrange(800,1340 + 15, 15)


                # Start time between midnight and midnight - time window
                start_time = random.randrange(0, 1_440 - time_window + 10, 10)
                end_time = start_time+time_window

                # Save generated data into graphs collection
                graphs.insert_one( {"graph_id" : graph_id , "node" : node, "start_time" : start_time, "end_time" : end_time, "n" : n, "has_traffic" : has_traffic, "is_complete" : is_complete, "is_oriented" : is_oriented, "row" : matrice[node]})
            graph_id += 1
    # Rows check
    print("Rows : "+str(graphs.count_documents({})))

if(SEARCH):
    # Search optimum route
    graph_id = 1
    
    iter_max = 10
    level_max = 10
    vehicules_nb = 4
    print(create_tour(graph_id, iter_max, level_max, vehicules_nb, depot=0))

    
if STATS:

    iter_max = 10
    level_max = 10
    vehicules_nb = 4

    # param run


    graphs_ids = graphs.find_one({}, {"_id":0, "graph_id":1}, sort=[("graph_id", -1)])["graph_id"]+1
    print(graphs_ids)
    times = []
    for graph_id in range(graphs_ids) :
        size = graphs.find_one({"graph_id" : graph_id}, {"_id":0, "n":1})["n"]
        start = time.time()
        # Getting a row for verbal param output
        create_tour(graph_id, iter_max, level_max, vehicules_nb, depot=0)
        # best current : 4500
        duration = time.time() - start
        times.append({"time" : duration, "size" : size})
    
    sizes = []
    avg_times = []
    tmp = {}
    for entry in times :
        if not entry["size"] in tmp : tmp[entry["size"]] = []
        tmp[entry["size"]].append(entry["time"])
    for key, value in tmp.items() :
        sizes.append(key)
        avg_times.append(sum(value)/len(value))
    plt.plot(sizes, avg_times)
    plt.ylabel('time')
    plt.xlabel('graph size')
    plt.show()