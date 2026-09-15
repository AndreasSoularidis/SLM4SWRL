from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.tools import tool
from langgraph.graph import MessagesState
from langchain_ollama import ChatOllama

load_dotenv()

ontology_path = "./ontologies/beAWARE_rdf_xml.txt"

with open(ontology_path, "r", encoding="utf-8") as f:
    docs = f.read()

text_splitter = RecursiveCharacterTextSplitter(
  separators=[
    # Manchester Syntax: whitespace-only lines before block keywords
    r"\n[ \t]*\n[ \t]*\n(?=(?:ObjectProperty|Class|DataProperty|AnnotationProperty|Individual|Datatype):)",
    # RDF/XML: whitespace-only lines before a <!-- comment --> that precedes a block
    r"\n[ \t]*\n[ \t]*\n[ \t]*(?=<!--)",
    r"\n\n",
    r"\n",
    r" ",
    r""
  ],
  is_separator_regex=True,
  keep_separator="start",
  chunk_size=1000,
  chunk_overlap=0
)

docs = [Document(page_content=docs, metadata={"source": ontology_path})]
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 7})


@tool
def retrieve_ontology_context(query: str) -> str:
  """Search and return ontology context based on the query."""
  docs = retriever.invoke(query)
  return "\n\n".join([doc.page_content for doc in docs])

retriever_tool = retrieve_ontology_context

retrieved_data = retriever_tool.invoke({"query": "types of reward hacking"})

response_model = ChatOllama(model="ministral-3:14b", temperature=0.0)

def generate_query_or_respond(state: MessagesState):
  """Call the model to generate a response based on the current state. Given
  the question, it will decide to retrieve using the retriever tool, or simply respond to the user.
  """
  response = (
      response_model
      .bind_tools([retriever_tool]).invoke(state["messages"])
  )
  return {"messages": [response]}


prompt = """Act as an ontology engineer. Use the following content (examples, part of the ontology, and a list of guidelines) as a guide to translate the natural language rule you are given into a SWRL rule. 
  EXAMPLES
    Example 1
    Rule in natural language: If a person has a sibling who is a man, then the person has a brother.
    SWRL rule: Person(?p) ^ hasSibling(?p, ?s) ^ Person(?s) ^ IsMan(?s, true) -> hasBrother(?p, ?s)

    Example 2
    Rule in natural language: if a person has a phone number that starts with '+', then the person has an international phone number.
    SWRL rule: Person(?p) ^ hasPhoneNumber(?p, ?number) ^ swrlb:startsWith(?number, "+") -> hasInternationalPhoneNumber(?p, true)

    Example 3
    Rule in natural language:  if a person has age greater than 17, then the person is an adult and has id card.
    SWRL rule: Person(?p) ^ hasAge(?p, ?age) ^ Age(?age) ^ swrlb:greaterThan(?age, 17) ^ IdCard(?id) -> Adult(?p) ^ hasIdCard(?p, ?id)

    Example 4
    Rule in natural language: if a publication has two different authors, then those authors have cooperated with each other.
    SWRL rule: Publication(?p) ^ Author(?y) ^ Author(?z) ^ hasAuthor(?p, ?y) ^ hasAuthor(?p, ?z) ^ differentFrom(?y, ?z) -> cooperatedWith(?y, ?z)

    Example 5
    Rule in natural language: if a researcher has published more than 10 papers in a Top-Tier conference, then the researcher is a prominent researcher and has a high citation impact.
    SWRL rule: Researcher(?r) ^ hasPublished(?r, ?c) ^ Conference(?c) ^ topTierConference(?c) ^ swrlb:greaterThan(count(?c), 10) -> ProminentResearcher(?r) ^ hasHighCitationImpact(?r, true)
  END OF EXAMPLES

  COMMON GUIDELINES

  Please try to implement the following guidelines:
  1: Variables e.g., (?something) used in Conclusions must be present in Conditions. So create as many variables as needed in Conditions. 
  2: Each atom must have exactly one variable if it represents class.
  3: Each atom must have exactly two variables if it represents object property.
  4: Each concept must be represented by a class and must be present in Conditions.

  END OF COMMON GUIDELINES

  The rule in natural language is the following: If a mission is related to a specific incident and that incident has a priority level of 'high', then the mission should also be assigned as a 'high' priority.
  Give only the final SWRL rule"""


input = {
    "messages": [
        {
            "role": "user",
            "content": prompt,
        }
    ]
}


generate_query_or_respond(input)["messages"][-1].pretty_print()