from state import AntState

class Ant:
    def __init__(self):
        self.visited = list()
        self.toVisit = list()
        self.state = AntState.IDLE

    def choose(self):
        pass

    def visit(self, choosed):
        self.visited.append(choosed)
        self.toVisit.remove(choosed)

    def travel(self, graph, phero):
        while self.toVisit:
            self.choose(graph, phero)

    def analyzeTravel():
        deltasPheromones = list()
        for i in range(0, len(self.visited)):
            pass

        


    
    def spittingPheromone(self):
        pass
