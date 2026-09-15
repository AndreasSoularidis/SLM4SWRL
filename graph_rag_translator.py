from graph_rag import RAGEngineInterface
from prompt_templates import CustomPromptTemplates
from ontology_analyzer import OntologyAnalyzer
from swrl_translator import SWRLTranslator


class GraphRAGTranslator(SWRLTranslator):
  """SWRL Translator using Graph RAG with ontology analysis"""
    
  def __init__(self, 
                model_name: str, 
                temperature: float,
                ontology_analyzer: OntologyAnalyzer,
                rag_engine: RAGEngineInterface, 
                mode: str = "LOCAL"):
      super().__init__(model_name, temperature, rag_engine, mode)
      self.ontology_analyzer = ontology_analyzer
  

  def get_context(self, rule_in_nl: str) -> str:
    """Get context using Graph RAG with ontology classes"""
    onto_classes = self._get_ontology_classes()
    return self.rag_engine.get_entities(question=rule_in_nl, onto_classes=onto_classes)
  

  def _get_ontology_classes(self) -> str:
    return ", ".join(self.ontology_analyzer.get_classes())
  

  def _get_prompt_template(self):
    from langchain_core.prompts import ChatPromptTemplate
    return ChatPromptTemplate.from_template(CustomPromptTemplates.prompt)
