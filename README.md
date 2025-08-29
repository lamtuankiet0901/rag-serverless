# WB-Chatbot-Backend

## Overview

This repository contains the backend code for the WB IC Chatbot, which is designed to help the user quickly retrieval into the internal data.

## APIs

- Chat Function: `POST/lambdas/chat`
    - Chatbot function of RAG Serverless, using Bedrock LLM to generate answers.
- Embedding Function: `POST/lambdas/embedding`
    - Embedding function of RAG Serverless, using to embedding vectors into pgVector.
## Repo Structure

```plaintext
ask-wb-ic-chatbot-backend/
├── lambdas/                              # AWS Lambda functions
│   ├── embedding/                        # Embedding functions
│   └── chat/                             # Chat functions
├── layers/                               # AWS Lambda Layers
│   └── langchain_py/                     # common lib and func
├── local                                 # data and UI
├── script                                # sql int pgVector
├── terraform/                            # Terraform scripts for infrastructure (RDS Postgres, S3)
├── Makefile                              # Automation script for common tasks
├── pyproject.toml                        # Configuration for Python project
├── samconfig.toml                        # Configuration for AWS SAM
└── template.yaml                         # Template SAM/CloudFormation
```

## Getting Started

1. Install dependencies:
   ```bash
   make setup
   ```
2. Build package:
   ```bash
   make package
   ```
3. Deploy package:
   ```bash
    make apply
    ```
