"""
Configuration for SWRL Translator
"""
from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()


@dataclass
class TranslatorConfig:
    """Configuration for SWRL translation"""
    
    # Translator type: "graph" or "embeddings"
    translator_type: str = "embeddings"
    
    # Model configuration
    model_name: str = "llama"
    temperature: float = 0.0
    mode: str = "LOCAL"  # "LOCAL" or "API"
    
    # RAG configuration
    rag_data_path: str = "./data_SWRL/Parkinson"
    chunk_size: int = 1250
    chunk_overlap: int = 0
    search_type: str = "similarity"
    k: int = 5
    
    # Ontology configuration (for graph translator)
    ontology_path: Optional[str] = "./ontologies/Wear4PDmoveOnto_turtle.txt"
    ontology_format: str = "manchester"
    
    # Neo4j configuration (for graph translator)
    neo4j_uri: Optional[str] = None
    neo4j_user: Optional[str] = None
    neo4j_password: Optional[str] = None
    
    # Rules configuration
    rules_file: str = "./rules_in_natural_language.json"
    rules_category: str = "PARKINSON"  # or "SAR", "SAFERS", etc.
    
    def __post_init__(self):
      """Load environment variables for Neo4j if not provided"""
      if self.translator_type == "graph":
        self.neo4j_uri = self.neo4j_uri or os.getenv("NEO4J_URI")
        self.neo4j_user = self.neo4j_user or os.getenv("NEO4J_USER")
        self.neo4j_password = self.neo4j_password or os.getenv("NEO4J_PASSWORD")

