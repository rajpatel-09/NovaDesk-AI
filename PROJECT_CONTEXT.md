# NovaDesk AI — Project Context

**Last updated:** October 22, 2026

## 1. Project Overview

**Project name:** NovaDesk AI
**Description:** AI-powered Internal IT Helpdesk Copilot

NovaDesk AI is an internship learning project designed to answer employee questions using company documentation and perform support-related tasks through AI agents, tools, and workflows.

The project is being developed incrementally to build practical, industry-oriented AI engineering skills.

The long-term goal is to create a reliable, production-style IT helpdesk copilot with document retrieval, agentic tool usage, workflow orchestration, and tool integration through the Model Context Protocol (MCP).

## 2. Learning Roadmap

1. Phase 1 — RAG (Retrieval-Augmented Generation)
2. Phase 2 — FastAPI
3. Phase 3 — Agentic AI
4. Phase 4 — LangGraph
5. Phase 5 — MCP
6. Phase 6 — Production improvements

**Current stage:** The RAG foundation is complete. The FastAPI core has been implemented and tested. An initial LangChain agent and its company-document search tool have been implemented and manually tested. Additional agent testing, API integration, documentation, and production improvements remain.

## 3. Teaching and Development Approach

- Work one step at a time.
- Explain why a change is needed before writing code.
- Explain code rather than providing unexplained copy-and-paste instructions.
- Use small experiments and ask for predictions where useful.
- Test changes before moving forward.
- Avoid repeating completed concepts unless needed for debugging.
- Prioritize understanding and practical implementation over memorization.
- Preserve working components rather than rebuilding them unnecessarily.
- Update project documentation after meaningful milestones.

## 4. Current Technology Stack

- Python 3.12
- `uv` for project and dependency management
- LangChain for LLM integration and agent development
- ChatGroq using `openai/gpt-oss-20b` for answer generation
- Hugging Face Sentence Transformers
- `sentence-transformers/all-MiniLM-L6-v2` for embeddings
- ChromaDB through `langchain-chroma` for vector storage and retrieval
- FastAPI for HTTP endpoints
- Pydantic for request validation
- LangChain Agents using `create_agent`
- LangGraph planned for explicit multi-step workflow orchestration
- MCP planned for exposing and using support-related tools through the Model Context Protocol

The Groq API key is stored in `.env` and must not be hard-coded in Python files or committed to Git.

## 5. Project Structure

Important project directories and files:

- `data/company_docs/` — synthetic company documentation
- `data/vector_store/` — persistent local ChromaDB data; ignored by Git
- `notebook/01_rag_fundamentals.ipynb` — RAG learning notebook
- `src/ingestion/` — document loading, splitting, embeddings, vector store, and retriever configuration
- `src/rag/` — retrieval, answer generation, RAG pipeline, and manual test scripts
- `src/api/` — FastAPI application with `GET /health` and `POST /ask`
- `src/agent/agent.py` — LangChain agent creation, instructions, and invocation
- `src/agent/tools.py` — company-document search tool used by the agent
- `src/graph/` — reserved for future LangGraph workflows
- `src/mcp/` — reserved for future MCP integration
- `tests/test_api.py` — automated API tests
- `LEARNING_LOG.md` — learning and implementation history
- `PROJECT_CONTEXT.md` — current project state
- `README.md` — project overview and setup instructions
- `pyproject.toml` — project metadata and dependencies
- `uv.lock` — locked dependency versions

## 6. Company Knowledge Base

Four `.txt` documents currently exist under `data/company_docs/`:

1. `HR/leave_policy.txt`
2. `IT/vpn_troubleshooting.txt`
3. `IT/software_installation_policy.txt`
4. `SECURITY/password_security_policy.txt`

The document loader discovers `.txt` files recursively under `data/company_docs/`.

The ingestion pipeline previously reported **11 chunks** in the ChromaDB collection `novadesk_docs`.

The vector store is persisted in `data/vector_store/`. This local data is excluded from Git.

## 7. Implemented RAG Components

### 7.1 Document ingestion

The ingestion process:

1. Loads company documents.
2. Splits documents into smaller chunks.
3. Creates embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
4. Stores document chunks, embeddings, and metadata in ChromaDB.

The current vector-store logic adds chunks from previously unseen source files. It does not yet automatically refresh chunks when an existing source file is modified.

### 7.2 Retrieval

`src/rag/retriever.py` contains `CompanyRetriever`.

