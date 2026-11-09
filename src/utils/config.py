"""
Configuration for SWRL Translator
"""
from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv
import yaml
load_dotenv()


_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'config.yaml')


@dataclass
class TranslatorConfig:
  """Configuration for SWRL translation"""
  with open(_CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

  # Terminal arguments
  rag_type: str
  domain: str
  
  # Model configuration
  temperature: float = config['model']['temperature']
  
  # RAG configuration
  ontology_path: str = config['rag']['ontology_path']
  chunk_size: int = config['rag']['chunk_size']
  chunk_overlap: int = config['rag']['chunk_overlap']
  search_type: str = config['rag']['search_type']
  k: int = config['rag']['k']

  
  # Neo4j configuration (for graph translator)
  neo4j_uri: Optional[str] = None
  neo4j_user: Optional[str] = None
  neo4j_password: Optional[str] = None
  
  # Rules configuration
  rules_file: str = config['rules'] 
  rules_category: str = None
  
  def __post_init__(self):
    """Load environment variables for Neo4j if not provided"""
    if self.rag_type == "graph":
      self.neo4j_uri = self.neo4j_uri or os.getenv("NEO4J_URI")
      self.neo4j_user = self.neo4j_user or os.getenv("NEO4J_USER")
      self.neo4j_password = self.neo4j_password or os.getenv("NEO4J_PASSWORD")
    if self.domain == "PARKINSON":
      self.rules_category = self.rules_category or "PARKINSON"
    elif self.domain == "SAR":
      self.rules_category = self.rules_category or "SAR"


