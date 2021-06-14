from graph import Graph 
# CONSTANT
# is_boolean | has_boolean
# variable | variable_ou_fonction
# Class

GENERATE = True
if(GENERATE):
    n = 5
    has_traffic = True
    is_complete = False
    
    print(Graph(n, has_traffic, is_complete).matrice)