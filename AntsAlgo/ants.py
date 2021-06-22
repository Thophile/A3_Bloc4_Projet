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

    def travel(self, graph, phero):
        while self.toVisit:
            self.choose(graph, phero)
    
    def spittingPheromone(self):
        pass
