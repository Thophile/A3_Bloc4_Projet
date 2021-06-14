import traffic
import random

class Edge:
    def __init__(self,length, traffic):
        # Generate an array of weight for base weight * traffic coefficient 
        self.weight = [length*i for i in traffic]

class Graph:
    def __init__(self, n, has_traffic, is_complete, is_oriented):
        g = []
        for i in range(n):
            row = []
            for j in range(n):
                    # For non oriented graphs use symmetry to generate the bottom left part of the graph
                if(j<i and not is_oriented):
                    weight = g[j][i]
                else:
                    weight = Edge(
                        # Random base weight for the edge, range start at 1 if the graphs is complete,
                        # weight is 0 if the edge is a loop
                        random.randrange((1 if is_complete else 0),10) if i!=j else 0,
                        # Generated traffic data or 1 if traffic is not used
                        traffic.generate() if has_traffic else [1] 
                        ).weight
                row.append(weight)
            g.append(row)
        self.matrice = g 
