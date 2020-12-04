import arcpy
import heapq
from math import sqrt
from sys import maxsize
from model import MAXIMUM_SPEED


def f_edge_cost_quickest():
    return lambda e: e.get_time()


def f_edge_cost_shortest():
    return lambda e: e.get_length()


def f_heuristic_quickest():
    return lambda curr, end: sqrt((curr.x - end.x) * (curr.x - end.x) + (curr.y - end.y) * (curr.y - end.y)) /\
                             MAXIMUM_SPEED


def f_heuristic_shortest():
    return lambda curr, end: sqrt((curr.x - end.x) * (curr.x - end.x) + (curr.y - end.y) * (curr.y - end.y))


def f_heuristic_zero():
    return lambda curr, end: 0


def visualize_path(fid_path, input_shp, output_shp):
    fid_str = ''
    for fid in fid_path:
        fid_str = fid_str + str(fid) + ', '
    fid_str = fid_str[:-2]

    arcpy.MakeFeatureLayer_management(input_shp, 'temp.lyr')

    arcpy.SelectLayerByAttribute_management('temp.lyr', 'NEW_SELECTION', '"FID" in ({})'.format(fid_str))

    arcpy.CopyFeatures_management('temp.lyr', output_shp)
    arcpy.Delete_management('temp.lyr')


def pathfinding_a_star(graph, start_id, end_id, edge_cost_function, heuristics_function):
    q_list = []  # not processed neighbours of previous nodes
    neighbours_map = {}  # map of not processed neighbours - used for quicker access to data

    f_score = {}  # value of a path from the start node to the current node with heuristics
    g_score = {}  # value of a path from the start node to the current node without heuristics
    p = {}  # previous node in a path
    for node in graph.nodes:
        f_score[node.id] = maxsize
        g_score[node.id] = maxsize
        p[node.id] = -1
        neighbours_map[node.id] = False

    current_node = graph.get_node_by_id(start_id)

    g_score[start_id] = 0
    f_score[start_id] = heuristics_function(current_node, graph.get_node_by_id(end_id))

    heapq.heappush(q_list, [f_score[start_id], start_id])  # create heapq from q_list
    neighbours_map[start_id] = True

    while len(q_list) != 0:
        current_node_id = heapq.heappop(q_list)[1]  # get id of a node from q_list with the lowest path value

        while not neighbours_map[current_node_id]:  # check if node was already visited
            current_node_id = heapq.heappop(q_list)[1]

        current_node = graph.get_node_by_id(current_node_id)

        if current_node_id == end_id:
            break

        neighbours_map[current_node.id] = False
        neighbouring_edges = [el[1] for el in graph.get_neighbours(current_node_id)]

        for edge_id in neighbouring_edges:
            edge = graph.get_edge_by_id(edge_id)

            next_node_id = edge.get_end(current_node_id)
            next_node = graph.get_node_by_id(next_node_id)

            h_value = heuristics_function(next_node, graph.get_node_by_id(end_id))
            edge_cost = edge_cost_function(edge)

            tentative_g_score = g_score[current_node.id] + edge_cost
            if tentative_g_score < g_score[next_node.id]:
                p[next_node.id] = edge_id
                g_score[next_node.id] = tentative_g_score
                f_score[next_node.id] = g_score[next_node.id] + h_value

                heapq.heappush(q_list, [f_score[next_node.id], next_node.id])
                neighbours_map[next_node.id] = True

    # reconstruct the path form end to start node
    curr_node_id = end_id
    path = []
    while curr_node_id != start_id:
        curr_edge_id = p[curr_node_id]
        edge = graph.get_edge_by_id(curr_edge_id)
        prev_node_id = curr_node_id

        curr_node_id = edge.to_node_id
        if prev_node_id == curr_node_id:
            curr_node_id = edge.from_node_id

        path.append(edge.id)

    print g_score[end_id]  # get the value of the shortest/quickest path

    return path


