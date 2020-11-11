import arcpy
from model import *

arcpy.env.workspace = r'D:\pycharm\pag_arcpy\bdot_skjz'
arcpy.env.overwriteOutput = True

roads_fc = 'L4_1_BDOT10k__OT_SKJZ_L.shp'

points = []  # list of all points
edges = []  # list of edges
d = {}

for row in arcpy.da.SearchCursor(roads_fc, ["SHAPE@", "SHAPE@LENGTH", "FID", "klasaDrogi", "kierunek"]):
    f_node = Node(round(row[0].firstPoint.X), round(row[0].firstPoint.Y))
    l_node = Node(round(row[0].lastPoint.X), round(row[0].lastPoint.Y))
    e_length = row[1]
    e = Edge(f_node.id, l_node.id, e_length, row[2], row[3], row[4])
    edges.append(e)
    d[f_node.id] = f_node
    d[l_node.id] = l_node

nodes = []  # list of nodes
for i in d:
    nodes.append(d[i])

torun_skjz = Graph(edges, nodes)
start_point = torun_skjz.get_closest_node(474015.240, 572269.582)
end_point = torun_skjz.get_closest_node(474076.359, 572436.534)
# start_point = torun_skjz.get_closest_node(472298, 573122)
# end_point = torun_skjz.get_closest_node(472421, 573194)
my_path = pathfinding_a_star(torun_skjz, start_point, end_point, False)

print my_path
print start_point
print end_point