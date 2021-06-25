from traffic import generate
from utility import console_clear
import random
import math

class Edge:
    def __init__(self,length, traffic):
        # Generate an array of weight for base weight * traffic coefficient 
        self.weight = [(length + 30*scale) if length!=0 else length for scale in traffic ]

class Graph:
    def __init__(self, n, has_traffic, is_oriented):
        g = []
        for i in range(n):
            console_clear()
            print("Progress : "+str(math.ceil(100*i/n)))
            row = []
            for j in range(n):
                    # For non oriented graphs use symmetry to generate the bottom left part of the graph
                if(j<i and not is_oriented):
                    weight = g[j][i]
                else:
                    weight = Edge(
                        # Random base weight for the edge, range start at 1 if the graphs is complete,
                        # weight is 0 if the edge is a loop
                        random.randrange(5, 240, 5) if i!=j else 0,
                        # Generated traffic data or 1 if traffic is not used
                        generate() if has_traffic else [0] 
                        ).weight
                row.append(weight)
            g.append(row)
        self.matrice = g 
