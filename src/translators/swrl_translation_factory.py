from rag.graph_rag import RAGEngineInterface
from utils.ontology_analyzer import OntologyAnalyzer
from translators.swrl_translator import SWRLTranslator
from translators.embeddings_rag_translator import EmbeddingsRAGTranslator
from translators.graph_rag_translator import GraphRAGTranslator
from typing import Optional

class SWRLTranslatorFactory:
  """Factory to create the appropriate SWRL translator based on configuration"""
    
  @staticmethod
  def create(translator_type: str, 
              model_name: str,
              temperature: float,
              rag_engine: RAGEngineInterface,
              mode: str = "LOCAL",
              ontology_analyzer: Optional[OntologyAnalyzer] = None) -> SWRLTranslator:
      """
      Create a SWRL translator based on type.
      
      Args:
          translator_type: "graph" or "embeddings"
          model_name: Name of the LLM model
          temperature: Temperature for generation
          rag_engine: RAG engine instance
          mode: "LOCAL" or "API"
          ontology_analyzer: Required for "graph" type
      
      Returns:
          Appropriate SWRLTranslator instance
      """
      translator_type = translator_type.lower()
      
      if translator_type == "graph":
        if ontology_analyzer is None:
          raise ValueError("ontology_analyzer is required for GraphRAGTranslator")
        return GraphRAGTranslator(
          model_name=model_name,
          temperature=temperature,
          ontology_analyzer=ontology_analyzer,
          rag_engine=rag_engine,
          mode=mode
        )
      elif translator_type == "embeddings":
        return EmbeddingsRAGTranslator(
          model_name=model_name,
          temperature=temperature,
          rag_engine=rag_engine,
          mode=mode
        )
      else:
        raise ValueError(f"Unknown translator type: {translator_type}. Use 'graph' or 'embeddings'")