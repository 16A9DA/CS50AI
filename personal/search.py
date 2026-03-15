

class Node():
    def __init__(self,state,parent,action):
        self.state = state
        self.parent = parent
        self.action = action

class StackForntier():
    def __init__(self):
        self.frontier = []
    
    def add(self,node):
        self.frontier.append(node)
    
    def checkEmpty(self):
        return len(self.frontier) == 0
    
    def contains_state(self,state):
        return any(node.state == state for node in self.frontier)
    
    def remove(self):
        if self.checkEmpty():
            return Exception("Empty")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackForntier):
    def remove(self):
        if self.checkEmpty():
            return Exception("Empty")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1::]
            return node