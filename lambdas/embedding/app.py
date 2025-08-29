import cryptography
import os
import glob
import asyncio

from indexing import chunk_documents, vectorstores

POSTGRES_USER = os.getenv("username")
POSTGRES_PASSWORD = os.getenv("password")
POSTGRES_HOST = os.getenv("host")
POSTGRES_PORT = os.getenv("port")
POSTGRES_DB = os.getenv("database")
TABLE_NAME = "vectorstore"

CONNECTION_STRING = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}"
    f":{POSTGRES_PORT}/{POSTGRES_DB}"
)

def handler(event, context):

    try:
        files = sorted(glob.glob(os.path.join("./data", "**/*.md"), recursive=True))

        contextualized_chunks = []
        print("Start chunking and vectorizing documents...")
        for file in files:
            print(f"Processing file: {file}")
            chucks = chunk_documents(file)
            contextualized_chunks.extend(chucks)
        print("Finished chunking documents. Now vectorizing...")
        asyncio.run(vectorstores(contextualized_chunks, CONNECTION_STRING, TABLE_NAME))
        print("Vectorization complete.")

        return {
            "statusCode": 200,
            "text": "message from LLM",
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            "statusCode": 500,
            "error": str(e),
        }