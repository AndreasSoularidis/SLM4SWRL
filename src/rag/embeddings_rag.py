from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from rag.graph_rag import RAGEngineInterface

class EmbeddingsRAG(RAGEngineInterface):
  def __init__(self, 
               ontology_path,
               domain,
               embeddings_model,
               serialization,
               chunk_size=1000,
               chunk_overlap=200,
               search_type="similarity",
               k=5):
    self.ontology_path = ontology_path
    self.domain = domain
    self.embeddings_model = embeddings_model
    self.chunk_size = chunk_size
    self.chunk_overlap = chunk_overlap
    self.search_type = search_type
    self.serialization = serialization
    self.k = k
    self.vector_store = self.create_vectorstore()


  def create_vectorstore(self):
    match self.domain:
      case "PARKINSON":
        ontology_name = "Wear4PDmoveOnto"
      case "SAR":
        ontology_name = "beAWARE"

    with open(f"{self.ontology_path}/{ontology_name}_{self.serialization}.txt", "r", encoding="utf-8") as f:
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
      chunk_size=self.chunk_size,
      chunk_overlap=self.chunk_overlap
    )
    docs = [Document(page_content=docs, metadata={"source": f"{self.ontology_path}/{ontology_name}_{self.serialization}.txt"})]
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=self.embeddings_model)
    return vectorstore
  

  def get_entities(self, question: str = "") -> str:
    """Retrieve relevant documents and return as formatted string"""
    retriever = self.vector_store.as_retriever(search_type=self.search_type, search_kwargs={"k": self.k})
    
    if question:
      # If question provided, retrieve relevant docs
      docs = retriever.invoke(question)
    else:
      # If no question, get all documents from the vectorstore
      docs = self.vector_store.similarity_search("", k=self.k)
    
    # Format documents as string
    return "\n".join(doc.page_content for doc in docs)