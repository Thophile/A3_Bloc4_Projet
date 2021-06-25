from graph import Graph 
from tour import create_tour
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pprint
import random
import time
from localsearch import *

# Constants
FLUSH = False
GENERATE = False
PRINT = True
SEARCH = False
STATS = True

# Connection to MongoDB
client = MongoClient('localhost', 27017)
db = client['DataProject']
graphs = db['graphs']

if(FLUSH):
    graphs.delete_many({})
if(GENERATE):

    n_min = 10
    n_max = 100
    n_step = 1
    graph_per_size = 5
    has_traffic = True
    is_oriented = True

    graph_id = 0
    for n in range(n_min, n_max-n_step, n_step) :
        for _ in range(graph_per_size):
            
            # Generate a graph with parameters
            matrice = Graph(n, has_traffic, is_oriented).matrice
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
                graphs.insert_one( {"graph_id" : graph_id , "node" : node, "start_time" : start_time, "end_time" : end_time, "n" : n, "has_traffic" : has_traffic, "is_oriented" : is_oriented, "row" : matrice[node]})
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

    iter_max = 30
    level_max = 12
    vehicules_nb = 4
    max_size = 50

    # param run
    for _ in range(4):
        # Using binary to generate boolean dict to test each combination
        b = "{0:b}".format(_)
        if len(b) < 2 : b = '0'+ b
        params = {"has_traffic" : b[0] == '1', "is_oriented" : b[1] == '1'}


        # Get all graphs id and size matching the params
        graphs_infos = graphs.aggregate( 
            [
                {"$match" : params},
                {"$group": { "_id": { 'graph_id': "$graph_id", 'n': "$n" } } },
                {"$sort" : {"_id.n":1}}
            ]
        )
        
        times = []
        qualities = []
        for e in graphs_infos :
            graph_info = e["_id"]
            size = graph_info["n"]
            if size > max_size : continue

            start = time.time()
            # Getting a row for verbal param output
            solution, solution_quality = create_tour(params, graph_info, iter_max, level_max, vehicules_nb, 0, local_search)
            # best current : 4500
            duration = time.time() - start
            times.append({"time" : solution_quality, "size" : size})
            qualities.append({"quality" : solution_quality, "size" : size})
            if PRINT : print (solution,solution_quality,duration)

        
        sizes = []
        avg_times = []
        tmp = {}
        for entry in times :
            if not entry["size"] in tmp : tmp[entry["size"]] = []
            tmp[entry["size"]].append(entry["time"])
        for key, value in tmp.items() :
            sizes.append(key)
            avg_times.append(sum(value)/len(value))
        plt.plot(sizes, avg_times, label = str(params))
    plt.ylabel('time')
    plt.xlabel('graph size')
    plt.title("Execution time in function of graph size for a combination of parameters")
    plt.legend()
    plt.show()