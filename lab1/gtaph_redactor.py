from tkinter import *
from Node import Node
from Line import Line

class GraphEditor(Frame):

    def __init__(self):
        super().__init__()
        self.nodes = []
        self.lines = []
        self.initUI()


    def initUI(self):
        self.master.title("graph editor")
        self.pack(fill=BOTH, expand=1)

        self.x = self.y = self.kod = 0
        self.canvas = Canvas(bg="white", width=850, height=650)

        self.var = IntVar()
        self.var.set(0)

        rb1 = Radiobutton(self, text="Node", variable=self.var, indicatoron=0, command=self.choose_what_to_do, width=10, height=5, value=0)
        rb2 = Radiobutton(self, text="Line", variable=self.var, indicatoron=0, command=self.choose_what_to_do, width=10, height=5, value=1)
        rb3 = Radiobutton(self, text="Delete", variable=self.var, indicatoron=0, command=self.choose_what_to_do, width=10, height=5, value=2)
        rb4 = Button (self, text="Clear", command=self.clear, width=10, height=5)
        rb1.grid(row=1, column=1, padx=50)
        rb2.grid(row=1, column=2, padx=50)
        rb3.grid(row=1, column=3, padx=50)
        rb4.grid(row=1, column=4, padx=50)

        self.canvas.pack(anchor=CENTER, expand=1)


    def clear(self):
        self.canvas.delete("all")
        self.nodes.clear()
        self.lines.clear()

    def on_button_press(self, event):
        for node in self.nodes:
            if (event.x-node.x)**2 + (event.y-node.y)**2 <= 100:
                self.start_node = node
        self.x = event.x
        self.y = event.y

    def draw_circle(self, event):
        node = self.canvas.create_oval(event.x - 10, event.y - 10, event.x + 10, event.y + 10)
        self.nodes.append(Node(event.x, event.y, len(self.nodes)+1, node))

    def draw_line(self, event):
        if self.is_in_circle(event.x, event.y) and self.is_in_circle(self.x, self.y):
            for node in self.nodes:
                if (event.x - node.x) ** 2 + (event.y - node.y) ** 2 <= 100:
                    self.finish_node = node
            x11 = self.start_node.x + (10*(self.finish_node.x-self.start_node.x)/self.distance(self.start_node.x, self.start_node.y, self.finish_node.x, self.finish_node.y))
            x12 = self.start_node.x - (10 * (self.finish_node.x - self.start_node.x) / self.distance(self.start_node.x,
                                                                                                      self.start_node.y,
                                                                                                 self.finish_node.x,
                                                                                                      self.finish_node.y))
            y11 = self.start_node.y + (10 * (self.finish_node.y - self.start_node.y) / self.distance(self.start_node.x,
                                                                                                      self.start_node.y,
                                                                                                      self.finish_node.x,
                                                                                                      self.finish_node.y))
            y12 = self.start_node.y - (10 * (self.finish_node.y - self.start_node.y) / self.distance(self.start_node.x,
                                                                                                      self.start_node.y,
                                                                                                      self.finish_node.x,
                                                                                                      self.finish_node.y))
            if self.distance(x11, y11, self.finish_node.x, self.finish_node.y)<self.distance(x12, y12, self.finish_node.x, self.finish_node.y):
                x1=x11
                y1=y11
            else:
                x1=x12
                y1=y12

            x21 = self.finish_node.x + (10 * (self.start_node.x - self.finish_node.x) / self.distance(self.start_node.x,
                                                                                                     self.start_node.y,
                                                                                                     self.finish_node.x,
                                                                                                     self.finish_node.y))
            x22 = self.finish_node.x - (10 * (self.start_node.x - self.finish_node.x) / self.distance(self.start_node.x,
                                                                                                     self.start_node.y,
                                                                                                     self.finish_node.x,
                                                                                                     self.finish_node.y))
            y21 = self.finish_node.y + (10 * (self.start_node.y - self.finish_node.y) / self.distance(self.start_node.x,
                                                                                                     self.start_node.y,
                                                                                                     self.finish_node.x,
                                                                                                     self.finish_node.y))
            y22 = self.finish_node.y - (10 * (self.start_node.y - self.finish_node.y) / self.distance(self.start_node.x,
                                                                                                     self.start_node.y,
                                                                                                     self.finish_node.x,
                                                                                                     self.finish_node.y))
            if self.distance(x21, y21, self.start_node.x, self.start_node.y) < self.distance(x22, y22,
                                                                                               self.start_node.x,
                                                                                               self.start_node.y):
                x2 = x21
                y2 = y21
            else:
                x2 = x22
                y2 = y22
            
            line = self.canvas.create_line(x1, y1, x2, y2)
            self.lines.append(Line(x1, y1, x2, y2, line, start_node=self.start_node, finish_node=self.finish_node))




    def distance(self,x1,y1,x2,y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def choose_what_to_do(self):
        if self.var.get() == 0:
            self.canvas.unbind("<Motion>")
            self.unbind_all()
            self.canvas.bind("<Double-Button-1>", self.draw_circle)
        elif self.var.get() == 1:
            self.unbind_all()
            self.canvas.unbind("Motion")
            self.canvas.bind("<Motion>", self.draw_line_between_two_circles)
        elif self.var.get() == 2:
            self.unbind_all()
            self.canvas.unbind("<Motion>")
            self.canvas.bind("<Motion>", self.choose_what_to_delete)


    def choose_what_to_delete(self, event):
        if self.is_in_circle(event.x, event.y):
            self.canvas.bind("<Double-Button-1>", self.delete_circle)
        elif self.is_on_line(event.x, event.y):
            self.canvas.bind("<Double-Button-1>", self.delete_line)

    def delete_line(self, event):
        for line in self.lines:
            if abs(line.k*event.x+line.b) <= abs(event.y)+2:
                self.canvas.delete(line.line)
                self.lines.remove(line)

    def delete_circle(self, event):
        for node in self.nodes:
            if (event.x-node.x)**2 + (event.y-node.y)**2 <= 100:
                self.canvas.delete(node.node)
                counter = 0
                while counter < len(self.lines):
                    if self.lines[counter].finish_node == node or self.lines[counter].start_node == node:
                        self.canvas.delete(self.lines[counter].line)
                        self.lines.remove(self.lines[counter])
                    else:
                        counter += 1
                self.nodes.remove(node)

    def is_in_circle(self, x, y):
        for node in self.nodes:
            if (x-node.x)**2 + (y-node.y)**2 <= 100:
                return True
        return False

    def is_on_line(self, x, y):
        for line in self.lines:
            if abs(line.k*x+line.b) <= abs(y)+2:
                return True
        return False

    def draw_line_between_two_circles(self, event):
        self.unbind_all()
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.draw_line)

    def unbind_all(self):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<Double-Button-1>")

if __name__ == "__main__":
    root = Tk()
    ex = GraphEditor()
    root.geometry("1000x800")
    root.mainloop()
