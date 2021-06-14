from graph import Graph 
# CONSTANT
# is_boolean | has_boolean
# variable | variable_ou_fonction
# Class

GENERATE = True
if(GENERATE):
    n = 5
    has_traffic = False
    is_complete = False
    is_oriented = False
    print(Graph(n, has_traffic, is_complete, is_oriented).matrice)