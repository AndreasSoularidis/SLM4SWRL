"""
Example: Using SWRL Translator with Factory Pattern
"""
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from swrl_translation_factory import SWRLTranslatorFactory
from config import TranslatorConfig
from embeddings_rag import EmbeddingsRAG
from graph_rag import GraphRAG, RAGEngineInterface
from neo4j_connector import Neo4jConnector
from ontology_analyzer import OntologyAnalyzer
import json

load_dotenv()


def setup_rag_engine(config: TranslatorConfig) -> RAGEngineInterface:
  """Setup the appropriate RAG engine based on configuration"""
  
  if config.rag_type == "embeddings":
      return EmbeddingsRAG(
          documents=config.rag_data_path,
          embeddings_model=OpenAIEmbeddings(),
          chunk_size=config.chunk_size,
          chunk_overlap=config.chunk_overlap,
          search_type=config.search_type,
          k=config.k
      )
  elif config.rag_type == "graph":
      neo4j_conn = Neo4jConnector(
          uri=config.neo4j_uri,
          username=config.neo4j_user,
          password=config.neo4j_password
      )
      return GraphRAG(
          model_name=config.model_name,
          temperature=config.temperature,
          neo4j_connector=neo4j_conn
      )
  else:
    raise ValueError(f"Unknown translator type: {config.rag_type}")


def main():
  config = TranslatorConfig()
  
  print(f"Using {config.rag_type} translator with {config.model_name}")
  
  # Load rules
  with open(config.rules_file, "r") as file:
    rules_in_nl = json.load(file)
  rules = rules_in_nl[config.rules_category]
  
  # Setup RAG engine
  rag_engine = setup_rag_engine(config)
  
  # Setup ontology analyzer (only if needed)
  ontology_analyzer = None
  if config.rag_type == "graph" and config.ontology_path:
    ontology_analyzer = OntologyAnalyzer(config.ontology_path)
  
  # Create translator using factory
  translator = SWRLTranslatorFactory.create(
    translator_type=config.rag_type,
    model_name=config.model_name,
    temperature=config.temperature,
    rag_engine=rag_engine,
    mode=config.mode,
    ontology_analyzer=ontology_analyzer
  )
  
  # Generate SWRL rules
  for index, rule in enumerate(rules, 1):
    print(f"\nRule {index}:")
    print(f"Natural Language: {rule}\n")
    print("SWRL rule:")
    translator.generate_swrl(rule)
    print("\n" + "="*80)


if __name__ == "__main__":
  main()
