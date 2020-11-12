import arcpy
import heapq
from sys import maxsize
from model import AVERAGE_SPEED


def visualize_path(fid_path, input_shp, output_shp):
    fid_str = ''
    for fid in fid_path:
        fid_str = fid_str + str(fid) + ', '
    fid_str = fid_str[:-2]

    arcpy.MakeFeatureLayer_management(input_shp, 'temp.lyr')

    arcpy.SelectLayerByAttribute_management('temp.lyr', 'NEW_SELECTION', '"FID" in ({})'.format(fid_str))

    arcpy.CopyFeatures_management('temp.lyr', output_shp)
    arcpy.Delete_management('temp.lyr')


def pathfinding_a_star(graph, start_id, end_id, the_shortest=True):
    q_list = []  # not processed neighbours of previous nodes
    neighbours_map = {}  # map of not processed neighbours - used for quicker access to data

    f_score = {}  # value of a path from the start node to the current node with heuristics
    g_score = {}  # value of a path from the start node to the current node without heuristics
    p = {}  # previous node in a path
    for node in graph.nodes:
        f_score[node.id] = maxsize
        g_score[node.id] = maxsize
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
            if the_shortest:
                h_value = next_node.heuristic_cost(graph.get_node_by_id(end_id).x, graph.get_node_by_id(end_id).y)
            else:
                h_value = next_node.heuristic_cost(graph.get_node_by_id(end_id).x, graph.get_node_by_id(end_id).y)
                h_value /= AVERAGE_SPEED  # corrects heuristics for quickest path variant

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

    print g_score[end_id]  # get the value of the shortest/quickest path

    return path