def range_algorithm(graph, start_id, edge_cost_function, end_time):
    q_list = []  # not processed neighbours of previous nodes
    neighbours_map = {}  # map of not processed neighbours - used for quicker access to data

    g_score = {}  # value of a path from the start node to the current node without heuristics
    p = {}  # previous node in a path
    for node in graph.nodes:
        g_score[node.id] = maxsize
        p[node.id] = -1
        neighbours_map[node.id] = False

    g_score[start_id] = 0

    heapq.heappush(q_list, [g_score[start_id], start_id])  # create heapq from q_list
    neighbours_map[start_id] = True

    while len(q_list) != 0:
        current_node_id = heapq.heappop(q_list)[1]  # get id of a node from q_list with the lowest path value

        while not neighbours_map[current_node_id] and g_score[current_node_id] < 2 * end_time:  # check if node was
            # already visited
            current_node_id = heapq.heappop(q_list)[1]

        current_node = graph.get_node_by_id(current_node_id)

        neighbours_map[current_node.id] = False
        neighbouring_edges = [el[1] for el in graph.get_neighbours(current_node_id)]

        for edge_id in neighbouring_edges:
            edge = graph.get_edge_by_id(edge_id)

            next_node_id = edge.get_end(current_node_id)
            next_node = graph.get_node_by_id(next_node_id)

            edge_cost = edge_cost_function(edge)

            tentative_g_score = g_score[current_node.id] + edge_cost
            if tentative_g_score < g_score[next_node.id]:
                p[next_node.id] = edge_id
                g_score[next_node.id] = tentative_g_score

                heapq.heappush(q_list, [g_score[next_node.id], next_node.id])
                neighbours_map[next_node.id] = True

    nodes_in_range = {}
    edges_in_range = []
    for p in g_score:
        if g_score[p] < 2 * end_time:
            neighbour_edges = [el[1] for el in graph.get_neighbours(p)]
            edges_in_range += neighbour_edges
            nodes_in_range[p] = g_score[p]

    edges_in_range = list(set(edges_in_range))  # to eliminate duplicated edges
    edges_avg_time = {}
    for e in edges_in_range:
        node_start_time = g_score[graph.get_edge_by_id(e).from_node_id]
        node_end_time = g_score[graph.get_edge_by_id(e).to_node_id]
        edges_avg_time[e] = (node_start_time + node_end_time) / 2

    return nodes_in_range, edges_avg_time


def visualize_range(tin, output_shp, roads_shp, travel_time, edge_average_time):
    points = []
    for row in arcpy.da.SearchCursor(roads_shp, ["SHAPE@", "FID"]):
        if row[1] in edge_average_time:
            edge_id = row[1]
            mid_point = (row[0].positionAlongLine(0.50, True).firstPoint.X,
                         row[0].positionAlongLine(0.50, True).firstPoint.Y)

            travel_time[mid_point] = edge_average_time[edge_id]

    cursor = arcpy.InsertCursor(output_shp, ['Id', 'SHAPE', 'Distance'])
    for point in travel_time:
        points.append(point)

    for point in points:
        row = cursor.newRow()
        row.setValue('Id', points.index(point))
        row.setValue('SHAPE', arcpy.Point(point[0], point[1]))
        row.setValue('Distance', travel_time[point])
        cursor.insertRow(row)

    del cursor
    del row

    projection = arcpy.Describe(roads_shp).spatialReference

    arcpy.CreateTin_3d(tin, projection,
                       'output\\range.shp Distance Mass_Points <None>',
                       'CONSTRAINED_DELAUNAY')  # visualisation via tin


def create_output_shapefile(shp_name, proj):
    arcpy.Delete_management(shp_name)
    arcpy.CreateFeatureclass_management(arcpy.env.workspace, shp_name, 'POINT', '', '', '', proj)
    arcpy.AddField_management(shp_name, 'Id', 'LONG')
    arcpy.AddField_management(shp_name, 'Distance', 'FLOAT', 10, 10)

    return shp_name
