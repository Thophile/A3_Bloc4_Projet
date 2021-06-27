from const import ALPHA, BETA, RHO, CUL
import random
from state import AntState

class Ant:
    def __init__(self):
        self.visited = list()
        self.toVisit = list()
        self.state = AntState.IDLE
        self.time = 0

    def choose(self, graph, phero):
        remaining_total = {}
        for city in self.toVisit:
            if graph[self.visited[len(self.visited)-1]][city] != 0:
                remaining_total[city] = 0.00001 + (pow(phero[self.visited[len(self.visited)-1]][city], ALPHA) * pow(graph[self.visited[len(self.visited)-1]][city], BETA))


        key_list = list(remaining_total.keys())
        val_list = list(remaining_total.values())
        chossen_city = random.choices(key_list, weights= val_list, k=1)
        self.visit(chossen_city[0], graph)
        return

    def deliver(self, tw):
        waiting_time = 0
        city = self.visited[len(self.visited)-1]
        if tw[city]["start"] >= self.time % 1440 or tw[city]["end"] <= self.time:
            print('waiting')
            waiting_time = (tw[city]["start"] - self.time) % 1440
        elif tw[city]["end"] >= self.time % 1440 and tw[city]["start"] <= self.time % 1440:
            print('not waiting')
            waiting_time = 0
        self.time += waiting_time


                
    def visit(self, choosed, graph):
        self.time += graph[self.visited[len(self.visited)-1]][choosed]
        self.visited.append(choosed)
        self.toVisit.remove(choosed)
        

    def travel(self, graph, phero, tw):
        self.time = 0
        while self.toVisit:
            print(self.time)
            self.choose(graph, phero)
            self.deliver(tw)
        #print(self.visited)
        #print("----------------------------------------------------")
        #print(phero)
        #self.spittingPheromone(phero, graph)


    def analyzeTravel(self, graph):
        deltasPheromones = list()
        """
        travail_sum = 0
        for i in range(len(self.visited)-1):
            travail_sum += graph[self.visited[i]][self.visited[i+1]]"""
        for i in range(0, len(self.visited)-1):
            deltasPheromones.append(CUL/self.time)
        #print(deltasPheromones)
        print(self.time)
        print(self.visited)
        return deltasPheromones 
        
    def spittingPheromone(self, phero, graph):
        pheromone_path = self.analyzeTravel(graph)   #Spit new pheromones
        for i in range(0, len(self.visited)-1):
            phero[self.visited[i]][self.visited[i+1]] += pheromone_path[i]
        return phero