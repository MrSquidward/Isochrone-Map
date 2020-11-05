import arcpy

arcpy.env.workspace = r'D:\pycharm\pag_algorythm\BDOT_Torun'
arcpy.env.overwriteOutput = True

roads_fc = 'L4_1_BDOT10k__OT_SKDR_L.shp'

# for row in arcpy.SearchCursor(roads_fc):
#     # Print the current polygon or polyline's ID
#     print("FID {}:".format(row.getValue('FID')))
#     startpt = row.getValue('SHAPE@XY').firstPoint

for row in arcpy.da.SearchCursor(roads_fc, ["SHAPE@"]):
    print(row[0].firstPoint.X)
    print(row[0].getPart(0)[0].X)

    # print(row[0].getPart(0)[-1].X)
    # print "x: ", abs(row[0].getPart(0)[0].X - row[0].getPart(0)[-1].X)
