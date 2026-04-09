from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from graph_rag import GraphRAG
from prompt_templates import CustomPromptTemplates
from ontology_analyzer import OntologyAnalyzer
from model_provider import ModelProvider
load_dotenv()


class SLM4SWRL:
  def __init__(self, 
               model_name: str, 
               temperature: float,
               ontology_analyser: OntologyAnalyzer,
               rag_engine: GraphRAG, 
               mode: str = "LOCAL"):
    self.ontology_analyzer = ontology_analyser
    self.rag_engine = rag_engine
    if mode == "LOCAL":
      self.model = ChatOllama(model=ModelProvider().get_model(model_name), temperature=temperature)
    else:
      self.model = ChatOpenAI(model=ModelProvider().get_model(model_name), temperature=temperature)


  def get_ontology_classes(self) -> str:
    return ", ".join(self.ontology_analyzer.get_classes())

  def generate_swrl(self, rule_in_nl: str) -> str:
    onto_classes = self.get_ontology_classes()
    context = self.rag_engine.get_entities(question=rule_in_nl, onto_classes=onto_classes)
    prompt = ChatPromptTemplate.from_template(CustomPromptTemplates.prompt)
    chain = prompt | self.model | StrOutputParser()

    for chunk in chain.invoke({"context": context, "question": rule_in_nl}):
      print(chunk, end="", flush=True)



# chain = (
#       RunnableParallel({
#         "context": context,
#         "question": RunnablePassthrough(),
#       })
#       | prompt
#       | self.model
#       | StrOutputParser()
#     )