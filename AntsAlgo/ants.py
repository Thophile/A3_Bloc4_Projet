from const import ALPHA, BETA, RHO, CUL
import random
from state import AntState

class Ant:
    def __init__(self):
        self.visited = list()
        self.toVisit = list()
        self.state = AntState.IDLE

    def choose(self, graph, phero):
        remaining_total = 0
        test = [0, 1, 2, 3]
        for city in self.toVisit:
            if graph[city][self.visited[len(self.visited)-1]] != 0:
                remaining_total += pow(phero[city][self.visited[len(self.visited)-1]], ALPHA) * pow(graph[city][self.visited[len(self.visited)-1]], BETA)
        for city in self.toVisit:
            if graph[city][self.visited[len(self.visited)-1]] != 0:
                proba = pow(phero[city][self.visited[len(self.visited)-1]], ALPHA) * pow(graph[city][self.visited[len(self.visited)-1]], BETA) / remaining_total
                if random.uniform(0, remaining_total) <= proba:
                    self.visit(city)
                    return

                
    def visit(self, choosed):
        self.visited.append(choosed)
        self.toVisit.remove(choosed)

    def travel(self, graph, phero):
        while self.toVisit:
            self.choose(graph, phero)
        print(self.visited)
        print(phero)
        print("----------------------------------------------------")
        self.spittingPheromone(phero, graph)


    def analyzeTravel(self, graph):
        deltasPheromones = list()
        for i in range(0, len(self.visited)-1):
            deltasPheromones.append(CUL/graph[self.visited[i]][self.visited[i+1]])
        return deltasPheromones 
        
    def spittingPheromone(self, phero, graph):
        
        for i in range(len(phero)):         #Evaportaion
            for j in range(len(phero)):
                phero[i][j] = phero[i][j] * RHO
        pheromone_path = self.analyzeTravel(graph)   #Spit new pheromones
        for i in range(len(self.visited)-1):
            phero[self.visited[i]][self.visited[i+1]] = pheromone_path[i]
        return phero