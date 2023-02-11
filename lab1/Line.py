from Node import Node

class Line:
    def __init__(self, x1, y1, x2, y2, line, start_node, finish_node):
        self.b = y1-self.k*x1
        self.line = line
        self.start_node = start_node
        self.finish_node = finish_node

    def find_Y(self, x):
        return self.k*x+self.b