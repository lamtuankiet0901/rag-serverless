import os

from langchain_aws import BedrockEmbeddings, ChatBedrock
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from db_connection import get_pgvector_store
from langchain.prompts import ChatPromptTemplate

async def retrieve_documents(query: str, connection_string: str, table: str) -> str:
    """Retrieve documents from a vector store using a query and return the answer.
    This function uses a pre-defined query to retrieve relevant documents from a Pinecone vector store
    and then uses a language model to generate an answer based on those documents.
    """
    print("Retrieving...")
    print(f"Query: {query}")
    llm = ChatBedrock(region_name="us-east-1", model_id="anthropic.claude-3-haiku-20240307-v1:0")
    vector_store = await get_pgvector_store(
        connection_string=connection_string,
        table=table
    )
    print("Vector store loaded.")

    retrieval_qa_chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "Use the following documents to answer the user's question. If you don't know the answer, just say you don't know. Response in Vietnamese only."),
        ("user", "Question: {input}\n\nDocuments:\n{context}")
    ])
    
    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    retrival_chain = create_retrieval_chain(
        retriever=vector_store.as_retriever(), combine_docs_chain=combine_docs_chain
    )

    print("Retrieval chain created.")

    result = retrival_chain.invoke(input={"input": query})
    print("Retrieval complete.")
    print(f"Result: {result['answer']}")
    return result['answer']
