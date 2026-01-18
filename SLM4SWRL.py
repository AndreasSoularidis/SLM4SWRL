from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from PromptTempates import CustomPromptTemplates
from ontology_analyzer import OntologyAnalyzer
import re
load_dotenv()

MODE = "LOCAL" # LOCAL

models = {
  "mistral": "mistral:7b",
  "mistral-instruct": "swot/mistral-v3-instruct:new",
  "llama": "llama3.1:8b",
  "llama-instruct": "llama/swrl",
  "qwen": "qwen2.5:7b",
  "qwen-instruct": "swot/qwen2.5-instruct:lastest",
  "openai": "ft:gpt-4o-2024-08-06:personal:recipe-ner:BMAvb5Vd",
  "phi-large": "phi3:14b",
  "phi-instruct": "swot/phi-3.5-mini-instruct:new",
  "phi4-instruct": "swot/phi-4-instruct:latest",
  "gemma": "gemma2:9b",
  "gemma-instruct": "swot/codegemma-instruct"
}

if MODE == "LOCAL":
  llm = ChatOllama(
    model=models["llama-instruct"],
    temperature=0.0,
  )
else:
  llm = ChatOpenAI(model=models["openai"], temperature=0.0)

retriever_llm = ChatOllama(
  model="llama3.1:8b",
  temperature=0.0,
  reasoning=False
)

graph = Neo4jGraph()
# Index creation
enhanced_graph = Neo4jGraph(enhanced_schema=True)
schema = enhanced_graph.get_structured_schema
nodes = schema['node_props']
filtered_nodes = [node for node in nodes if node.startswith("owl")]
entities = "(n:" + "|".join(filtered_nodes) + ")"
graph.query(f"CREATE FULLTEXT INDEX ontology IF NOT EXISTS FOR {entities} ON EACH [n.rdfs__label]")


class Entities(BaseModel):
  """Identifying information about entities."""

  names: List[str] = Field(
      ...,
      description="FIND and RETURN ALL the ontology concepts such as entities and relationships that appear in the text",
  )

prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      "You are an expert Knowledge/Ontology Engineer. "
      "Your task is to extract nouns or short phrases that appear in the input text and are present in the context. "
      "Output only the list of concept names, no explanations, no reasoning, no OWL or RDF, no text other than the list. "
      "Each concept must exactly match or be semantically equivalent to an ontology label."
    ),
    (
      "human",
      "Context:\n{context}\n\n"
      "Text:\n{question}\n\n"
    ),
  ]
)

onto_analyzer = OntologyAnalyzer("./ontologies/beAWARE.ttl")

onto_classes = ", ".join(onto_analyzer.get_classes())

entity_chain = prompt | retriever_llm.with_structured_output(Entities)

def breakCamelCaseEntities(entity: str) -> str:
  return re.sub(r'(?<!^)(?=[A-Z])', ' ', entity)

def structured_retriever(question: str) -> str:
  # results = ""
  results_set = set()
  entities = entity_chain.invoke({"question": question, "context": onto_classes})
  for entity in entities.names:
    response = graph.query(
      """ CALL db.index.fulltext.queryNodes('ontology', $query, {limit:4})
          YIELD node,score
          CALL(node) {
            WITH node
            MATCH (node)-[r]->(neighbor)
            RETURN  
              ':' + CASE 
                WHEN node.uri CONTAINS '#' THEN split(node.uri, '#')[-1]
                ELSE split(node.uri, '/')[-1]
              END + '  ' + 
              ':' + replace(type(r), '__', ':') + '  ' + 
              ':' + CASE 
                WHEN neighbor.uri CONTAINS '#' THEN split(neighbor.uri, '#')[-1]
                ELSE split(neighbor.uri, '/')[-1]
              END AS output
            UNION ALL
            WITH node
            MATCH (node)<-[r]-(neighbor)
            RETURN 
              ':' + CASE 
                WHEN neighbor.uri CONTAINS '#' THEN split(neighbor.uri, '#')[-1]
                ELSE split(neighbor.uri, '/')[-1]
              END + '  ' + 
              ':' + replace(type(r), '__', ':') + '  ' +
              ':' + CASE 
                WHEN node.uri CONTAINS '#' THEN split(node.uri, '#')[-1]
                ELSE split(node.uri, '/')[-1]
              END AS output
          }
          RETURN output, score
      """,
      {"query": breakCamelCaseEntities(entity)},
    )
    for el in response:
      results_set.add(el['output']) 

  result_list = sorted(list(results_set))
  results = "\n".join(result_list)
  return results


# print(structured_retriever("If a mission is related to a specific incident and that incident has a priority level of 'high', then the mission should also be assigned as a 'high' priority."))

templates = CustomPromptTemplates()

prompt = ChatPromptTemplate.from_template(templates.get_prompt("graph"))

chain = (
  RunnableParallel({
    "context": structured_retriever,
    "question": RunnablePassthrough(),
  })
  | prompt
  | llm
  | StrOutputParser()
)

rules = CustomPromptTemplates.sar_rules_in_nl(0, 10)
for _ in range(3):
  for index, rule in enumerate(rules):
    print(f"Rule {index+1}")
    print(f"Natural Language: {rule}")
    print(f"\nSWRL rule:")
    for chunk in chain.invoke(rule):
      print(chunk, end="", flush=True)
    print("\n")