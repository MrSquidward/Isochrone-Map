import arcpy
from model import *


def roads_shp_to_graph(linear_shp):
    edges = []  # list of edges
    nodes_dict = {}  # dict of nodes

    with arcpy.da.SearchCursor(linear_shp, ["SHAPE@", "SHAPE@LENGTH", "FID", "klasaDrogi", "kierunek"]) as cursor:
        for row in cursor:
            first_node = Node(round(row[0].firstPoint.X), round(row[0].firstPoint.Y))
            last_node = Node(round(row[0].lastPoint.X), round(row[0].lastPoint.Y))
            edge_length = row[1]

            edge = Edge(first_node.id, last_node.id, edge_length, row[2], row[3], row[4])
            edges.append(edge)

            nodes_dict[first_node.id] = first_node
            nodes_dict[last_node.id] = last_node

    nodes = [nodes_dict[node_id] for node_id in nodes_dict]  # list of nodes

    return Graph(edges, nodes)


def visualize_path(fid_path, input_shp, output_shp):
    fid_str = ''
    for fid in fid_path:
        fid_str = fid_str + str(fid) + ', '
    fid_str = fid_str[:-2]

    arcpy.MakeFeatureLayer_management(input_shp, 'temp.lyr')

    arcpy.SelectLayerByAttribute_management('temp.lyr', 'NEW_SELECTION', '"FID" in ({})'.format(fid_str))

    arcpy.CopyFeatures_management('temp.lyr', output_shp)
    arcpy.Delete_management('temp.lyr')


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
                       '{} Distance Mass_Points <None>'.format(output_shp),
                       'CONSTRAINED_DELAUNAY')  # visualisation via tin


def create_output_shapefile(path_to_shp, proj):
    arcpy.Delete_management(path_to_shp)

    path_to_shp_catalog = '\\'.join(path_to_shp.split('\\')[0:-1])
    shp_name = path_to_shp.split('\\')[-1]

    arcpy.CreateFeatureclass_management(path_to_shp_catalog, shp_name, 'POINT', '', '', '', proj)
    arcpy.AddField_management(path_to_shp, 'Id', 'LONG')
    arcpy.AddField_management(path_to_shp, 'Distance', 'FLOAT', 10, 10)

    return path_to_shp
