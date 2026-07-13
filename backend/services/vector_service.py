from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)