- The default `top_k` is 3.
- `CompanyRetriever` uses the retriever configured in `src/ingestion/retriever.py`.
- The ChromaDB retriever uses `similarity_score_threshold` with an initial relevance threshold of `0.25`.
- Matches below the configured threshold are rejected.
- The number of returned documents is limited by `top_k`.
- The threshold has been manually tested with a relevant VPN troubleshooting question and an unsupported FIFA ticket reimbursement question.
- The threshold is an initial configuration and needs evaluation against a wider range of questions.

### 7.3 Answer generation

`src/rag/generator.py` contains `AnswerGenerator`.

Current model configuration:

- Model: `openai/gpt-oss-20b` through ChatGroq
- Temperature: `0`
- Reasoning format: `hidden`

The generator receives the user's question and retrieved documents as context to produce a grounded answer.

### 7.4 RAG pipeline

`src/rag/pipeline.py` contains `RAGPipeline`.

The current flow is:

Question → Retrieve relevant documents → Generate answer → Return answer and source paths

If the retriever returns no relevant documents, the pipeline returns:

`I could not find relevant information in the company documents.`

When documents are retrieved, their source paths are included in the result.

## 8. What Has Been Tested

### 8.1 RAG and retrieval

- HR leave-policy questions.
- IT VPN troubleshooting questions.
- Security-policy questions.
- An out-of-scope FIFA World Cup ticket reimbursement question.
- Retrieval using `top_k=3` and `top_k=5`.
- Ingestion and retrieval of the software installation policy.
- Source-document reporting.
- Similarity-score relevance filtering with an initial threshold of `0.25`.
- Confirmed that a relevant VPN question retrieves the VPN troubleshooting guide and produces a useful answer.
- Confirmed that the unsupported FIFA reimbursement question returns the fallback response without listing unrelated source documents.
- Re-tested the VPN question after adding the relevance threshold.

### 8.2 FastAPI

- Implemented `GET /health` and `POST /ask`.
- Connected the `/ask` endpoint to the existing RAG pipeline.
- Tested Pydantic validation for empty or whitespace-only questions and requests missing the required `question` field.
- Verified invalid requests return HTTP 422.
- Tested exception handling around RAG pipeline failures.
- Verified unexpected errors return HTTP 500 with a generic error response.
- Implemented lazy initialization and caching of the RAG pipeline.
- Added automated API tests using mocked RAG behavior.
- Verified that all five automated API tests pass using `uv run python -m pytest`.

### 8.3 Agentic AI

- Created an agent using LangChain's `create_agent`.
- Connected the `search_company_docs` tool to the existing RAG pipeline.
- Confirmed that a VPN troubleshooting question triggers the document-search tool and produces an answer.
- Inspected the agent's message sequence and verified that a `ToolMessage` was returned by `search_company_docs`.
- Confirmed that a vague question receives a clarifying question without calling the tool.
- Confirmed that the unsupported FIFA reimbursement question triggers document search and returns a fallback response rather than an invented policy.
- Re-tested relevant and unsupported questions after introducing the retrieval relevance threshold.

### 8.4 Environment and Git

- Recreated a separate Python 3.12 environment after installation problems with the original environment.
- Verified that LangChain and `create_agent` import successfully.
- Verified that the existing RAG pipeline runs in the new environment.
- Confirmed that `uv lock --check` completes without an error.
- Re-ran the automated API tests successfully after the retrieval changes.
- Committed and pushed the agent implementation, dependency updates, and relevance-filtering changes to GitHub in commit `b634858`.

The files `src/rag/test_pipeline.py` and `src/rag/test_retriever.py` are manual test scripts containing `main()` functions, not automated pytest test cases. They are not counted among the five automated API tests.

These checks cover the current implementation. Broader automated testing is still needed.

## 9. Known Limitations

- The relevance threshold of `0.25` is an initial setting. It has been manually tested with a relevant VPN question and an unsupported FIFA ticket reimbursement question, but it needs evaluation against more questions.
- Similarity scores do not guarantee that every returned chunk contains all the information needed to answer a question.
- The current ingestion logic does not automatically refresh chunks when an existing source file is modified.
- The five automated tests cover API behavior. Additional automated tests for retrieval, answer generation, and agent behavior would improve reliability.
- The initial agent implementation has passed the documented manual checks, but broader testing is still needed for tool selection, unsupported requests, and error handling.
- The agent has not yet been fully integrated into the FastAPI `/ask` endpoint.
- Authentication, authorization, rate limiting, and other production security considerations still need to be evaluated before any real company deployment.
- The original `.venv` encountered incomplete package metadata and Windows access or file-linking errors. It has been left untouched.

