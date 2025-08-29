import cryptography
import os
import asyncio

from aws_lambda_powertools import Logger, Tracer
from aws_xray_sdk.core import xray_recorder
from query import retrieve_documents
from aws_env import load_secrets_as_env_vars

logger = Logger()
tracer = Tracer()
load_secrets_as_env_vars(os.getenv("SECRET_NAME"))

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

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
@xray_recorder.capture("handler")
def handler(event, context):
    logger.info(f"cryptography __version__: {cryptography.__version__}")
    logger.info(event)
    user_content = event["text"]

    try:
        # Call LLM to get response
        message = asyncio.run(retrieve_documents(user_content, CONNECTION_STRING, TABLE_NAME))

        return {
            "statusCode": 200,
            "text": message,
        }

    except Exception as e:
        logger.error(f"Error call LLM function: {str(e)}")
        return {
            "statusCode": 500,
            "error": str(e),
        }