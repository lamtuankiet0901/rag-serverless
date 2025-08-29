from langchain_postgres import PGEngine
from langchain_postgres import PGVectorStore
from langchain_aws import BedrockEmbeddings

async def get_pgvector_store(connection_string: str, table: str) -> PGVectorStore:

    pg_engine = PGEngine.from_connection_string(url=connection_string)
    embedding = BedrockEmbeddings(region_name="us-east-1", model_id="amazon.titan-embed-text-v2:0")
    
    # await pg_engine.ainit_vectorstore_table(
    #     table_name=table,
    #     vector_size=vector_size,
    # )
    
    store = await PGVectorStore.create(
        engine=pg_engine,
        table_name=table,
        # schema_name=SCHEMA_NAME,
        embedding_service=embedding,
        id_column="langchain_id",
        content_column="content",
        embedding_column="embedding",
        metadata_json_column="langchain_metadata"
    )

    return store