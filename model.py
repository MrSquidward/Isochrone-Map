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

    def heuristic_cost(self, hx, hy, manhattan=False):
        x_diff = abs(self.x - hx)
        y_diff = abs(self.y - hy)

        if manhattan:
            return x_diff + y_diff

        return math.sqrt(x_diff ** 2 + y_diff ** 2)


class Edge:
    def __init__(self, f_node, t_node, c, FID, d=0):
        self.from_node_id = f_node
        self.to_node_id = t_node
        self.id = (f_node, t_node)
        self.cost = c
        self.direction = d
        self.fid = FID

    def get_end(self, one_node_id):
        if one_node_id == self.from_node_id:
            return self.to_node_id
        return self.from_node_id

    def get_cost(self):
        return self.cost

    # def get_time_cost(self):
    #     return self.cost /


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
            if edge.id not in nodes_edges[edge.from_node_id]:
                nodes_edges[edge.from_node_id].append(edge.id)
            if edge.id not in nodes_edges[edge.to_node_id]:
                nodes_edges[edge.to_node_id].append(edge.id)

        for node in self.nodes:
            node.edges = nodes_edges[node.id]

    def get_node_by_id(self, node_id):
        return self.dict_of_nodes_by_id[node_id]

    def get_edge_by_id(self, edge_id):
        return self.dict_of_edges_by_id[edge_id]

    def get_neighbours(self, node_id):
        neighbour_edges = self.dict_of_nodes_by_id[node_id].edges
        neighbour_nodes = []
        for edge in neighbour_edges:
            neighbour_nodes.append(self.get_edge_by_id(edge).get_end(node_id))

        return_list = []
        for index in range(0, len(neighbour_nodes)):
            return_list.append((neighbour_nodes[index], neighbour_edges[index]))

        return return_list

    def get_closest_node(self, my_x, my_y):
        final_list = sorted(self.nodes, key=lambda node: math.sqrt(abs(my_x - node.x) ** 2 + abs(my_y - node.y) ** 2))
        return final_list[0]


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
    for node in graph.nodes:
        f_score[node.id] = sys.maxsize
        g_score[node.id] = sys.maxsize
        p[node.id] = (-1, -1)
        neighbours_map[node.id] = False

    g_score[start_id] = 0
    current_node = graph.get_node_by_id(start_id)
    f_score[start_id] = current_node.heuristic_cost(graph.get_node_by_id(end_id).x, graph.get_node_by_id(end_id).y)
    q_list.add(start_id)
    neighbours_map[start_id] = True

    while len(q_list) != 0:
        current_node_id = extract_minimum(q_list, f_score)  # get id of a node from q_list with the lowest path value
        current_node = graph.get_node_by_id(current_node_id)

        if current_node_id == end_id:
            break

        q_list.remove(current_node.id)
        neighbours_map[current_node.id] = False
        neighbouring_nodes = []
        for el in graph.get_neighbours(current_node.id):
            neighbouring_nodes.append(el[0])

        for node in neighbouring_nodes:
            next_node = graph.get_node_by_id(node)
            h_value = next_node.heuristic_cost(graph.get_node_by_id(end_id).x, graph.get_node_by_id(end_id).y)

            try:
                edge_cost = graph.get_edge_by_id((current_node.id, next_node.id)).get_cost()
            except KeyError:
                edge_cost = graph.get_edge_by_id((next_node.id, current_node.id)).get_cost()
            
            tentative_g_score = g_score[current_node.id] + edge_cost
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
