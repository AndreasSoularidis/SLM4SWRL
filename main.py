from dotenv import load_dotenv
from SLM4SWRL import SLM4SWRL
from graph_rag import GraphRAG
from neo4j_connector import Neo4jConnector
from ontology_analyzer import OntologyAnalyzer
import json
import os

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

with open("./rules_in_natural_language.json", "r") as file:
  rules_in_nl = json.load(file)

rules = rules_in_nl["PARKINSON"]

ontology_analyzer = OntologyAnalyzer("./ontologies/Wear4PDmoveOnto_turtle.txt")
rag_engine = GraphRAG(
  model_name="llama",
  temperature=0.0, 
  neo4j_connector=Neo4jConnector(uri=NEO4J_URI, username=NEO4J_USER, password=NEO4J_PASSWORD)
)

app = SLM4SWRL(
  model_name="llama",
  temperature=0.0,
  ontology_analyser=ontology_analyzer,
  rag_engine=rag_engine,
  mode="LOCAL")


for rule in rules:
  print(f"Natural Language: {rule}")
  print(f"\nSWRL rule:")
  app.generate_swrl(rule)
  print("\n")
