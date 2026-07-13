from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

loader = PyPDFLoader("knowledge/FAQs.pdf")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)


query = "What is this document about?"

results = vector_store.similarity_search(
    query=query,
    k=3
)