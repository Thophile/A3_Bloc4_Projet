from graph import Graph 
from pymongo import MongoClient
import pprint

# CONSTANT
# is_boolean | has_boolean
# variable | variable_ou_fonction
# Class

# Constantes
GENERATE = True
STORE = False
PRINT = True

# Connection a MongoDB
client = MongoClient('localhost', 27017)
db = client['DataProject']


if(GENERATE):
    n = 5
    graphs_to_generate = 1
    has_traffic = False
    is_complete = False
    is_oriented = False

    data = []
    for _ in range(graphs_to_generate):
        # Generate a graph with parameters
        matrice = Graph(n, has_traffic, is_complete, is_oriented).matrice
        if(PRINT): 
            # Print de graph using pprint
            pprint.pprint(matrice) 

        # generate the row that will be saved in MongoDB       
        data.append({"n" : n, "has_traffic" : has_traffic, "is_complete" : is_complete, "is_oriented" : is_oriented, "matrice" : matrice})
        
    if(STORE):
        # Save generated data into graphs collection
        graphs = db['graphs']
        graphs.insert_many(list(data))
