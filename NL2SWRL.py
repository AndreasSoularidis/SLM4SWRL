from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from prompt_templates import CustomPromptTemplates
from FileLoaders import FileLoader
from langchain_ollama import ChatOllama

load_dotenv()

# PARAMETERS
FULL_MODE = True
ONTOLOGY_MODE = False
MODEL = "llama3.1-SWRL-3" 
TEMPERATURE = 0.0
RAG_DATA = "./data_SWRL/SAFERS"
CHUNK_SIZE = 1250
CHUNK_OVERLAP = 0
SEARCH_TYPE = "similarity"
K = 5
FORMAT = "manchester"

# Initialize the LLM with deepseek-r1:8b model
llm = ChatOllama(
  model=MODEL,
  temperature=TEMPERATURE,
  max_tokens=500,
)

def format_docs(docs):
  return "\n\n".join(doc.page_content for doc in docs)

if FULL_MODE or ONTOLOGY_MODE:
  docs = FileLoader.get_txt_loader(RAG_DATA)

  text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
  splits = text_splitter.split_documents(docs)

  vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
  retriever = vectorstore.as_retriever(search_type=SEARCH_TYPE, search_kwargs={"k": K})

  if FULL_MODE: 
    custom_prompt = PromptTemplate.from_template(CustomPromptTemplates.prompt)
  else:
    custom_prompt = PromptTemplate.from_template(CustomPromptTemplates.prompt)
  
  chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | custom_prompt
    | llm
    | StrOutputParser()
  )
else:
  custom_prompt = PromptTemplate.from_template(CustomPromptTemplates.prompt)
  chain = custom_prompt | llm | StrOutputParser()

prompts = CustomPromptTemplates.sar_rules_in_nl(0, 10)
for _ in range(1):
  for index, prompt in enumerate(prompts):
    print(f"Rule {index+1}")
    for chunk in chain.invoke(prompt):
      print(chunk, end="", flush=True)
    print()