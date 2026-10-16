# NovaDesk AI — Project Context

**Last updated:** October 15, 2026

## 1. Project Overview

**Project name:** NovaDesk AI
**Description:** AI-powered Internal IT Helpdesk Copilot

NovaDesk AI is an internship learning project designed to answer employee questions using company documentation and later perform support-related actions through tools and workflows.

The project is being built incrementally to develop practical, industry-oriented AI engineering skills.

## 2. Learning Roadmap

1. RAG — Retrieval-Augmented Generation
2. Agentic AI
3. LangGraph
4. MCP
5. Production-style improvements

**Current stage:** Phase 2 — FastAPI in progress. The initial health-check endpoint is working.

## 3. Teaching and Development Approach

- Work one step at a time.
- Explain why a change is needed before writing code.
- Explain code rather than providing unexplained copy-paste instructions.
- Use small experiments and ask for predictions where useful.
- Test changes before moving forward.
- Avoid repeating completed concepts unless needed for debugging.
- Prioritize understanding and practical implementation over memorization.

## 4. Current Technology Stack

- Python 3.12
- `uv` for project and dependency management
- LangChain
- ChatGroq with `openai/gpt-oss-20b` for answer generation
- Hugging Face Sentence Transformers
- `sentence-transformers/all-MiniLM-L6-v2` embeddings
- ChromaDB through `langchain-chroma`
- FastAPI — planned, not implemented yet
- LangGraph — planned
- MCP — planned

The Groq API key is stored in `.env`, not hard-coded in Python files.

## 5. Project Structure

Important existing directories and files:

- `data/company_docs/` — synthetic company documentation
- `data/vector_store/` — local ChromaDB persistence; ignored by Git
- `notebook/01_rag_fundamentals.ipynb` — RAG learning notebook
- `src/ingestion/` — document loading, splitting, embeddings, vector store, and ingestion pipeline
- `src/rag/` — retrieval, answer generation, pipeline, and test files
- `src/api/` — FastAPI application with `GET /health` and `POST /ask` endpoints
- `src/agent/` — reserved for Agentic AI
- `src/graph/` — reserved for LangGraph
- `src/mcp/` — reserved for MCP
- `LEARNING_LOG.md` — learning and implementation history
- `PROJECT_CONTEXT.md` — current project state
- `README.md` — project overview and setup instructions
- `pyproject.toml` and `uv.lock` — dependencies and environment configuration

## 6. Company Knowledge Base

Four `.txt` documents currently exist under `data/company_docs/`:

1. `HR/leave_policy.txt`
2. `IT/vpn_troubleshooting.txt`
3. `IT/software_installation_policy.txt`
4. `SECURITY/password_security_policy.txt`

The loader discovers `.txt` files recursively under `data/company_docs/`.

The ingestion pipeline currently reports **11 chunks** in the ChromaDB collection `novadesk_docs`.

## 7. Implemented RAG Components

### Document ingestion

The ingestion process:

1. Loads company documents.
2. Splits them into smaller chunks.
3. Creates embeddings using `all-MiniLM-L6-v2`.
4. Stores the chunks and their embeddings in ChromaDB.

The vector store is persisted in `data/vector_store/`.

The current vector-store logic adds chunks from previously unseen source files. It does not yet refresh chunks when an existing source file is modified.

### Retrieval

`src/rag/retriever.py` contains `CompanyRetriever`.

- Default `top_k` is 3.
- It uses the retriever created by `vectorstore.as_retriever()`.
- The number of retrieved chunks can be configured.

### Answer generation

`src/rag/generator.py` contains `AnswerGenerator`.

The current model configuration is:

- Model: `openai/gpt-oss-20b` through ChatGroq
- Temperature: `0`
- Reasoning format: `hidden`

The generator receives the question and retrieved documents as context.

### RAG pipeline

`src/rag/pipeline.py` contains `RAGPipeline`.

The current flow is:

Question → Retrieve chunks → Generate answer → Return answer and source paths

The pipeline returns a fallback message if retrieval returns no documents.

## 8. What Has Been Tested

- HR leave-policy questions
- IT VPN troubleshooting questions
- Security-policy questions
- An out-of-scope question
- Retrieval using `top_k=3` and `top_k=5`
- Ingestion of a new software installation policy
- Retrieval of the newly added policy
- Source-document reporting
- GitHub repository setup and initial push

Examples of observed behavior:

- The casual-leave question correctly returned 12 days, supported by the HR policy.
- The software-installation question correctly stated that IT approval is required.
- The out-of-scope FIFA World Cup question received a fallback-style response rather than a factual guess.

## 9. Known Limitations

- Retrieval can return unrelated chunks even when the final answer is correct.
- `top_k=3` does not guarantee that every retrieved chunk is relevant.
- Out-of-scope questions can still retrieve unrelated company documents.
- No similarity-score threshold or dedicated relevance-checking stage has been implemented.
- Modified source files are not automatically re-indexed by the current ingestion logic.
- Further automated testing and error handling are needed.

These are known improvement areas, not reasons to rebuild the existing RAG foundation.

## 10. Phase Status

### Phase 1 — RAG core: Completed

Document ingestion, embeddings, ChromaDB storage, retrieval, answer generation, and source reporting are implemented and have been manually tested.

### Phase 2 — FastAPI: In progress

Completed:
- Installed FastAPI using `uv add "fastapi[standard]"`.
- Created `src/api/main.py`.
- Implemented `GET /health` and verified it in the browser.
- Verified FastAPI's interactive documentation at `/docs`.
- Implemented `POST /ask` using Pydantic's `QuestionRequest` model.
- Connected the endpoint to the existing `RAGPipeline`.
- Successfully tested question submission and received a JSON answer.
- Added Pydantic validation to reject empty or whitespace-only questions.
- Verified invalid questions return HTTP 422.
- Fixed a validator bug by raising `ValueError` instead of attempting to raise a string.
- Retested valid questions to confirm the RAG pipeline still works.
- Verified that requests missing the required `question` field return HTTP 422.

Development server:
`uv run uvicorn src.api.main:app --reload`

Note: The FastAPI CLI command did not resolve the `src` import correctly. Running the app through Uvicorn using `src.api.main:app` works.

Next: Improve request validation and error handling, then test edge cases.

### Phase 3 — Agentic AI: Not started

Introduce decision-making and tool usage where appropriate.

### Phase 4 — LangGraph: Not started

Orchestrate multi-step workflows using state, nodes, edges, and conditional routing.

### Phase 5 — MCP: Not started

Expose and use support-related tools through the Model Context Protocol.

### Phase 6 — Production improvements: Not started

Improve testing, logging, error handling, configuration, security, and documentation.

## 11. Git and GitHub

- Git branch: `main`
- GitHub repository: https://github.com/rajpatel-09/NovaDesk-AI
- Initial RAG implementation commit: `0f71f8d`
- `.env` and `data/vector_store/` are excluded through `.gitignore`.

Never commit API keys or other secrets.

## 12. Immediate Next Steps

1. Update `PROJECT_CONTEXT.md`.
2. Update `LEARNING_LOG.md` with the completed RAG implementation, debugging, experiments, and GitHub setup.
3. Update `README.md` to reflect the actual project status and technology stack.
4. Verify and commit the documentation changes.
5. Begin Phase 2: FastAPI, integrating the existing RAG pipeline rather than rebuilding it.
