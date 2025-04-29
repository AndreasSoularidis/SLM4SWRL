from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_neo4j.vectorstores.neo4j_vector import remove_lucene_chars
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from PromptTempates import CustomPromptTemplates

load_dotenv()

models = {
  "mistral": "mistral:v0.3",
  "mistral-instruct": "mistral-instruct-v3:latest",
  "llama": "llama3.1:latest",
  "llama-instruct": "llama3.1-instruct-v3:latest",
  "openai": "ft:gpt-4o-2024-08-06:personal:recipe-ner:BMAvb5Vd"
}

llm = ChatOllama(
  model=models["llama-instruct"],
  temperature=0.0,
)

# llm = ChatOpenAI(model=models["openai"], temperature=0.0)

retriever_llm = ChatOllama(
  model="llama3.1:latest",
  temperature=0.0,
)

graph = Neo4jGraph()
enhanced_graph = Neo4jGraph(enhanced_schema=True)
schema = enhanced_graph.get_structured_schema

nodes = schema['node_props']
rels = schema['rel_props']
entities = "(n:" + "|".join(nodes) + "|".join(rels) + ")"
graph.query(f"CREATE FULLTEXT INDEX ontology IF NOT EXISTS FOR {entities} ON EACH [n.label]")

class Entities(BaseModel):
  """Identifying information about entities."""

  names: List[str] = Field(
      ...,
      description="The related concepts are shown in the given text with the first letter capitalised. FIND and RETURN ALL the ontology concepts such as entities and relationships that appear in the text",
  )

def generate_full_text_query(input: str) -> str:
  full_text_query = ""
  words = [el for el in remove_lucene_chars(input).split() if el]
  for word in words[:-1]:
    full_text_query += f" {word} AND"
  full_text_query += f" {words[-1]}"
  
  return full_text_query.strip()


def structured_retriever(question: str) -> str:
  results = ""
  entities = entity_chain.invoke({"question": question})
  for entity in entities.names:
    response = graph.query(
      """CALL db.index.fulltext.queryNodes('ontology', $query, {limit:5})
          YIELD node,score
          CALL(node) {
            WITH node
            MATCH (node)-[r]->(neighbor)
            RETURN type(r) + ' (domain: ' + node.label + ', range: ' + neighbor.label + ')' AS output
            UNION ALL
            WITH node
            MATCH (node)<-[r]-(neighbor)
            RETURN type(r) + ' (domain: ' + neighbor.label + ', range: ' + node.label + ')' AS output
          }
          RETURN output LIMIT 50
      """,
      {"query": generate_full_text_query(entity)},
    )
    result = "\n".join([el['output'] for el in response])
    results += result + "\n"
  return results


prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      "You are an Knowledge/Ontology Engineer, your goal is to extract concepts (nouns) from the text.",
    ),
    (
      "human",
      "Use the given format to extract concepts (nouns) from the following "
      "input: {question}",
    ),
  ]
)


entity_chain = prompt | retriever_llm.with_structured_output(Entities)


# print(structured_retriever("if gas is recognized at coordinates and fire is recognized at these coordinates and agents is nearby to these coordinates, then send an alert to these agents, and the agents must abort mission."))
prompt = ChatPromptTemplate.from_template(CustomPromptTemplates.ontology_template)

chain = (
  RunnableParallel({
      "context": structured_retriever,
      "question": RunnablePassthrough(),
  })
  | prompt
  | llm
  | StrOutputParser()
)

# print(chain.invoke("if gas is recognized at coordinates and fire is recognized at these coordinates and agents is nearby to these coordinates, then send an alert to these agents, and the agents must abort mission."))
# print("\n")
# print(chain.invoke("if a person is recognized at coordinates and has heart rate less than 30 pulses per minute and the location in these coordinates is safe, then send to thsese coordinates a search and rescue team."))
# print("\n")
# print(chain.invoke("if house on fire is recognized at coordinates and person has Voice Sign 'help', then send alert to fire station, send to these coordinates a search and rescue team, send to these coordinates a flying drone agent and send to these coordinates a spot robot agent."))

rules = CustomPromptTemplates.rules_in_nl()

for rule in rules:
  print(f"Natural Language rule: {rule}")
  print(f"SWRL rule:")
  for chunk in chain.invoke(rule):
    print(chunk, end="", flush=True)
  print()