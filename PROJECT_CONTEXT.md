# NovaDesk AI — Project Context

**Last updated:** October 24, 2026

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

**Current stage:** The RAG foundation and FastAPI core are implemented and tested. An initial LangChain agent and its company-document search tool have been integrated into the FastAPI `POST /ask` endpoint. Three manual API scenarios and five automated API tests have passed. Further agent testing, documentation, and production improvements remain.

## 3. Teaching and Development Approach

- Explain why a change is needed before writing code.
- Explain existing code rather than providing unexplained copy-and-paste instructions.
- Work through related tasks in manageable batches.
- Use small experiments and ask for predictions where useful.
- Test changes before moving forward.
- Avoid repeating completed concepts unless needed for debugging.
- Prioritize understanding and practical implementation over memorization.
- Preserve working components rather than rebuilding them unnecessarily.
- Update project documentation after meaningful milestones.
- Review changes before committing them to GitHub.

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
- pytest for automated testing
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
- `src/api/main.py` — FastAPI application with `GET /health` and `POST /ask`
- `src/agent/agent.py` — LangChain agent creation, system instructions, and invocation
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

The current vector-store logic adds chunks from previously unseen source files. It does not yet automatically refresh stored chunks when an existing source file is modified.

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

## 8. Agentic AI Implementation

### 8.1 Agent creation

`src/agent/agent.py` defines the agent using LangChain's `create_agent`.

The agent is configured with:

- The LLM obtained from `AnswerGenerator`.
- The `search_company_docs` tool.
- System instructions describing its role and expected behavior.

The system instructions tell the agent to use company documents for company-specific questions, ask concise clarifying questions when requests are too vague, and avoid inventing unsupported company facts.

### 8.2 Agent invocation

The `ask_agent(question)` function:

1. Calls `get_agent()` to obtain the configured agent.
2. Sends the employee's question to the agent using `.invoke()`.
3. Allows the agent to decide whether to call the search tool.
4. Returns the content of the final agent message.

The `get_agent()` function uses `@lru_cache(maxsize=1)` so the configured agent can be reused instead of recreated for every question.

### 8.3 Company-document search tool

`src/agent/tools.py` defines `search_company_docs(question)`.

The tool uses:

`get_rag_pipeline().ask(question)`

The cached `get_rag_pipeline()` function returns a reusable `RAGPipeline` instance.

**Current architecture:** The tool runs the existing RAG retrieval and answer-generation workflow. It returns the RAG result to the agent, which then produces the final response.

This preserves the tested RAG implementation. A future architecture review may evaluate a retrieval-only tool that returns document passages directly to the agent. That change should be made only after considering evidence grounding, model calls, latency, and the existing pipeline behavior.

### 8.4 Agent and API integration

The FastAPI endpoint in `src/api/main.py` now calls:

`ask_agent(request.question)`

The earlier direct call to `get_rag_pipeline().ask(request.question)` has been replaced.

The current request flow is:

Employee Question → FastAPI `POST /ask` → `ask_agent()` → Agent Tool Selection → RAG Pipeline When Needed → Agent Final Response → API Response

The agent's and RAG pipeline's cached components are initialized when needed.

## 9. What Has Been Tested

### 9.1 RAG and retrieval

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

### 9.2 FastAPI and agent integration

The following three scenarios were manually tested through FastAPI's Swagger UI:

1. **Supported company-policy question:** "How many casual leave days do employees get?" The API returned the answer of 12 days per year and cited the leave policy.
2. **Vague question:** "It does not work. Help me." The agent asked for clarification.
3. **Unsupported policy question:** "What is NovaTech Solutions policy on reimbursing FIFA World Cup tickets?" The agent acknowledged that the company documents did not provide the answer rather than inventing a policy.

All three requests returned HTTP `200 OK`, and the observed responses matched the expected behaviors.

### 9.3 Automated API tests

The latest verified automated test run reported:

**5 passed in 1.48 seconds.**

The tests in `tests/test_api.py` cover:

- `GET /health`.
- Rejection of blank questions.
- Rejection of requests missing the required `question` field.
- A successful `/ask` response using a mocked agent.
- Unexpected-error handling.

The automated tests mock `ask_agent`. They verify API behavior without requiring the real agent or LLM for those test cases.

The three Swagger scenarios provide the separate manual verification of the real agent integration.

