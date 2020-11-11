import math
import sys

import heapq

SPEED_ARRAY = {'G' : 50 * 1000 / 60 * 0.9, 'Z' : 50 * 1000 / 60 * 1.1, 'L' : 45 * 1000 / 60, 'D' : 40, 'I' : 50 * 1000 / 60, 'GP' : 70 * 1000 / 60, 'S' : 120 * 1000 / 60 * 1.1, 'A' : 140 * 1000 / 60 * 1.1}


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
    def __init__(self, f_node, t_node, c, fid, road_cl = 'G', d=0):
        self.from_node_id = f_node
        self.to_node_id = t_node
        self.id = (f_node, t_node)
        self.length = c
        self.direction = d
        self.FID = fid
        self.speed = SPEED_ARRAY[road_cl]
        self.time = c / SPEED_ARRAY[road_cl]

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
        min_dist = sys.maxsize
        id_of_min_dist = (-1, -1)
        for n in self.nodes:
            if math.sqrt((pt_x - n.x) * (pt_x - n.x) + (pt_y - n.y) * (pt_y - n.y)) < min_dist:
                min_dist = math.sqrt((pt_x - n.x) * (pt_x - n.x) + (pt_y - n.y) * (pt_y - n.y))
                id_of_min_dist = n.id

        return id_of_min_dist


def pathfinding_a_star(graph, start_id, end_id, the_shortest = True):
    q_list = []  # not processed neighbours of previous nodes
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
    heapq.heappush(q_list, [f_score[start_id], start_id])  # create heapq from q_list
    neighbours_map[start_id] = True

    while len(q_list) != 0:
        current_node_id = heapq.heappop(q_list)[1]  # get id of a node from q_list with the lowest path value
        current_node = graph.get_node_by_id(current_node_id)

        if current_node_id == end_id:
            break

        neighbours_map[current_node.id] = False
        neighbouring_nodes = [el[0] for el in graph.get_neighbours(current_node_id)]

        for node in neighbouring_nodes:
            next_node = graph.get_node_by_id(node)
            h_value = next_node.heuristic_cost(graph.get_node_by_id(end_id).x, graph.get_node_by_id(end_id).y)

            try:
                if the_shortest:
                    edge_cost = graph.get_edge_by_id((current_node.id, next_node.id)).get_length()
                else:
                    edge_cost = graph.get_edge_by_id((current_node.id, next_node.id)).get_time()
            except KeyError:
                if the_shortest:
                    edge_cost = graph.get_edge_by_id((next_node.id, current_node.id)).get_length()
                else:
                    edge_cost = graph.get_edge_by_id((next_node.id, current_node.id)).get_time()
            tentative_g_score = g_score[current_node.id] + edge_cost
            if tentative_g_score < g_score[next_node.id]:
                p[next_node.id] = current_node.id
                g_score[next_node.id] = tentative_g_score
                f_score[next_node.id] = g_score[next_node.id] + h_value

                if not neighbours_map[next_node.id]:
                    heapq.heappush(q_list, [f_score[next_node.id], next_node.id])
                    neighbours_map[next_node.id] = True

    # reconstruct the path form end to start node
    curr_node_id = end_id
    path = []
    while curr_node_id != start_id:
        prev_node_id = curr_node_id
        curr_node_id = p[curr_node_id]
        e_fid = graph.get_fid_from_nodes_id(curr_node_id, prev_node_id)
        path.append(e_fid)

    print g_score[end_id]  # get the value of the shortest path

    return path
