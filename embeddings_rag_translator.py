from prompt_templates import CustomPromptTemplates
from swrl_translator import SWRLTranslator


class EmbeddingsRAGTranslator(SWRLTranslator):
  """SWRL Translator using Embeddings RAG (simpler approach)"""
    
  def get_context(self, rule_in_nl: str) -> str:
    """Get context using Embeddings RAG"""
    return self.rag_engine.get_entities(question=rule_in_nl)
    
  def _get_prompt_template(self):
    from langchain_core.prompts import PromptTemplate
    return PromptTemplate.from_template(CustomPromptTemplates.prompt)