import os

from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph

neptune_host = os.getenv('NEPTUNE_HOST')
neptune_port = os.getenv('NEPTUNE_PORT')
protocol = os.getenv('NEPTUNE_PROTOCOL')

# Create a connection to the Gremlin server
graph = Graph()
connection = DriverRemoteConnection(f"{protocol}://{neptune_host}:{neptune_port}/gremlin", "g")
g = graph.traversal().withRemote(connection)

# Insert a new vertex
new_vertex_a = g.addV("person").property("name", "Alice").property("age", 30).next()
new_vertex_b = g.addV("person").property("name", "Bob").property("age", 35).next()

# Retrieve the vertices by ID
vertex_a = g.V(new_vertex_a).next()
vertex_b = g.V(new_vertex_b).next()

# Insert a new edge
new_edge = g.V(vertex_a).addE("knows").to(vertex_b).next()

# Commit the transaction
connection.commit()
