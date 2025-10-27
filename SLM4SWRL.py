from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph
from langchain_ollama import ChatOllama, OllamaLLM
from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_neo4j.vectorstores.neo4j_vector import remove_lucene_chars
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import ChatOpenAI
from PromptTempates import CustomPromptTemplates
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
import re
from rdflib.plugins.sparql import prepareQuery

load_dotenv()

MODE = "LOCAL" # LOCAL

models = {
  "mistral": "mistral:7b",
  "mistral-instruct": "swot/mistral-v3-instruct:new",
  "llama": "llama3.1:8b",
  "llama-instruct": "swot/llama3.1-instruct:new",
  "qwen": "qwen2.5:7b",
  "qwen-instruct": "swot/qwen2.5-instruct:lastest",
  "openai": "ft:gpt-4o-2024-08-06:personal:recipe-ner:BMAvb5Vd",
  "phi-large": "phi3:14b",
  "phi-instruct": "swot/phi-3.5-mini-instruct:new",
  "phi4-instruct": "swot/phi-4-instruct:latest",
  "gemma": "gemma2:9b",
  "gemma-instruct": "swot/codegemma-instruct",
  "qwen3": "qwen3:8b"
}

if MODE == "LOCAL":
  llm = OllamaLLM(
    model=models["llama"],
    temperature=0.0
  )
else:
  llm = ChatOpenAI(model=models["openai"], temperature=0.0)

retriever_llm = ChatOllama(
  model="qwen3:8b",
  temperature=0.6,
  reasoning=False
)

def get_txt_loader(folder_name):
  # Use forward slashes and turn off silent_errors to see what's wrong
  text_loader = DirectoryLoader(
      f"./{folder_name}", 
      glob="**/*.txt",  # Changed from **\\*.txt
      loader_cls=TextLoader, 
      show_progress=True, 
      silent_errors=False,  # Changed from True
      loader_kwargs={'encoding': 'utf-8'}  # Added encoding
  )
  docs = text_loader.load()
  
  # Add debugging
  if not docs:
      print(f"No documents loaded from {folder_name}")
      print(f"Check if folder exists: {os.path.exists(f'./{folder_name}')}")
  
  return docs

def format_docs(docs):
  return "\n".join(doc.page_content for doc in docs)

docs = get_txt_loader("./ontologies/PD_ontology")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
splits = text_splitter.split_documents(docs)

vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

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
      description="List of ontology concept names found in the text. Only use ontology terms. No explanations."
  )

def generate_full_text_query(input: str) -> str:
  full_text_query = ""
  words = [el for el in remove_lucene_chars(input).split() if el]
  for word in words[:-1]:
    full_text_query += f" {word} AND"
  full_text_query += f" {words[-1]}"
  return full_text_query.strip()


prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      "You are an expert Knowledge/Ontology Engineer. "
      "Your task is to extract nouns or short phrases that appear in the input text "
      "and are present in the provided ontology. "
      "Output only the list of concept names, no explanations, no reasoning, no OWL or RDF, no text other than the list. "
      "Each concept must exactly match or be semantically equivalent to an ontology label."
    ),
    (
      "human",
      "Ontology:\n{context}\n\n"
      "Text:\n{question}\n\n"
    ),
  ]
)

def breakCamelCaseEntities(entity: str) -> str:
  return re.sub(r'(?<!^)(?=[A-Z])', ' ', entity)

entity_chain = prompt | retriever_llm.with_structured_output(Entities)

def structured_retriever(question: str) -> str:
  relevant_docs = retriever.invoke(question) 
  results_set = set()
  entities = entity_chain.invoke({"context": relevant_docs, "question": question, })
  print(f"Entities found: {entities}")
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

prompt = ChatPromptTemplate.from_template(CustomPromptTemplates.RAG_template)

chain = (
  RunnableParallel({
    "context": structured_retriever,
    "question": RunnablePassthrough(),
  })
  | prompt
  | llm
  | StrOutputParser()
)

rules = CustomPromptTemplates.pd_rules_in_nl(0,10)

for index, rule in enumerate(rules):
  print(f"Rule {index+1}")
  print(f"Natural Language: {rule}")
  print(f"\nSWRL rule:")
  for chunk in chain.invoke(rule):
    print(chunk, end="", flush=True)
  print("\n")
  time.sleep(5)

