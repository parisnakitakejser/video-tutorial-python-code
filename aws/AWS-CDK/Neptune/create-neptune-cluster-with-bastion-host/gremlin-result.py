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

# Execute a Gremlin query to retrieve vertices with the "Company" label
result = g.V().hasLabel("person").valueMap().toList()
print(result)
