import state

class Ant:
    def __init__(self):
        self.visited = list()
        self.toVisit = list()
        self.state = state.IDLE