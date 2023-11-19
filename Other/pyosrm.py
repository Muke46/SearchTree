from pyrosm import OSM, get_data
import osmnx as ox

# Initialize the reader
osm = OSM(get_data("helsinki_pbf"))

# Get all walkable roads and the nodes 
nodes, edges = osm.get_network(nodes=True)

# Check first rows in the edge 
edges.head()