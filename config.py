"""
Configuration for SWRL Translator
"""
from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv
import yaml
load_dotenv()


@dataclass
class TranslatorConfig:
  """Configuration for SWRL translation"""
  with open('C:\\Andreas\\Projects\\SLM4SWRL\\config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
  
  # Translator type: "graph" or "embeddings"
  rag_type: str = config['rag_type']
  domain: str = config['domain']  # or "SAR"
  
  # Model configuration
  model_name: str = config['model']['name']
  temperature: float = config['model']['temperature']
  mode: str = config['model']['mode']
  
  # RAG configuration
  rag_data_path: str = None
  chunk_size: int = config['rag']['chunk_size']
  chunk_overlap: int = config['rag']['chunk_overlap']
  search_type: str = config['rag']['search_type']
  k: int = config['rag']['k']
  
  # Ontology configuration (for graph translator)
  ontology_path: Optional[str] = None
  ontology_format: str = config['ontology']['ontology_format']
  
  # Neo4j configuration (for graph translator)
  neo4j_uri: Optional[str] = None
  neo4j_user: Optional[str] = None
  neo4j_password: Optional[str] = None
  
  # Rules configuration
  rules_file: str = "./rules_in_natural_language.json"
  rules_category: str = None
  
  def __post_init__(self, config=config):
    """Load environment variables for Neo4j if not provided"""
    if self.rag_type == "graph":
      self.neo4j_uri = self.neo4j_uri or os.getenv("NEO4J_URI")
      self.neo4j_user = self.neo4j_user or os.getenv("NEO4J_USER")
      self.neo4j_password = self.neo4j_password or os.getenv("NEO4J_PASSWORD")
    if self.domain == "PARKINSON":
      self.ontology_path = self.ontology_path or config['ontology']['ontology_path_parkinson']
      self.rag_data_path = self.rag_data_path or config['rag']['rag_data_path_parkinson']
      self.rules_category = self.rules_category or "PARKINSON"
    elif self.domain == "SAR":
      self.ontology_path = self.ontology_path or config['ontology']['ontology_path_sar']
      self.rag_data_path = self.rag_data_path or config['rag']['rag_data_path_sar']
      self.rules_category = self.rules_category or "SAR"