These are improvement areas, not reasons to rebuild the existing RAG foundation.

## 10. Phase Status

### Phase 1 — RAG core: Completed

Document ingestion, embeddings, ChromaDB storage, retrieval, answer generation, and source reporting are implemented and manually tested.

An initial relevance threshold of `0.25` has been added and tested against selected relevant and unsupported questions.

### Phase 2 — FastAPI: Core implementation completed; improvements ongoing

Completed:

- Created `src/api/main.py` with `GET /health` and `POST /ask`.
- Connected the `/ask` endpoint to the existing RAG pipeline.
- Added Pydantic request validation.
- Verified invalid requests return HTTP 422.
- Added logging and exception handling around RAG pipeline failures.
- Verified unexpected errors return HTTP 500 with a generic error response.
- Implemented lazy initialization and caching of the RAG pipeline.
- Added automated API tests using mocked RAG behavior.
- Verified all five automated API tests pass.
- Confirmed the real RAG pipeline continues to work with the API implementation.

Development server:

`uv run uvicorn src.api.main:app --reload`

The current application command uses Uvicorn with `src.api.main:app`. This works with the existing project structure.

Remaining work:

- Expand automated testing where useful.
- Improve API reliability, error handling, and configuration.
- Integrate the agent into the API where appropriate.
- Continue production-oriented improvements and documentation.

### Phase 3 — Agentic AI: Initial implementation completed; further development ongoing

Implemented:

- Created `src/agent/agent.py` using LangChain's `create_agent`.
- Created `src/agent/tools.py` with the `search_company_docs` tool.
- Connected the tool to the existing `RAGPipeline`.
- Added instructions for the agent to use company documents for company-specific questions.
- Added instructions to ask clarifying questions when requests are too vague.
- Added instructions not to invent company-specific facts when relevant information is unavailable.
- Implemented lazy initialization and caching for the agent and its RAG pipeline.
- Manually verified relevant, vague, and unsupported question behavior.
- Verified that the agent calls the document-search tool when answering the tested VPN question.
- Verified that vague questions are clarified without calling the tool.
- Verified that an unsupported question returns a fallback rather than an invented company policy.

Remaining work:

- Add automated tests for agent behavior and tool calls.
- Test a wider range of relevant, vague, and unsupported questions.
- Improve agent error handling and reliability.
- Integrate the agent into the FastAPI application where appropriate.

The current agent has passed the listed manual checks. Broader testing and integration remain.

### Phase 4 — LangGraph: Not started

Use LangGraph to orchestrate multi-step workflows with state, nodes, edges, and conditional routing.

### Phase 5 — MCP: Not started

Expose and use support-related tools through the Model Context Protocol.

### Phase 6 — Production improvements: Not started

Improve testing, logging, error handling, configuration, security, maintainability, and deployment readiness.

## 11. Git and GitHub

- Git branch: `main`
- GitHub repository: https://github.com/rajpatel-09/NovaDesk-AI
- Initial RAG implementation commit: `0f71f8d`
- Latest recorded project commit: `b634858` — `feat: add agent and relevance filtering`
- The latest recorded commit was successfully pushed to `origin/main`.
- `.env`, `.venv/`, `data/vector_store/`, and other generated or local files are excluded through `.gitignore`.

Never commit API keys, credentials, or other secrets.

### Local Python environment note

A separate Python 3.12 environment was created at:

`%LOCALAPPDATA%\uv-envs\novadesk-ai`

The original project `.venv` remains untouched.

The environment was successfully synchronized using:

`uv sync --link-mode=copy`

The `UV_PROJECT_ENVIRONMENT` variable was set in the working PowerShell terminal to direct `uv` to this separate environment:

`$env:UV_PROJECT_ENVIRONMENT = "$env:LOCALAPPDATA\uv-envs\novadesk-ai"`

This setting is specific to the current terminal session unless configured elsewhere. If a new terminal does not inherit or define it, set it again before running project commands with `uv`. Do not delete the original `.venv` as part of this recovery.

## 12. Immediate Next Steps

1. Finish updating and reviewing `PROJECT_CONTEXT.md`.
2. Update `LEARNING_LOG.md` with the environment recovery, agent implementation, relevance filtering, tests, and GitHub commit.
3. Update `README.md` to reflect the actual project architecture, setup instructions, and implemented features.
4. Verify the documentation changes and run the relevant automated tests.
5. Review, commit, and push the documentation updates to GitHub.
6. Add automated tests