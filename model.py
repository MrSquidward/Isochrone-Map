import math
from sys import maxsize


SPEED_ARRAY = {
    'G':  60 * 1000 / 60,
    'Z':  50 * 1000 / 60,
    'L':  45 * 1000 / 60,
    'D':  50 * 1000 / 60,
    'I':  50 * 1000 / 60,
    'GP': 70 * 1000 / 60,
    'S': 120 * 1000 / 60,
    'A': 140 * 1000 / 60
}

AVERAGE_SPEED = 80 * 1000 / 60


class Node:
    def __init__(self, x, y, e=None):
        if e is None:
            e = []

        self.x = int(x)
        self.y = int(y)
        self.id = (int(x), int(y))
        self.edges = e

    def heuristic_cost(self, hx, hy, manhattan=False):
        x_diff = abs(self.x - hx)
        y_diff = abs(self.y - hy)

        if manhattan:
            return x_diff + y_diff

        return math.sqrt(x_diff * x_diff + y_diff * y_diff)


class Edge:
    def __init__(self, f_node, t_node, c, fid, road_cl='G', d=0):
        self.from_node_id = f_node
        self.to_node_id = t_node
        self.id = (f_node, t_node)
        self.length = c
        self.direction = d
        self.FID = fid
        self.speed = SPEED_ARRAY[road_cl]
        self.time = self.length / self.speed

    def get_end(self, one_node_id):
        if one_node_id == self.from_node_id:
            return self.to_node_id
        return self.from_node_id

    def get_length(self):
        return self.length
    
    def get_time(self):
        return self.time


class Graph:
    def __init__(self, e, n):
        self.edges = e
        self.nodes = n

        self.__add_node_edges()

        self.dict_of_edges_by_id = {}
        for edge in self.edges:
            self.dict_of_edges_by_id[edge.id] = edge

        self.dict_of_nodes_by_id = {}
        for node in self.nodes:
            self.dict_of_nodes_by_id[node.id] = node

    def __add_node_edges(self):
        nodes_edges = {}
        for node in self.nodes:
            nodes_edges[node.id] = []

        for edge in self.edges:
            if edge.id not in nodes_edges[edge.from_node_id] and edge.direction < 2:
                nodes_edges[edge.from_node_id].append(edge.id)
            if edge.id not in nodes_edges[edge.to_node_id] and edge.direction in (0, 2):
                nodes_edges[edge.to_node_id].append(edge.id)

        for node in self.nodes:
            node.edges = nodes_edges[node.id]

    def get_node_by_id(self, node_id):
        return self.dict_of_nodes_by_id[node_id]

    def get_edge_by_id(self, edge_id):
        return self.dict_of_edges_by_id[edge_id]

    def get_fid_from_edge_id(self, edge_id):
        return self.dict_of_edges_by_id[edge_id].FID

    def get_fid_from_nodes_id(self, f_node, l_node):
        try:
            return self.dict_of_edges_by_id[(f_node, l_node)].FID
        except KeyError:
            return self.dict_of_edges_by_id[(l_node, f_node)].FID

    def get_neighbours(self, node_id):
        neighbour_edges = self.dict_of_nodes_by_id[node_id].edges
        neighbour_nodes = []
        for edge in neighbour_edges:
            neighbour_nodes.append(self.get_edge_by_id(edge).get_end(node_id))

        return_list = []
        for index in range(0, len(neighbour_nodes)):
            return_list.append((neighbour_nodes[index], neighbour_edges[index]))

        return return_list

    def get_closest_node(self, pt_x, pt_y):
        min_dist = maxsize
        id_of_min_dist = (-1, -1)
        for n in self.nodes:
            if math.sqrt((pt_x - n.x) * (pt_x - n.x) + (pt_y - n.y) * (pt_y - n.y)) < min_dist:
                min_dist = math.sqrt((pt_x - n.x) * (pt_x - n.x) + (pt_y - n.y) * (pt_y - n.y))
                id_of_min_dist = n.id

        return id_of_min_dist
