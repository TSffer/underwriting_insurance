import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

PERSIST_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/chroma_db")


def get_vectorstore():
    """Retorna la instancia conectada a ChromaDB."""
    embedding_function = OpenAIEmbeddings(model="text-embedding-3-large")

    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_function,
        collection_name="insurance_policies"
    )
    return vectorstore
