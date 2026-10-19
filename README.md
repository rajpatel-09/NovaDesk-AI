# NovaDesk AI

**AI-powered Internal IT Helpdesk Copilot**

NovaDesk AI is an AI-powered internal IT helpdesk assistant that uses Retrieval-Augmented Generation (RAG) to answer employee questions using company documentation.

This project is being developed as a practical, internship-oriented AI engineering project. The goal is to build a working RAG system first, then extend it with FastAPI, Agentic AI, LangGraph, and MCP.

## Project Objectives

The project aims to:

- Answer employee questions using company documents.
- Retrieve relevant information through semantic search.
- Generate answers using an LLM and retrieved context.
- Report the source documents used to generate answers.
- Expose the RAG pipeline through a FastAPI backend.
- Introduce agentic decision-making and tool usage.
- Orchestrate multi-step workflows using LangGraph.
- Integrate tools through the Model Context Protocol (MCP).
- Improve testing, logging, error handling, and security.

Features that have not yet been implemented are part of the future roadmap.

## Current Features

The RAG core is implemented and has been manually tested.

- Recursive loading of company `.txt` documents.
- Document splitting into smaller chunks.
- Semantic embeddings using Sentence Transformers.
- Persistent vector storage using ChromaDB.
- Configurable retrieval using `top_k`.
- Answer generation through ChatGroq.
- Source-document reporting.
- Basic handling of questions that cannot be answered from the available context.
- Support for adding documents from new source files to the existing knowledge base.

## How It Works

```text
Employee Question
       |
       v
Question Embedding
       |
       v
ChromaDB Similarity Search
       |
       v
Retrieve Top 3 Chunks
       |
       v
Question + Retrieved Context
       |
       v
ChatGroq LLM
       |
       v
Generated Answer + Source Documents
```

The default RAG pipeline retrieves three chunks. The number of chunks can be changed when creating the pipeline.

Retrieval results are not guaranteed to be fully relevant. Improving retrieval quality and handling insufficient evidence are ongoing improvement areas.

## Technology Stack

### Implemented

- Python 3.12
- `uv` — Python project and dependency management
- LangChain
- ChatGroq — LLM integration
- `openai/gpt-oss-20b` — configured answer-generation model
- Hugging Face Sentence Transformers
- `sentence-transformers/all-MiniLM-L6-v2` — embedding model
- `langchain-chroma` and ChromaDB — vector storage and retrieval

### Planned

- FastAPI — HTTP API
- Agentic AI — decision-making and tool usage
- LangGraph — workflow orchestration
- MCP — tool integration
- Expanded automated testing and production improvements

## Company Knowledge Base

The knowledge base currently contains four synthetic company documents:

| Department | Document | Purpose |
|---|---|---|
| HR | `leave_policy.txt` | Employee leave rules |
| IT | `vpn_troubleshooting.txt` | VPN troubleshooting |
| IT | `software_installation_policy.txt` | Software approval and installation |
| Security | `password_security_policy.txt` | Password and account security |

Documents are stored under `data/company_docs/`.

The loader discovers `.txt` files recursively. The current ChromaDB collection is named `novadesk_docs` and is persisted under `data/vector_store/`.

The ingestion pipeline has reported 11 chunks for the current knowledge base.

## Project Structure

```text
NovaDesk-AI/
├── data/
│   ├── company_docs/
│   │   ├── HR/
│   │   ├── IT/
│   │   └── SECURITY/
│   └── vector_store/              # Local ChromaDB data
├── notebook/
│   └── 01_rag_fundamentals.ipynb
├── src/
│   ├── ingestion/
│   │   ├── embeddings.py
│   │   ├── loader.py
│   │   ├── pipeline.py
│   │   ├── retriever.py
│   │   ├── splitter.py
│   │   └── vectorstore.py
│   ├── rag/
│   │   ├── generator.py
│   │   ├── pipeline.py
│   │   ├── retriever.py
│   │   ├── test_pipeline.py
│   │   └── test_retriever.py
│   ├── api/                        # Planned: FastAPI
│   ├── agent/                      # Planned: Agentic AI
│   ├── graph/                      # Planned: LangGraph
│   ├── mcp/                        # Planned: MCP
│   ├── config/
│   └── novadesk_ai/
├── .env                            # Local secrets; not committed
├── .gitignore
├── LEARNING_LOG.md
├── PROJECT_CONTEXT.md
├── README.md
├── pyproject.toml
└── uv.lock
```

## Getting Started

### Prerequisites

- Python 3.12
- `uv`
- A Groq API key

### 1. Clone the repository

```powershell
git clone https://github.com/rajpatel-09/NovaDesk-AI.git
cd NovaDesk-AI
```

### 2. Install dependencies

```powershell
uv sync
```

### 3. Configure the API key

Create a `.env` file in the project root and configure your Groq API key according to the project's environment setup.

```text
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own key. Never commit your real API key to GitHub.

### 4. Build or update the knowledge base

```powershell
uv run python -m src.ingestion.pipeline
```

This loads the company documents, creates chunks and embeddings, and adds documents to the persistent ChromaDB collection according to the current ingestion logic.

### 5. Ask a question

Run the following command from the project root:

```powershell
uv run python -c "from src.rag.pipeline import RAGPipeline; print(RAGPipeline().ask('How many casual leave days do employees get?'))"
```

The pipeline returns the generated answer followed by the source-document paths.

## Current Project Status

### Phase 1 — RAG Core

**Status: Implemented and manually tested**

Completed:

- Document loading and splitting
- Embedding generation
- ChromaDB vector storage
- Configurable retrieval
- LLM answer generation
- Source reporting
- Initial out-of-scope testing
- Adding a new company policy and testing retrieval

### Phase 2 — FastAPI

**Status: In progress**

Implemented and tested:

- `GET /health` — checks that the API responds.
- `POST /ask` — accepts an employee question and calls the existing RAG pipeline.
- Pydantic request model for incoming questions.
- Interactive API documentation at `/docs`.

Run the development server from the project root:

```powershell
uv run uvicorn src.api.main:app --reload
```

Next: improve request validation and error handling, then test edge cases.

### Phase 3 — Agentic AI

**Status: Not started**

Introduce controlled decision-making and tool usage.

### Phase 4 — LangGraph

**Status: Not started**

Build stateful, multi-step workflows.

### Phase 5 — MCP

**Status: Not started**

Integrate tools using the Model Context Protocol.

### Phase 6 — Production Improvements

**Status: Not started**

Improve error handling, logging, security, automated testing, and documentation.

## Known Limitations

- Retrieved chunks can contain irrelevant information.
- The number of retrieved chunks does not guarantee relevance or correctness.
- Out-of-scope questions may still retrieve unrelated company documents.
- The current ingestion logic handles new source files but does not automatically refresh chunks when an existing document is modified.
- More automated tests and explicit checks for insufficient evidence are needed.

## Learning Approach

This is a project-based learning journey:

```text
Learn
  |
  v
Understand Why
  |
  v
Implement
  |
  v
Test
  |
  v
Debug and Improve
```

The focus is on understanding how each component works and gradually developing the ability to implement it independently.

## Repository

GitHub: https://github.com/rajpatel-09/NovaDesk-AI

## Security

- Store API keys in `.env`.
- Keep secrets out of source code and Git commits.
- Keep `.env` and the local `data/vector_store/` directory excluded through `.gitignore`.

## Automated API Testing

Run the automated test suite from the project root:

```powershell
uv run python -m pytest -v