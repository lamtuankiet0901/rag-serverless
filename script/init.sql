create EXTENSION vector;

-- Table Definition
CREATE TABLE "public"."vectorstore" (
    "langchain_id" uuid NOT NULL,
    "content" text NOT NULL,
    "embedding" vector NOT NULL,
    "langchain_metadata" json,
    PRIMARY KEY ("langchain_id")
);