The files `src/rag/test_pipeline.py` and `src/rag/test_retriever.py` are manual test scripts containing `main()` functions, not automated pytest test cases. They are not included in the count of five automated tests.

### 9.4 Environment and Git

- Recreated a separate Python 3.12 environment after installation problems with the original environment.
- Verified that LangChain and `create_agent` import successfully.
- Verified that the existing RAG pipeline runs in the new environment.
- Confirmed that `uv lock --check` completes without an error.
- Re-ran the automated API tests successfully after retrieval and API integration changes.
- Previously committed and pushed the agent implementation, dependency updates, and relevance-filtering changes.
- Reviewed the latest integration changes with `git diff`.
- Confirmed that `git diff --check` returned no errors before documentation updates.

Broader automated testing is still needed.

## 10. Known Limitations

- The relevance threshold of `0.25` is an initial setting. It has been manually tested with selected relevant and unsupported questions, but it needs evaluation against more questions.
- Similarity scores do not guarantee that every returned chunk contains all the information needed to answer a question.
- The current ingestion logic does not automatically refresh chunks when an existing source file is modified.
- The five automated tests cover API behavior. Additional automated tests for retrieval, answer generation, and agent behavior would improve reliability.
- The agent's document-search tool currently runs the full RAG question-answering pipeline before returning its result to the agent.
- The three manually verified agent scenarios provide useful initial coverage but are not sufficient to establish production reliability.
- Authentication, authorization, rate limiting, monitoring, and other production security considerations still need to be evaluated before any real company deployment.
- The original `.venv` encountered incomplete package metadata and Windows access or file-linking errors. It has been left untouched.

These are improvement areas, not reasons to rebuild the existing RAG foundation.

## 11. Phase Status

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

**Status: Core implementation completed; agent integration verified.**

Implemented:

- `GET /health` and `POST /ask`.
- Pydantic request validation.
- Error handling and logging.
- Integration of `POST /ask` with `ask_agent()`.
- Lazy initialization and caching of the agent and RAG pipeline.
- Five passing automated API tests.
- Manual verification of the integrated endpoint using three scenarios.

Remaining work includes expanded automated testing, configuration improvements, and production-readiness improvements.

### Phase 3 — Agentic AI

**Status: Initial implementation and API integration completed; further development ongoing.**

Implemented:

- LangChain agent using `create_agent`.
- `search_company_docs` tool.
- Connection to the existing RAG pipeline.
- Instructions for clarifying vague requests.
- Instructions to avoid unsupported company-specific claims.
- Lazy initialization and caching.
- Integration with FastAPI's `/ask` endpoint.
- Manual verification of relevant, vague, and unsupported questions through the API.
- Five passing automated API tests following the integration changes.

Remaining work:

- Add automated tests for agent behavior and tool invocation.
- Test a wider range of relevant, vague, and unsupported questions.
- Improve agent error handling and reliability.
- Evaluate whether the search tool should return document passages directly instead of a complete RAG-generated answer.
- Continue production-oriented improvements.

### Phase 4 — LangGraph

**Status: Not started.**

Planned: Use LangGraph to orchestrate multi-step workflows with state, nodes, edges, and conditional routing.

### Phase 5 — MCP

**Status: Not started.**

Planned: Expose and use support-related tools through the Model Context Protocol.

### Phase 6 — Production Improvements

**Status: Not started.**

Planned: Improve testing, logging, error handling, configuration, security, maintainability, monitoring, and deployment readiness.

## 12. Git and GitHub

- Git branch: `main`
- GitHub repository: https://github.com/rajpatel-09/NovaDesk-AI
- Previously pushed agent and relevance-filtering source-code milestone: `b634858` — `feat: add agent and relevance filtering`
- Previously pushed documentation milestone: `3b23a17` — `docs: update project documentation`

The latest Agentic AI/FastAPI integration changes were verified locally, but the modified implementation files and documentation still need to be committed and pushed as a new milestone.

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

## 13. Immediate Next Steps

1. Finish updating `PROJECT_CONTEXT.md` and `LEARNING_LOG.md`.
2. Review all documentation changes for consistency with the implemented code.
3. Run `git diff --check` and the automated API test suite.
4. Review the final code and documentation changes.
5. Stage, commit, and push the verified integration milestone to GitHub.
6. Add automated tests for agent behavior and tool invocation.
7. Continue improving NovaDesk AI without unnecessarily rebuilding the tested RAG foundation.