from graph import Graph 
from pymongo import MongoClient
import pprint

# Constants
GENERATE = True
STORE = False
PRINT = True

# Connection to MongoDB
client = MongoClient('localhost', 27017)
db = client['DataProject']


if(GENERATE):

    n_min = 5
    n_max = 7
    n_step = 1
    graphs_to_generate = 1
    has_traffic = False
    is_complete = True
    is_oriented = False

    for n in range(n_min, n_max, n_step) :
        data = []
        for _ in range(graphs_to_generate):
            
            # Generate a graph with parameters
            matrice = Graph(n, has_traffic, is_complete, is_oriented).matrice
            if(PRINT): 
                # Print graph using pprint , using normal print for 3 dimension array

                print(matrice) if has_traffic else pprint.pprint(matrice) 

            # Generate the row that will be saved in MongoDB       
            data.append({"n" : n, "has_traffic" : has_traffic, "is_complete" : is_complete, "is_oriented" : is_oriented, "matrice" : matrice})
        if(STORE):
            # Save generated data into graphs collection
            graphs = db['graphs']
            graphs.insert_many(list(data))
