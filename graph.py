import traffic
import random

class Edge:
    def __init__(self,length, traffic):
        self.weight = [length*i for i in traffic]

class Graph:
    def __init__(self, n, has_traffic, is_complete, is_oriented):
        g = []
        for i in range(n):
            row = []
            for j in range(n):
                if(j<i and not is_oriented):
                    weight = g[j][i]
                else:
                    weight = Edge(
                        random.randrange((1 if is_complete else 0),10) if i!=j else 0,
                        traffic.generate() if has_traffic else [1]
                        ).weight
                row.append(weight)
            g.append(row)
        self.matrice = g 
