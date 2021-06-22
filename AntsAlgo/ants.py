from AntsAlgo.const import ALPHA, BETA, RHO
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
                    self.visit(self, city)
                    
        

    def visit(self, choosed):
        self.visited.append(choosed)

    def travel(self, graph, phero):
        while self.toVisit:
            self.choose(graph, phero)

    def analyzeTravel:
        
    
    def spittingPheromone(self, phero):
        
        for i in range(len(phero)):         #Evaportaion
            for j in range(len(phero)):
                phero[i][j] = phero[i][j] * RHO

        pheromone_path = self.analyzeTravel     #Spit new pheromones
        for i in range(len(self.visited)):
            phero[self.visited[i]][self.visited[i+1]] = pheromone_path[i]
        pass
