class Node:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.id = 0
        self.name = ""

    def __init__(self, x, y, id, name, node):
        self.x = x
        self.y = y
        self.id = id
        self.name = name
        self.node = node


    def __init__(self, x, y, id, node):
        self.x = x
        self.y = y
        self.id = id
        self.name = ""
        self.node = node