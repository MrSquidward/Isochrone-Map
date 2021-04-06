from arcpy_integration import *
from algorithms import *


arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension('Spatial')
arcpy.CheckOutExtension('3D')

# input data
roads_shp = 'input/L4_1_BDOT10k__OT_SKJZ_L.shp'
points_shp = 'input/range_point.shp'
output_tin_file = r'output\range_shp'
requested_time = 5  # minutes

output_path = '\\'.join(output_tin_file.split('\\')[0:-1])
points_output_file = output_path + r'\range_points.shp'

projection = arcpy.Describe(roads_shp).spatialReference
create_output_shapefile(points_output_file, projection)

graph = roads_shp_to_graph(roads_shp)

points = {}
for row in arcpy.da.SearchCursor(points_shp, ["SHAPE@XY", "FID"]):
    points[row[1]] = row[0]

start_point = graph.get_closest_node(points[0][0], points[0][1])
edge_cost_fun = edge_cost_quickest()

travel_range, mid_of_edges = range_algorithm(graph, start_point, edge_cost_fun, requested_time)

visualize_range(output_tin_file, points_output_file, roads_shp, travel_range, mid_of_edges)
