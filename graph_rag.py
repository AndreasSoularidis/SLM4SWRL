import re
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from model_provider import ModelProvider
from neo4j_connector import Neo4jConnector
from prompt_templates import CustomPromptTemplates

class Entities(BaseModel):
  """Identifying information about entities."""
  names: List[str] = Field(
      ...,
      description="FIND and RETURN ALL the ontology concepts such as entities and relationships that appear in the text",
  )

class RAGEngineInterface:
  @staticmethod
  def get_entities(self, question: str, onto_classes: str = None) -> str:
    pass

class GraphRAG(RAGEngineInterface):
  def __init__(self,
               model_name: str,
               temperature: float, 
               neo4j_connector: Neo4jConnector,):
    self.neo4j_connector = neo4j_connector
    self.retriever_llm = ChatOllama(model=ModelProvider().get_model(model_name), temperature=temperature, reasoning=False)
  

  def extract_entities_from_text(self, question: str, onto_classes: str):
    system_prompt = CustomPromptTemplates().retreiver_system
    prompt_template = CustomPromptTemplates().retreiver_prompt
    prompt = ChatPromptTemplate.from_messages(
      [
        {
          'role': 'system',
          'content': system_prompt,
        },
        {
          'role': 'user',
          'content': prompt_template,
        }
      ]
    )
    chain = prompt | self.retriever_llm.with_structured_output(Entities, method="json_schema")
    response = chain.invoke({"question": question, "context": onto_classes})
    return response

  def breakCamelCaseEntities(self, entity: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', entity)


  def get_entities(self, question: str, onto_classes: str) -> str:
    results_set = set()
    entities = self.extract_entities_from_text(question, onto_classes)
    for entity in entities.names:
      search_query = self.breakCamelCaseEntities(entity)
      # print(f"DEBUG: Searching for '{entity}' -> '{search_query}'")
      
      response = self.neo4j_connector.query(
        """ CALL db.index.fulltext.queryNodes('ontology', $query, {limit: 4})
            YIELD node,score
            CALL(node) {
              WITH node
              MATCH (node)-[r]->(neighbor)
              RETURN  
                ':' + CASE 
                  WHEN node.uri CONTAINS '#' THEN split(node.uri, '#')[-1]
                  ELSE split(node.uri, '/')[-1]
                END + '  ' + 
                replace(type(r), '__', ':') + '  ' + 
                ':' + CASE 
                  WHEN neighbor.uri CONTAINS '#' THEN split(neighbor.uri, '#')[-1] + ' .'
                  ELSE split(neighbor.uri, '/')[-1] + ' .'
                END AS output
              UNION ALL
              WITH node
              MATCH (node)<-[r]-(neighbor)
              RETURN 
                ':' + CASE 
                  WHEN neighbor.uri CONTAINS '#' THEN split(neighbor.uri, '#')[-1]
                  ELSE split(neighbor.uri, '/')[-1]
                END + '  ' + 
                replace(type(r), '__', ':') + '  ' +
                ':' + CASE 
                  WHEN node.uri CONTAINS '#' THEN split(node.uri, '#')[-1] + ' .'
                  ELSE split(node.uri, '/')[-1] + ' .'
                END AS output
            }
            RETURN output, score
        """,
        {"query": search_query},
      )
      # print(f"DEBUG: Query returned {len(response)} results for '{entity}'")
      for el in response:
        results_set.add(el['output'])

    result_list = sorted(list(results_set))
    results = "\n".join(result_list)
    # print(f"DEBUG: Final RAG results ({len(result_list)} items):\n{results}\n")
    return results