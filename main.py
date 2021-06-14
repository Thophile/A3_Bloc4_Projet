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
            # Print graph using pprint
            pprint.pprint(matrice) 

        # Generate the row that will be saved in MongoDB       
        data.append({"n" : n, "has_traffic" : has_traffic, "is_complete" : is_complete, "is_oriented" : is_oriented, "matrice" : matrice})
        
    if(STORE):
        # Save generated data into graphs collection
        graphs = db['graphs']
        graphs.insert_many(list(data))
