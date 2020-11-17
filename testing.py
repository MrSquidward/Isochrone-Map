from utils import *
from model import *

# arcpy.env.workspace = r'C:\Users\user\Documents\Studia\PAG\PAG\BDOT'
arcpy.env.workspace = r'D:\pycharm\pag_arcpy\bdot_skjz'
arcpy.env.overwriteOutput = True

# roads_fc = arcpy.GetParameterAsText(0)
# points_fc = arcpy.GetParameterAsText(1)
# output_file = arcpy.GetParameterAsText(2)

roads_fc = r'input\L4_1_BDOT10k__OT_SKJZ_L.shp'
points_fc = r'input\input_points.shp'
output_file = r'output\path.shp'


edges = []  # list of edges
nodes_dict = {}  # dict of nodes

for row in arcpy.da.SearchCursor(roads_fc, ["SHAPE@", "SHAPE@LENGTH", "FID", "klasaDrogi", "kierunek"]):
    f_node = Node(round(row[0].firstPoint.X), round(row[0].firstPoint.Y))
    l_node = Node(round(row[0].lastPoint.X), round(row[0].lastPoint.Y))
    e_length = row[1]

    e = Edge(f_node.id, l_node.id, e_length, row[2], row[3], row[4])
    edges.append(e)

    nodes_dict[f_node.id] = f_node
    nodes_dict[l_node.id] = l_node

nodes = [nodes_dict[n_id] for n_id in nodes_dict]  # list of nodes

torun_skjz = Graph(edges, nodes)

points = {}
for row in arcpy.da.SearchCursor(points_fc, ["SHAPE@XY", "FID"]):
    points[row[1]] = row[0]

start_point = torun_skjz.get_closest_node(points[0][0], points[0][1])
end_point = torun_skjz.get_closest_node(points[1][0], points[1][1])

my_path = pathfinding_a_star(torun_skjz, start_point, end_point, False)

print my_path

visualize_path(my_path, roads_fc, output_file)
