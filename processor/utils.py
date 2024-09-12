import os
from pathlib import Path
from uuid import uuid4
import PyPDF2
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


def get_file_type(file_path: str) -> str:
    """
    Determine the type of the file based on its extension.

    Args:
    file_path (str): Path to the file

    Returns:
    str: File type ('txt', 'pdf', 'doc', or 'unknown')
    """
    extension = Path(file_path).suffix.lower()
    if extension == ".txt":
        return "txt"
    elif extension == ".pdf":
        return "pdf"
    elif extension in [".doc", ".docx"]:
        return "doc"
    else:
        return "unknown"


def generate_asset_id() -> str:
    """
    Generate a unique asset ID.

    Returns:
    str: Unique Asset ID
    """
    return str(uuid4())


def extract_text_from_txt(file_path: str) -> str:
    """
    Extract text from a .txt file.

    Args:
    file_path (str): Path to a .txt file

    Returns:
    str: Extracted text content
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a .pdf file.

    Args:
    file_path (str): Path to a .pdf file

    Returns:
    str: Extracted text content
    """
    text = ""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def extract_text_from_doc(file_path: str) -> str:
    """
    Extract text from a .doc or .docx file.

    Args:
    file_path (str): Path to the .doc or .docx file

    Returns:
    str: Extracted text content
    """
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])


def extract_text(file_path: str) -> str:
    """
    Extract text from a file based on its type.

    Args:
    file_path (str): Path to the file

    Returns:
    str: Extracted text content
    """
    file_type = get_file_type(file_path)
    if file_type == "txt":
        return extract_text_from_txt(file_path)
    elif file_type == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_type == "doc":
        return extract_text_from_doc(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def create_embeddings(text: str, asset_id: str) -> Chroma:
    """
    Create embeddings from text and store them in ChromaDB.

    Args:
    text (str): Text to create embeddings from
    asset_id (str): Unique identifier for the document

    Returns:
    Chroma: Chroma DB instance containning the embeddings
    """
    # split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)

    # create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # store embeddings in Chroma DB
    db = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory="./chromadb",
        collection_name=asset_id,
    )

    return db


def process_document(file_path: str):
    """
    Process a document: extract text, create embeddings, and store them in Chroma DB

    Args:
    file_path (str): Path to the document file

    Returns:
    str: Asset ID of the processed document
    """
    # Extract text from the document
    text = extract_text(file_path)

    # Generate a unique asset ID
    asset_id = generate_asset_id()

    # create embeddings and store them in Chroma DB
    db = create_embeddings(text, asset_id)

    # persist the database
    # db.persist()

    return asset_id
