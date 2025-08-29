create EXTENSION vector;

CREATE TABLE vectorstore (
    langchain_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content TEXT,
    langchain_metadata JSON,
    embedding vector(1024) DEFAULT NULL -- vector dimensions depends on the embedding model
);