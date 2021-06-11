import traffic
import random

class Edge:
    def __init__(self,length, traffic):
        self.weigth = [length*i for i in traffic]

class Graph:
    def __init__(self,n,has_traffic):
        g = []
        for _ in range(n):
            row = []
            for _ in range(n):
                row.append(Edge(
                    random.randrange(1,10),
                    traffic.generate() if has_traffic else [1]).weigth)
            g.append(row)
        self.matrice = g 
