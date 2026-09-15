from langchain_neo4j import Neo4jGraph
from neo4j import GraphDatabase


class Neo4jConnector:
  def __init__(self, uri: str, username: str, password: str, enhanced_schema: bool = True):
    self.graph = Neo4jGraph(url=uri, username=username, password=password, enhanced_schema=enhanced_schema)
    schema = self.graph.get_structured_schema
    nodes = schema['node_props']
    filtered_nodes = [node for node in nodes if node.startswith("owl")]
    entities = "(n:" + "|".join(filtered_nodes) + ")"
    self.query(f"CREATE FULLTEXT INDEX ontology IF NOT EXISTS FOR {entities} ON EACH [n.rdfs__label]")

  def close(self):
    self.graph.close()

  def query(self, query: str, parameters: dict = None) -> list:
    result = self.graph.query(query, parameters)
    return result