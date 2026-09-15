"""
SWRL Translator - Abstract Base Class and Factory Pattern
"""
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from rag.graph_rag import RAGEngineInterface
from utils.model_provider import ModelProvider
load_dotenv()


class SWRLTranslator(ABC):
  """Abstract base class for SWRL translators"""
  def __init__(self, 
                model_name: str, 
                temperature: float,
                rag_engine: RAGEngineInterface, 
                mode: str = "LOCAL"):
      self.rag_engine = rag_engine
      if mode == "LOCAL":
          self.model = ChatOllama(model=ModelProvider().get_model(model_name), temperature=temperature)
      else:
          self.model = ChatOpenAI(model=ModelProvider().get_model(model_name), temperature=temperature)
    
  @abstractmethod
  def get_context(self, rule_in_nl: str) -> str:
    """Get context for the translation. Must be implemented by subclasses."""
    pass

  @abstractmethod
  def _get_prompt_template(self):
    """Get the appropriate prompt template"""
    pass
    
  def generate_swrl(self, rule_in_nl: str) -> str:
    """Generate SWRL rule from natural language - common implementation"""
    context = self.get_context(rule_in_nl)
    prompt = self._get_prompt_template()
    chain = prompt | self.model | StrOutputParser()

    for chunk in chain.invoke({"context": context, "question": rule_in_nl}):
      print(chunk, end="", flush=True)