from graph import Graph 
from heuristic import heuristic
from pymongo import MongoClient
import pprint
import random

# Constants
FLUSH = False
GENERATE = False
PRINT = False
SEARCH = True

# Connection to MongoDB
client = MongoClient('localhost', 27017)
db = client['DataProject']
graphs = db['graphs']

if(FLUSH):
    graphs.delete_many({})
if(GENERATE):

    n_min = 100
    n_max = 101
    n_step = 1
    graphs_to_generate = 1
    has_traffic = True
    is_complete = True
    is_oriented = False

    for n in range(n_min, n_max, n_step) :
        for _ in range(graphs_to_generate):
            
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
                graphs.insert_one( {"graph_id" : _ , "node" : node, "start_time" : start_time, "end_time" : end_time, "n" : n, "has_traffic" : has_traffic, "is_complete" : is_complete, "is_oriented" : is_oriented, "row" : matrice[node]})
    # Rows check
    print("Rows : "+str(graphs.count_documents({})))

if(SEARCH):
    # Search optimum route
    graphs_to_search = 1
    iter_max = 100
    level_max = 50

    for graph_id in range(graphs_to_search) :

        # Getting a row for verbal param output
        heuristic(graph_id, iter_max, level_max)