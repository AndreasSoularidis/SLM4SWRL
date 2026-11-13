from email import parser

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from translators.swrl_translation_factory import SWRLTranslatorFactory
from utils.config import TranslatorConfig
from rag.embeddings_rag import EmbeddingsRAG
from rag.graph_rag import GraphRAG, RAGEngineInterface
from infrastructure.neo4j_connector import Neo4jConnector
from utils.ontology_analyzer import OntologyAnalyzer
import argparse
import json
import os

# Load environment variables from the correct location
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
env_path = os.path.join(PROJECT_ROOT, 'data', 'config', '.env')
load_dotenv(env_path)

def parse_arguments():
  parser = argparse.ArgumentParser(description="Run the SWRL translator")
  parser.add_argument("--model", default="ministral", help="Specify the model to use. Available options 'llama', 'mistral', 'qwen', 'ministral', 'gemma', 'gpt', etc.")
  parser.add_argument("--rag-type", default="embeddings", help="Specify the RAG type to use. Available options 'embeddings' or 'graph'")
  parser.add_argument("--serialization", default="turtle", help="Specify the serialization format if needed. Available options 'turtle', 'rdfxml', 'manchester'")
  parser.add_argument("--domain", default="SAR", help="Specify the domain to use. Available options 'SAR' or 'PARKINSON'.")
  parser.add_argument("--iterations", default=1, help="Number of iterations.")
  return parser.parse_args()


ARGS = parse_arguments()
MODEL = ARGS.model
RAG_TYPE = ARGS.rag_type
SERIALIZATION = ARGS.serialization
DOMAIN = ARGS.domain
ITERATIONS =  int(ARGS.iterations)

def get_ontology_file_for_domain(ontology_dir: str, domain: str) -> str:
  """Get the ontology file path based on domain"""
  match domain:
    case "PARKINSON":
      ontology_name = "Wear4PDmoveOnto"
    case "SAR":
      ontology_name = "beAWARE"
    case "FWP":
      ontology_name = "fwp_ontology"
    case "AUTOMATION":
      ontology_name = "Automation-I4.0-Ontology"
    case _:
      raise ValueError(f"Unknown domain: {domain}")
  
  return os.path.join(ontology_dir, f"{ontology_name}.owl")


def setup_rag_engine(config: TranslatorConfig) -> RAGEngineInterface:
  """Setup the appropriate RAG engine based on configuration"""
  
  if RAG_TYPE == "embeddings":
    return EmbeddingsRAG(
      ontology_path=config.ontology_path,
      domain=DOMAIN,
      embeddings_model=OpenAIEmbeddings(),
      serialization=SERIALIZATION,
      chunk_size=config.chunk_size,
      chunk_overlap=config.chunk_overlap,
      search_type=config.search_type,
      k=config.k
    )
  elif RAG_TYPE == "graph":
    neo4j_conn = Neo4jConnector(
      uri=config.neo4j_uri,
      username=config.neo4j_user,
      password=config.neo4j_password
    )
    return GraphRAG(
      model_name=MODEL,
      temperature=config.temperature,
      neo4j_connector=neo4j_conn,
      mode= "LOCAL" if MODEL != "gpt" else "API"
    )
  else:
    raise ValueError(f"Unknown translator type: {RAG_TYPE}")


def main():
  config = TranslatorConfig(rag_type=RAG_TYPE, domain=DOMAIN)
  
  print(f"Using {RAG_TYPE} translator with {MODEL}")
  
  # Load rules
  with open(config.rules_file, "r") as file:
    rules_in_nl = json.load(file)
  rules = rules_in_nl[config.rules_category]
  
  # Setup RAG engine
  rag_engine = setup_rag_engine(config)
  
  # Setup ontology analyzer (only if needed)
  ontology_analyzer = None
  if RAG_TYPE == "graph" and config.ontology_path:
    ontology_file = get_ontology_file_for_domain(config.ontology_path, DOMAIN)
    ontology_analyzer = OntologyAnalyzer(ontology_file)
  
  # Create translator using factory
  translator = SWRLTranslatorFactory.create(
    translator_type=RAG_TYPE,
    model_name=MODEL,
    temperature=config.temperature,
    rag_engine=rag_engine,
    mode="LOCAL" if MODEL != "gpt" else "API",
    ontology_analyzer=ontology_analyzer
  )
  
  # Generate SWRL rules
  for _ in range(ITERATIONS):  # Run multiple times to test consistency
    for index, rule in enumerate(rules, 1):
      print(f"\nRule {index}:")
      print(f"Natural Language: {rule}\n")
      print("SWRL rule:")
      translator.generate_swrl(rule)
      print("\n" + "="*80)


if __name__ == "__main__":
  main()
