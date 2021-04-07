from arcpy_integration import *
from algorithms import *


arcpy.env.overwriteOutput = True

# input data
roads_shp = 'input/L4_1_BDOT10k__OT_SKJZ_L.shp'
points_shp = 'input/input_points.shp'
output_shp = 'output/found_path.shp'
shortest = False

graph = roads_shp_to_graph(roads_shp)

points = {}
with arcpy.da.SearchCursor(points_shp, ["SHAPE@XY", "FID"]) as cursor:
    for row in cursor:
        points[row[1]] = row[0]

start_point = graph.get_closest_node(points[0][0], points[0][1])
end_point = graph.get_closest_node(points[1][0], points[1][1])

if shortest:
    heuristic_func = heuristic_shortest()
    edge_cost_func = edge_cost_shortest()
else:
    heuristic_func = heuristic_quickest()
    edge_cost_func = edge_cost_quickest()

found_path = pathfinding_a_star(graph, start_point, end_point, edge_cost_func, heuristic_func)
visualize_path(found_path, roads_shp, output_shp)
