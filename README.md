# NovaDesk AI

**AI-powered Internal IT Helpdesk Copilot**

NovaDesk AI is an AI-powered internal IT helpdesk assistant that answers employee questions using company documentation. It combines Retrieval-Augmented Generation (RAG), a FastAPI backend, and an initial LangChain agent with a company-document search tool.

This is an internship-oriented AI engineering project built incrementally, with an emphasis on understanding, testing, and implementing realistic software components.

## Project Objectives

- Answer employee questions using company documentation.
- Retrieve relevant information using semantic search.
- Generate answers grounded in retrieved context.
- Report the source documents used to support answers.
- Expose the RAG pipeline through a FastAPI backend.
- Introduce agentic decision-making and tool usage.
- Orchestrate multi-step workflows using LangGraph.
- Integrate tools through the Model Context Protocol (MCP).
- Improve testing, logging, error handling, configuration, and security.

## Current Features

### RAG and Knowledge Retrieval

- Recursive loading of company `.txt` documents.
- Document splitting into smaller chunks.
- Semantic embeddings using Sentence Transformers.
- Persistent vector storage using ChromaDB.
- Configurable retrieval with `top_k`.
- Similarity-score threshold filtering, initially set to `0.25`.
- Answer generation through ChatGroq.
- Source-document reporting.
- A fallback response when no relevant documents are retrieved.
- Support for adding previously unseen source files to the knowledge base.

### FastAPI

- `GET /health` to check API availability.
- `POST /ask` to submit employee questions to the RAG pipeline.
- Pydantic validation for incoming questions.
- Logging and handling of unexpected pipeline errors.
- Lazy initialization and caching of the RAG pipeline.
- Five automated API tests covering health checks, request validation, successful responses with mocked RAG behavior, and error handling.

### Initial Agentic AI Implementation

- LangChain agent created using `create_agent`.
- `search_company_docs` tool connected to the existing RAG pipeline.
- Clarifying questions for vague requests.
- Instructions to avoid inventing unsupported company-specific facts.
- Manual testing of relevant questions, vague requests, and unsupported questions.

**Current limitation:** The agent has been tested separately and is not yet integrated into the FastAPI `/ask` endpoint.

## Architecture

### RAG Workflow

```text
Employee Question
       |
       v
RAGPipeline
       |
       v
CompanyRetriever
       |
       v
ChromaDB Similarity Search
       |
       v
Relevance Threshold Filtering
       |
       v
Retrieved Context
       |
       v
ChatGroq Answer Generator
       |
       v
Answer + Source Documents
```

The retriever uses an initial relevance threshold of `0.25` and a default `top_k` of 3. These settings are starting points and require evaluation with more questions.

### Agent Workflow

```text
Employee Question
       |
       v
LangChain Agent
       |
       v
Decide Whether to Use a Tool
       |
       v
search_company_docs
       |
       v
Existing RAGPipeline
       |
       v
Tool Result
       |
       v
Agent Response
```

The agent can ask a clarifying question when a request is too vague to understand. For company-specific questions, it can use the document-search tool to obtain supporting information.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Main programming language |
| `uv` | Dependency and project management |
| LangChain | LLM integration and agent development |
| ChatGroq | Language-model integration |
| `openai/gpt-oss-20b` | Configured answer-generation model |
| Hugging Face Sentence Transformers | Embedding generation |
| `sentence-transformers/all-MiniLM-L6-v2` | Embedding model |
| ChromaDB | Vector storage and similarity search |
| `langchain-chroma` | LangChain integration with ChromaDB |
| FastAPI | HTTP API |
| Pydantic | Request validation |
| pytest | Automated testing |

LangGraph and MCP are planned for future project phases.

## Company Knowledge Base

The knowledge base contains four synthetic company documents.

| Department | Document | Purpose |
|---|---|---|
| HR | `leave_policy.txt` | Employee leave rules |
| IT | `vpn_troubleshooting.txt` | VPN troubleshooting |
| IT | `software_installation_policy.txt` | Software approval and installation |
| Security | `password_security_policy.txt` | Password and account security |

Documents are stored under `data/company_docs/`.

The document loader discovers `.txt` files recursively. The ChromaDB collection is named `novadesk_docs` and is persisted under `data/vector_store/`.

The current knowledge base has previously reported 11 chunks.

### Ingestion Limitation

The current ingestion logic adds chunks from previously unseen source files. It does not yet automatically refresh stored chunks when an existing source document is modified.

## Project Structure

