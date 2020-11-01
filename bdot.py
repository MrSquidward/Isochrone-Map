import arcpy

arcpy.env.workspace = r'D:\pycharm\pag_algorythm\BDOT_Torun'
arcpy.env.overwriteOutput = True

roads_fc = 'L4_1_BDOT10k__OT_SKDR_L.shp'

for row in arcpy.SearchCursor(roads_fc, ["OID@", "SHAPE@"]):
    # Print the current polygon or polyline's ID
    print("Feature {}:".format(row.getValue('FID')))
    partnum = 0

    # Step through each part of the feature
    for part in row.getValue("SHAPE@"):
        # Print the part number
        print("Part {}:".format(partnum))

        # Step through each vertex in the feature
        for pnt in part:
            if pnt:
                # Print x,y coordinates of current point
                print("{}, {}".format(pnt.X, pnt.Y))
            else:
                # If pnt is None, this represents an interior ring
                print("Interior Ring:")

        partnum += 1