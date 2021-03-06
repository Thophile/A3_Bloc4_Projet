from graph import Graph 
from tour import create_tour
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pprint
import random
import time
from localsearch import *
from AntsAlgo.antMain import *
from tabou import *

# Constants
FLUSH = True
GENERATE = True
PRINT = True
SEARCH = True
STATS = False
algo = local_search

# Connection to MongoDB
client = MongoClient('localhost', 27017)
db = client['DataProject']
graphs = db['graphs']

if(FLUSH):
    graphs.delete_many({})
if(GENERATE):

    n_min = 100
    n_max = 100
    n_step = 20
    graph_per_size = 1

    for _ in range(1):
        # Using binary to generate boolean dict to test each combination
        b = "{0:b}".format(_)
        if len(b) < 2 : b = '0'+ b
        params = {"has_traffic" : b[0] != '1', "is_oriented" : b[1] == '1'}

        for n in range(n_min, n_max+n_step, n_step) :
            graph_id = 0
            for _ in range(graph_per_size):
                
                # Generate a graph with parameters
                matrice = Graph(n, params["has_traffic"], params["is_oriented"]).matrice

                # Generate the row that will be saved in MongoDB 
                for node in range(len(matrice)) :       
                    
                    # Opening time between 13h and 22h minutes
                    time_window = random.randrange(800,1340 + 15, 15)


                    # Start time between midnight and midnight - time window
                    start_time = random.randrange(0, 1_440 - time_window + 10, 10)
                    end_time = start_time+time_window

                    # Save generated data into graphs collection
                    graphs.insert_one( {"graph_id" : graph_id , "node" : node, "start_time" : start_time, "end_time" : end_time, "n" : n, "has_traffic" : params["has_traffic"], "is_oriented" : params["is_oriented"], "row" : matrice[node]})
                graph_id += 1
    # Rows check
    print("Rows : "+str(graphs.count_documents({})))

if(SEARCH):
    # Search optimum route
    graph_info = {"graph_id" : 0, "n": 100}
    params = {"has_traffic" : True, "is_oriented" : False}
    iter_max = 100
    level_max = 15
    vehicules_nb = 4
    start = time.time()
    # Getting a row for verbal param output
    solution, solution_quality = create_tour(params, graph_info, iter_max, level_max, vehicules_nb, 0, algo)
    # best current : 4500
    duration = time.time() - start
    print("Duration(s) : " + str(duration) +"; Quality(%) : " + str(solution_quality) + "; Solution : " +str(solution))


if STATS:

    iter_max = 30
    level_max = 12
    vehicules_max_nb = 5
    
    max_size = 400
    min_size = 0
    for vehicules_nb in range(1,vehicules_max_nb + 1):

        fig, (time_ax, quality_ax) = plt.subplots(2)    

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
                if size > max_size or size < min_size : continue

                start = time.time()
                # Getting a row for verbal param output
                solution, solution_quality = create_tour(params, graph_info, iter_max, level_max, vehicules_nb, 0, algo)
                # best current : 4500
                duration = time.time() - start
                times.append({"time" : duration, "size" : size})
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
            time_ax.plot(sizes, avg_times, label = str(params))
            time_ax.set(xlabel='Graph size', ylabel='Time (s)')
            time_ax.legend()

            avg_qualities = []
            tmp = {}
            for entry in qualities :
                if not entry["size"] in tmp : tmp[entry["size"]] = []
                tmp[entry["size"]].append(entry["quality"])
            for key, value in tmp.items() :
                avg_qualities.append(sum(value)/len(value))
            quality_ax.plot(sizes, avg_qualities, label = str(params))
            quality_ax.set(xlabel='Graph size', ylabel='Quality (%)')
            quality_ax.legend()
            
        fig.suptitle("Execution time and quality in function of graph size for a combination of parameters")
        fig.add_axes(quality_ax)
        fig.add_axes(time_ax)
        fig.show()
        input()