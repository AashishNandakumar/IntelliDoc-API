import os
from uuid import uuid4
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory


def get_chat_model() -> ChatOpenAI:
    """
    Get an OpenAI chat model.

    Returns:
    ChatOpenAI: ChatOpenAI instance of a specific model
    """
    return ChatOpenAI(model="gpt-3.5-turbo", streaming=True)


def get_vector_store(asset_id: str):
    """
    Get the vector store for the corresponding asset ID.

    Args:
    asset_id (str): unique identifier of the document

    Returns:
    Chroma: ChromaDB instance of the corresponding asset ID
    """
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma(
        persist_directory="./chromadb",
        embedding_function=embeddings,
        collection_name=asset_id,
    )

    if vector_store._collection.count() == 0:
        print(f"Warning: No documents found for asset ID: {asset_id}")
        return None

    return vector_store


def create_chat_chain(asset_id: str):
    """
    Create a chain to chat with the document corresponding to the asset ID

    Args:
    asset_id (str): unique identifier for the document

    Returns:
    ConversationalRetrievalChain: A chain that combines LLM + Retriever + Memory
    """
    vector_store = get_vector_store(asset_id)
    if vector_store is None:
        return None

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3},
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
    )

    return ConversationalRetrievalChain.from_llm(
        llm=get_chat_model(),
        retriever=retriever,
        memory=memory,
        verbose=True,
    )


def generate_thread_id():
    """
    Generate a unique asset ID.

    Returns:
    str: Unique Asset ID
    """
    return str(uuid4())
