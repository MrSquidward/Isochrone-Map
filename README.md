# Isochrone-Map
The application allows you to create a graph based on a line shapefile (we used a SKJZ_L file from BDOT10k with 1 added column representing road's direction) and using this structure finds the shortest path from start point to end point. Furthermore one of the algorithm allows you to vizualize time travel isochrones (lines connecting areas of the same time required to reach them).

## Input data
When using pathfinding algorithm you need to provide into pathfinding.py file following data: 
* Line shapefile (used to create roads graph)
* Point shapefile (containing starting point and ending point)
* Output shapefile 
* Shortest/fastest path
```
roads_shp = 'input/L4_1_BDOT10k__OT_SKJZ_L.shp'
points_shp = 'input/input_points.shp'
output_shp = 'output/found_path.shp'
shortest = False
```
### Example result:
![image](https://user-images.githubusercontent.com/50464859/113927156-6572d580-97ed-11eb-82bf-f4f541c8174c.png)

When using range algorithm you need to provide into range.py file following data: 
* Line shapefile (used to create roads graph)
* Point shapefile (containing ONE starting point)
* Requested search time
* Output directory
```
roads_shp = 'input/L4_1_BDOT10k__OT_SKJZ_L.shp'
points_shp = 'input/range_point.shp'
output_dir = 'output'
requested_time = 5
```
### Example result for 3 minutes:
![image](https://user-images.githubusercontent.com/50464859/113926540-91da2200-97ec-11eb-89fb-ae68a561a23f.png)

## Pathfinding algorithm
It is based on the A* algorithm and is using our own graph model (model.py file). The user can choose whether he wants to find the quickest path or the shortest one. If you don't provide road shapefile containing road class, you don't need this option. The time needed to travel through a road is based on a maximum speed allowed on it. Starting point and ending point don't have to be one of graph's nodes. Algorithm will calculate the closest possible node in the graph.
## Range algorithm
It is based on the Dijkstra algorithm and is using our own graph model (model.py file). The user can choose requested time for which the algorithm will calculate isochrones (For vizualization purposes the algorithm will double the time given). The basic result is a point shapefile in which every point contains data about the time needed to get to it. The final vizualization is a TIN file. It is created based on the previously mentioned point shapefile (the TIN algorithm interpolate known points).

## Requirements
* You have to run files on a Python 2.7 with arcpy module installed.
* You have to install heapq module
* To visualize and check results we used an ArcMap but you can also use QGIS instead.

## Authors
* Michał Nguyen
* Antoni Gołoś
Students from Warsaw University of Technology