```text
NovaDesk-AI/
├── data/
│   ├── company_docs/
│   │   ├── HR/
│   │   ├── IT/
│   │   └── SECURITY/
│   └── vector_store/             # Local ChromaDB data; ignored by Git
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
│   ├── api/
│   │   └── main.py
│   ├── agent/
│   │   ├── agent.py
│   │   └── tools.py
│   ├── graph/                    # Reserved for LangGraph
│   ├── mcp/                      # Reserved for MCP
│   ├── config/
│   └── novadesk_ai/
├── tests/
│   └── test_api.py
├── .env                          # Local secrets; not committed
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

From the project root, run:

```powershell
uv sync --link-mode=copy
```

The copy mode can help avoid file-linking problems on some Windows or cloud-synced setups. On systems where hardlinks work normally, the standard `uv sync` command can also be used.

### 3. Configure the API key

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own key. Never commit your real API key to GitHub.

### 4. Build or update the knowledge base

Run:

```powershell
uv run python -m src.ingestion.pipeline
```

This loads company documents, creates chunks and embeddings, and adds previously unseen source documents to the persistent ChromaDB collection according to the current ingestion logic.

### 5. Ask a RAG question

Run:

```powershell
uv run python -c "from src.rag.pipeline import RAGPipeline; print(RAGPipeline().ask('How many casual leave days do employees get?'))"
```

The pipeline returns an answer followed by source-document paths when relevant documents are retrieved.

### 6. Run the FastAPI application

Start the development server from the project root:

```powershell
uv run uvicorn src.api.main:app --reload
```

The server runs locally at:

`http://127.0.0.1:8000`

Open the interactive API documentation at:

`http://127.0.0.1:8000/docs`

The available endpoints are:

- `GET /health`
- `POST /ask`

Example PowerShell request:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri "http://127.0.0.1:8000/ask" `
  -ContentType "application/json" `
  -Body '{"question":"How can I troubleshoot VPN connection problems?"}'
```

### 7. Test the initial agent

The agent can currently be tested separately from the API:

```powershell
uv run python -c "from src.agent.agent import ask_agent; print(ask_agent('How can I troubleshoot VPN connection problems?'))"
```

This calls the existing agent and allows it to use `search_company_docs` when appropriate.

## Automated Testing

Run the automated tests from the project root:

```powershell
uv run python -m pytest
```

The latest recorded run reported **5 passed**.

The automated tests are in `tests/test_api.py`. They cover API behavior, including request validation, mocked successful RAG responses, and unexpected errors.

The files `src/rag/test_pipeline.py` and `src/rag/test_retriever.py` are manual test scripts rather than automated pytest test cases.

Manual tests have also verified:

- Relevant VPN troubleshooting questions.
- Vague requests that need clarification.
- Unsupported FIFA ticket reimbursement questions.
- Tool invocation by the agent.
- Relevance filtering for selected supported and unsupported questions.

Automated testing for retrieval and agent behavior remains future work.

## Current Project Status

### Phase 1 — RAG Core

**Status: Completed; relevance filtering added and manually tested.**

Implemented:

- Document ingestion and chunking.
- Embedding generation and ChromaDB storage.
- Configurable retrieval.
- LLM answer generation.
- Source-document reporting.
- Initial relevance threshold of `0.25`.
- Manual tests for relevant and unsupported questions.

### Phase 2 — FastAPI

**Status: Core implementation completed; improvements ongoing.**

Implemented:

- `GET /health` and `POST /ask`.
- Integration with the existing RAG pipeline.
- Pydantic validation.
- Error handling and logging.
- Lazy initialization and caching.
- Five passing automated API tests.

Remaining work includes expanded testing, configuration improvements, and integration with the agent.

### Phase 3 — Agentic AI

**Status: Initial implementation completed; further development ongoing.**

Implemented:

- LangChain agent using `create_agent`.
- `search_company_docs` tool.
- Connection to the existing RAG pipeline.
- Clarification for vague requests.
- Fallback behavior for unsupported requests.

Remaining work includes automated agent tests, broader behavior evaluation, and API integration.

### Phase 4 — LangGraph

**Status: Not started.**

Planned: orchestrate multi-step workflows using state, nodes, edges, and conditional routing.

### Phase 5 — MCP

**Status: Not started.**

Planned: expose and use support-related tools through the Model Context Protocol.

### Phase 6 — Production Improvements

**Status: Not started.**

Planned: improve automated testing, configuration, logging, error handling, security, maintainability, and deployment readiness.

## Known Limitations

- The `0.25` relevance threshold is an initial setting, not a universally validated value.
- Similarity scores do not guarantee that retrieved chunks contain all the information needed to answer a question.
- Only a limited set of supported and unsupported questions has been manually tested.
- The ingestion logic does not automatically refresh chunks when existing documents change.
- Agent behavior does not yet have a dedicated automated test suite.
- The initial agent is not yet integrated into the FastAPI `/ask` endpoint.
- Production security, authentication, authorization, monitoring, and deployment considerations remain to be addressed.

## Learning Approach

This project follows an incremental learning process:

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

The goal is to understand why each component exists, explain how it works, and gradually build the ability to implement the components independently.

## Repository

GitHub: https://github.com/rajpatel-09/NovaDesk-AI

Latest recorded project commit:

`b634858` — `feat: add agent and relevance filtering`

## Security

- Store API keys in `.env`.
- Never hard-code credentials in source code.
- Never commit secrets to Git.
- Keep `.env` and local `data/vector_store/` data excluded through `.gitignore`.