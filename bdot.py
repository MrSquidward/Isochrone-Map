import arcpy
from model import *

arcpy.env.workspace = r'D:\pycharm\pag_algorythm\BDOT_Torun'
arcpy.env.overwriteOutput = True

roads_fc = 'L4_1_BDOT10k__OT_SKJZ_L.shp'

# for row in arcpy.SearchCursor(roads_fc):
#     # Print the current polygon or polyline's ID
#     print("FID {}:".format(row.getValue('FID')))
#     startpt = row.getValue('SHAPE@XY').firstPoint
# print(row[0].firstPoint.X)
# print(row[0].getPart(0)[0].X)

points = []  # list of all points
edges = []  # list of edges
d = {}
for row in arcpy.da.SearchCursor(roads_fc, ["SHAPE@", "SHAPE@LENGTH"]):
    f_node = Node(int(row[0].firstPoint.X), int(row[0].firstPoint.Y))
    l_node = Node(int(row[0].lastPoint.X), int(row[0].lastPoint.Y))
    e_length = row[1]
    e = Edge(f_node.id, l_node.id, e_length)
    edges.append(e)
    d[f_node.id] = f_node
    d[l_node.id] = l_node

nodes = []  # list of nodes
for i in d:
    nodes.append(d[i])

nodes_edges = {}
for node in nodes:
    nodes_edges[node.id] = []

for edge in edges:
    if edge.id not in nodes_edges[edge.from_node_id]:
        nodes_edges[edge.from_node_id].append(edge.id)
    if edge.id not in nodes_edges[edge.to_node_id]:
        nodes_edges[edge.to_node_id].append(edge.id)

# for edge in edges:
#     if edge.id not in nodes_edges[edge.from_node_id]:
#         temp = nodes_edges[edge.from_node_id]
#         temp.append(edge.id)
#         nodes_edges[edge.from_node_id] = temp
#     if edge.id not in nodes_edges[edge.to_node_id]:
#         temp = nodes_edges[edge.to_node_id]
#         temp.append(edge.id)
#         nodes_edges[edge.to_node_id] = temp

for i in nodes_edges:
    print i, len(nodes_edges[i]), nodes_edges[i]

torun_skjz = Graph(edges, nodes)
