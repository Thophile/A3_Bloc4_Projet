from const import ALPHA, BETA, RHO, CUL
import random
from state import AntState

class Ant:
    def __init__(self):
        self.visited = list()
        self.toVisit = list()
        self.state = AntState.IDLE

    def choose(self, graph, phero):
        remaining_total = {}
        for city in self.toVisit:
            if graph[city][self.visited[len(self.visited)-1]] != 0:
                
                remaining_total[city] = 1 + (pow(phero[city][self.visited[len(self.visited)-1]], ALPHA) * pow(graph[city][self.visited[len(self.visited)-1]], BETA))


        key_list = list(remaining_total.keys())
        val_list = list(remaining_total.values())
        chossen_city = random.choices(key_list, weights= val_list, k=1)
        self.visit(chossen_city[0])
        return
                
    def visit(self, choosed):
        self.visited.append(choosed)
        self.toVisit.remove(choosed)

    def travel(self, graph, phero):
        while self.toVisit:
            self.choose(graph, phero)
        #print(self.visited)
        #print("----------------------------------------------------")
        #print(phero)
        #self.spittingPheromone(phero, graph)


    def analyzeTravel(self, graph):
        deltasPheromones = list()
        travail_sum = 0
        for i in range(len(self.visited)-1):
            travail_sum += graph[self.visited[i]][self.visited[i+1]]
        for i in range(0, len(self.visited)-1):
            deltasPheromones.append(CUL/travail_sum)
        #print(deltasPheromones)
        print(travail_sum)
        return deltasPheromones 
        
    def spittingPheromone(self, phero, graph):
        
        for i in range(len(phero)):         #Evaportaion
            for j in range(len(phero)):
                phero[i][j] = phero[i][j] * RHO
        pheromone_path = self.analyzeTravel(graph)   #Spit new pheromones
        for i in range(0, len(self.visited)-1):
            phero[self.visited[i]][self.visited[i+1]] += pheromone_path[i]
        return phero