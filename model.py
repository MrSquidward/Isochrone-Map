import math
import sys


class Node:
    def __init__(self, x, y, e=None):
        if e is None:
            e = []

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
    def __init__(self, f_node, t_node, c, d=0):
        self.from_node_id = f_node
        self.to_node_id = t_node
        self.id = (f_node, t_node)
        self.cost = c
        self.direction = d

    def get_end(self, one_node_id):
        if one_node_id == self.from_node_id:
            return self.to_node_id
        return self.from_node_id


class Graph:
    def __init__(self, e, n):
        self.edges = e
        self.nodes = n


def extract_minimum(q, d):
    extract = {}
    for id, value in d.items():
        if id in q:
            extract[id] = value

    return min(extract, key=d.get)


def pathfinding_a_star(graph, start_id, end_id):
    q_list = set()  # not processed neighbours of previous nodes
    neighbours_map = {}  # map of not processed neighbours - used for quicker access to data

    f_score = {}  # value of a path from the start node to the current node with heuristics
    g_score = {}  # value of a path from the start node to the current node without heuristics
    p = {}  # previous node in a path
    all_nodes = {}  # map of all nodes in graph - key is an id of node, value is an object of node
    for node in graph.nodes:
        f_score[node.id] = sys.maxsize
        g_score[node.id] = sys.maxsize
        p[node.id] = (-1, -1)
        all_nodes[node.id] = node
        neighbours_map[node.id] = False

    g_score[start_id] = 0
    current_node = all_nodes[start_id]
    f_score[start_id] = current_node.heuristic_cost(all_nodes[end_id].x, all_nodes[end_id].y)
    q_list.add(start_id)
    neighbours_map[start_id] = True

    while len(q_list) != 0:
        current_node_id = extract_minimum(q_list, f_score)  # get id of a node from q_list with the lowest path value
        current_node = all_nodes[current_node_id]

        if current_node_id == end_id:
            break

        q_list.remove(current_node.id)
        neighbours_map[current_node.id] = False

        for edge in current_node.edges:
            next_node = all_nodes[edge.to_node_id]
            h_value = next_node.heuristic_cost(all_nodes[end_id].x, all_nodes[end_id].y)
            tentative_g_score = g_score[current_node.id] + edge.cost

            if tentative_g_score < g_score[next_node.id]:
                p[next_node.id] = current_node.id
                g_score[next_node.id] = tentative_g_score
                f_score[next_node.id] = g_score[next_node.id] + h_value

                if not neighbours_map[next_node.id]:
                    q_list.add(next_node.id)
                    neighbours_map[next_node.id] = True

    # reconstruct the path form end to start node
    curr_node_id = end_id
    path = [curr_node_id]
    while curr_node_id != start_id:
        curr_node_id = p[curr_node_id]
        path.append(curr_node_id)

    print g_score[end_id]  # get the value of the shortest path

    return path
