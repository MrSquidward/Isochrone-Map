import math
import sys
import copy


def find_node(node_list, x, y):
    for node in node_list:
        if node.x == x and node.y == y:
            return node

    return None


def find_neighbours(node_list, n):
    node_neighbours = []
    n_i = n.x
    n_j = n.y

    n1 = find_node(node_list, n_i - 1, n_j)
    if n1 is not None:
        node_neighbours.append(n1)

    n2 = find_node(node_list, n_i + 1, n_j)
    if n2 is not None:
        node_neighbours.append(n2)

    n3 = find_node(node_list, n_i, n_j - 1)
    if n3 is not None:
        node_neighbours.append(n3)

    n4 = find_node(node_list, n_i, n_j + 1)
    if n4 is not None:
        node_neighbours.append(n4)

    return node_neighbours


def extract_minimum(q, d):
    extracted_q = [(n.x, n.y) for n in q]
    extract = {}
    for id, value in d.items():
        if id in extracted_q:
            extract[id] = value

    return min(extract, key=d.get)


class Graph:
    def __init__(self, e, n):
        self.edges = e
        self.nodes = n

    def pathfinding_dijkstra(self, start, end):
        s_list = []  # processed nodes
        q_list = copy.copy(self.nodes)  # not processed nodes

        d = {}  # value of a path from the start node to the current node
        for n in self.nodes:
            d[(n.x, n.y)] = sys.maxsize
        d[(start.x, start.y)] = 0

        p = {}  # previous node in a path
        for n in self.nodes:
            p[(n.x, n.y)] = (-1, -1)

        while len(q_list) != 0:
            current_node_id = extract_minimum(q_list, d)
            current_node = find_node(q_list, current_node_id[0], current_node_id[1])
            q_list.remove(current_node)
            s_list.append(current_node)

            for edge in current_node.edges:
                next_node_id = (edge.to_node.x, edge.to_node.y)
                if d[next_node_id] > d[current_node_id] + edge.cost:
                    d[next_node_id] = d[current_node_id] + edge.cost
                    p[next_node_id] = current_node_id

        curr_node_id = (end.x, end.y)
        path = [curr_node_id]
        while curr_node_id != (start.x, start.y):
            curr_node_id = p[curr_node_id]
            path.append(curr_node_id)

        print('d:', d[(end.x, end.y)])
        return path

    def pathfinding_a_star(self, start, end):
        s_list = set()  # processed nodes
        q_list = set()  # not processed nodes

        d = {}  # value of a path from the start node to the current node
        for n in self.nodes:
            d[(n.x, n.y)] = sys.maxsize
        d[(start.x, start.y)] = 0

        p = {}  # previous node in a path
        for n in self.nodes:
            p[(n.x, n.y)] = (-1, -1)

        current_node = start
        s_list.add(start)
        q_list.add(start)
        current_node_id = (current_node.x, current_node.y)
        while (current_node.x, current_node.y) != (end.x, end.y):
            for edge in current_node.edges:
                next_node_id = (edge.to_node.x, edge.to_node.y)
                next_node = find_node(self.nodes, next_node_id[0], next_node_id[1])
                h_value = next_node.heuristic_cost(end.x, end.y)
                if next_node not in s_list:
                    if d[next_node_id] > d[current_node_id] + edge.cost + h_value:
                        d[next_node_id] = d[current_node_id] + edge.cost
                        q_list.add(next_node)
                        p[next_node_id] = current_node_id

            q_list.remove(current_node)

            current_node_id = extract_minimum(q_list, d)
            current_node = find_node(q_list, current_node_id[0], current_node_id[1])

            s_list.add(current_node)

        curr_node_id = (end.x, end.y)
        path = [curr_node_id]
        while curr_node_id != (start.x, start.y):
            curr_node_id = p[curr_node_id]
            path.append(curr_node_id)
        print('end cost', d[(end.x, end.y)])
        return path


class Edge:
    def __init__(self, f_node, t_node, c):
        self.from_node = f_node
        self.to_node = t_node
        self.cost = c


class Node:
    def __init__(self, x, y, v, e):
        self.x = x
        self.y = y
        self.value = v
        self.edges = e

    def heuristic_cost(self, hx, hy, manhattan=True):
        x_diff = abs(self.x - hx)
        y_diff = abs(self.y - hy)

        if manhattan:
            return x_diff + y_diff

        return math.sqrt(x_diff ** 2 + y_diff ** 2)


# read file with nodes
f = open('graph40.txt')

input_edges = []
for line in f:
    row = [int(x) for x in line.split()]
    input_edges.append(row)


# convert table with input values to Node object
nodes = []
for i, row in enumerate(input_edges):
    for j, val in enumerate(row):
        nodes.append(Node(i, j, val, []))

# build edges for nodes in nodes[]
edges = []
for node in nodes:
    neighbours = find_neighbours(nodes, node)
    one_node_edges = []
    for n in neighbours:
        edge_cost = (node.value + n.value) / 2
        one_node_edges.append(Edge(node, n, edge_cost))

    node.edges = one_node_edges
    edges.append(one_node_edges)

main_graph = Graph(edges, nodes)
main_path = main_graph.pathfinding_a_star(main_graph.nodes[0], main_graph.nodes[-1])
main_path2 = main_graph.pathfinding_dijkstra(main_graph.nodes[0], main_graph.nodes[-1])
print('a*:', main_path, len(main_path))
print('d:', main_path2, len(main_path2))


