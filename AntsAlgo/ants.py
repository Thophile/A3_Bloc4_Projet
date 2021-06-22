from AntsAlgo.const import ALPHA, BETA
from random import random
from state import AntState

class Ant:
    def __init__(self):
        self.visited = list()
        self.toVisit = list()
        self.state = AntState.IDLE

    def choose(self, graph, phero):
        Remaining_Total = 0
        for city in self.toVisit:
            if graph[len(self.toVisit)][city]:
                Remaining_Total =+ ((phero[len(self.toVisit)][city] ^ ALPHA) * (graph[len(self.toVisit)][city] ^ BETA))
        for city in self.toVisit:
            if graph[len(self.toVisit)][city]:
                proba = ((phero[len(self.toVisit)][city] ^ ALPHA) * (graph[len(self.toVisit)][city] ^ BETA)) / Remaining_Total
                if random(0, Remaining_Total) > proba:
                    pass
                    
        

    def visit(self):
        pass
