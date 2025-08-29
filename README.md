# WB-Chatbot-Backend

## Overview

This repository contains the backend code for the WB IC Chatbot, which is designed to help the user quickly retrieval into the internal data.

## APIs

- Chat Function: `POST/lambdas/chat`
    - Chatbot function of WB IC Chatbot, using Bedrock LLM to generate answers.
- Bot Function: `POST/lambdas/bot`
    - Bot function of WB IC Chatbot, using to deploy bot into Microsoft Teams.
## Repo Structure

```plaintext
ask-wb-ic-chatbot-backend/
├── lambdas/                              # AWS Lambda functions
│   ├── bot/           
│   └── chat/            
├── layers/                               # AWS Lambda Layers         
│   └── chat_layer/         
├── local                                 # Indexing Documents into Vector DB
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
