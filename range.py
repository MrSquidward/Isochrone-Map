from arcpy_integration import *
from algorithms import *


arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension('Spatial')
arcpy.CheckOutExtension('3D')

# input data
roads_shp = 'input/L4_1_BDOT10k__OT_SKJZ_L.shp'
points_shp = 'input/range_point.shp'
output_dir = r'output'
requested_time = 5  # minutes

points_output_file = r'\range_points.shp'
points_output_path = output_dir + points_output_file
tin_output_file = output_dir + r'\range'

projection = arcpy.Describe(roads_shp).spatialReference
create_output_shapefile(output_dir, points_output_file, projection)

graph = roads_shp_to_graph(roads_shp)

points = {}
for row in arcpy.da.SearchCursor(points_shp, ["SHAPE@XY", "FID"]):
    points[row[1]] = row[0]

start_point = graph.get_closest_node(points[0][0], points[0][1])
edge_cost_fun = edge_cost_quickest()

travel_range, mid_of_edges = range_algorithm(graph, start_point, edge_cost_fun, requested_time)

visualize_range(tin_output_file, points_output_path, roads_shp, travel_range, mid_of_edges)
