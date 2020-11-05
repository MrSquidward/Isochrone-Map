import math

class Node:
    def __init__(self, x, y, v, e):
        self.x = int(x)
        self.y = int(y)
        self.id = (int(x), int(y))
        self.edges = e

    def heuristic_cost(self, hx, hy, manhattan=True):
        x_diff = abs(self.x - hx)
        y_diff = abs(self.y - hy)

        if manhattan:
            return x_diff + y_diff

        return math.sqrt(x_diff ** 2 + y_diff ** 2)

class Edge:
    def __init__(self, f_node, t_node, c):
        self.from_node = f_node
        self.to_node = t_node
        self.edge_id = (f_node, t_node)
        self.cost = c

class Graph:
    def __init__(self, e, n):
        self.edges = e
        self.nodes = n

def extract_minimum(q, d):
    extracted_q = [(n.x, n.y) for n in q]
    extract = {}
    for id, value in d.items():
        if id in extracted_q:
            extract[id] = value

    return min(extract, key=d.get)