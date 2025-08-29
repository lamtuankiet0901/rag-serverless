import os

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.schema import Document
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrock
from db_connection import get_pgvector_store

def chunk_documents(file_path) -> List[Document]:
    """
    Chunk the documents in the directory_path into smaller chunks of size chunk_size.

    Steps:
        1. MarkdownNodeParser: Parse the markdown files into nodes.
        2. Context Retrieval
    """
    loader = TextLoader(file_path=file_path)
    docs = loader.load()
    
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
    chunks = markdown_splitter.split_text(docs[0].page_content)
    contextualized_chunks = generate_contextualized_chunks(file_path, docs[0].page_content, chunks)
    
    return contextualized_chunks

def generate_contextualized_chunks(filename :str, document: str, chunks: List[Document]) -> List[Document]:
    """
    Generate contextualized versions of the given chunks.
    """
    contextualized_chunks = []
    for chunk in chunks:
        context = generate_context(filename, document, chunk.page_content)
        contextualized_content = f"{context}\n\n{chunk.page_content}"
        print(f"Context generated: {contextualized_content}")  # Print first 50 characters for brevity
        contextualized_chunks.append(Document(page_content=contextualized_content, metadata=chunk.metadata))
    return contextualized_chunks

def generate_context(filename :str, document: str, chunk: str) -> str:
    """
    Generate context for a specific chunk using the language model.
    """
    prompt = ChatPromptTemplate.from_template("""
    Here is the details of document:
    <filename>
    {filename}
    </filename>
    <document>
    {document}
    </document>

    Here is the chunk we want to situate within the whole document::
    <chunk>
    {chunk}
    </chunk>

    Give me a response follow:
        SUMMARY CONTEXT: Short summary context of chunk in the document

        HEADER: <policy_full_name>/<header_of_chunk_1>/<subheader_of_chunk_1>/.../<title_of_chunk_1><subtitle_of_chunk_1>
        
    Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk.
    Add headers/sub-headers of chunk in document.
    Answer only with the succinct context and nothing else. 
    Response in Vietnamese only.
    """)
    messages = prompt.format_messages(filename=filename, document=document, chunk=chunk)

    llm = ChatBedrock(region_name="us-east-1", model_id="anthropic.claude-3-haiku-20240307-v1:0")
    
    response = llm.invoke(messages)
    
    return response.content

async def vectorstores(documents: List[Document], CONNECTION_STRING: str, TABLE_NAME: str) -> None:
    """
    Create a vector store from the given documents.
    """
    vector_store = await get_pgvector_store(
        connection_string=CONNECTION_STRING,
        table=TABLE_NAME
    )
    
    await vector_store.aadd_documents(documents)