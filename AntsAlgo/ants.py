from AntsAlgo.const import ALPHA, BETA, RHO, CUL
import random

class Ant: # the ant class
    def __init__(self): # initialize visited and to visit cities lists as well as the time
        self.visited = list()
        self.toVisit = list()
        self.time = 0

    """[summary]

        Function to choose the next city by using pheromones and distances (formulas)
    """
    def choose(self, graph, phero, param):
        remaining_total = {} # list of importance of the city regarding the distance and the pheromones
        for city in self.toVisit:
            if graph[self.visited[len(self.visited)-1]][city][(self.time%1440)//60 if param["has_traffic"] else 0] != 0: # check if the ant can go to this city
                remaining_total[city] = 0.00001 + (pow(phero[self.visited[len(self.visited)-1]][city], ALPHA) * pow(graph[self.visited[len(self.visited)-1]][city][(self.time%1440)//60 if param["has_traffic"] else 0], BETA))


        key_list = list(remaining_total.keys())
        val_list = list(remaining_total.values())
        chossen_city = random.choices(key_list, weights= val_list, k=1) # randomly weighted choice of the next city
        self.visit(chossen_city[0], graph, param) # go to the city
        return

    """[summary]

        Function to check if the ants arrived on time, and then calculate the waiting time
    """
    def deliver(self, tw):
        waiting_time = 0
        city = self.visited[len(self.visited)-1]
        if tw[city]["start_time"] >= self.time % 1440 or tw[city]["end_time"] <= self.time: # if late or early
            waiting_time = (tw[city]["start_time"] - self.time) % 1440
        elif tw[city]["end_time"] >= self.time % 1440 and tw[city]["start_time"] <= self.time % 1440: # on time
            waiting_time = 0
        self.time += waiting_time


    """[summary]

        Function to actualize the two list and update the current time
    """    
    def visit(self, choosed, graph, param):
        self.time += graph[self.visited[len(self.visited)-1]][choosed][(self.time%1440)//60 if param["has_traffic"] else 0] # add the time
        last = None
        if self.toVisit == [0]:
            last = True
        self.visited.append(choosed)
        self.toVisit.remove(choosed)
        if self.toVisit == [] and not(last):
            self.toVisit.append(0)
        
    """[summary]

        Loop to travel all the cities of the list
    """
    def travel(self, graph, phero, tw, param):
        self.time = 0
        while self.toVisit:
            self.choose(graph, phero, param)
            self.deliver(tw)


    """[summary]

        Function calculate the delta pheromones
    """
    def analyzeTravel(self, graph):
        deltasPheromones = list()
        for i in range(0, len(self.visited)-1):
            deltasPheromones.append(CUL/self.time) # formula
        return deltasPheromones 
        
    """[summary]

        Put the pheromones in the pheromones graph
    """    
    def spittingPheromone(self, phero, graph, param):
        pheromone_path = self.analyzeTravel(graph)   #Spit new pheromones
        for i in range(0, len(self.visited)-1):
            phero[self.visited[i]][self.visited[i+1]] += pheromone_path[i]
        return phero