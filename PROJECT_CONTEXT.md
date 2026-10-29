# NovaDesk-AI — Project Context

**Last updated:** October 29, 2026
**Project:** NovaDesk-AI — AI IT Helpdesk Copilot
**Repository:** https://github.com/rajpatel-09/NovaDesk-AI.git
**Current learning phase:** Phase 3 — Agentic AI
**Current focus:** Finish documentation, review the current changes, then understand `tests/test_agent.py` line by line.

---

## 1. Project Overview

NovaDesk-AI is an AI-powered IT helpdesk assistant that answers employee questions using internal company documentation.

The project is being developed as an internship learning project with the goal of building practical, maintainable AI application skills.

The planned learning sequence is:

1. Retrieval-Augmented Generation (RAG)
2. FastAPI
3. Agentic AI
4. LangGraph
5. Model Context Protocol (MCP)
6. Production improvements and project finishing

**Important:** Phase 1 and the core Phase 2 implementation are complete. Phase 3 implementation has started, but understanding and verification are still in progress. Do not treat Phase 3 as mastered or completed.

## 2. Development Environment

**Project directory**

```text
C:\Users\Lenovo\OneDrive\Desktop\NovaDesk-AI
```

**Python:** 3.12
**Package manager:** uv
**Git branch:** `main`

The project uses an external uv environment because of earlier environment and package-linking issues on Windows.

At the beginning of each new VS Code PowerShell terminal, run:

```powershell
$env:UV_PROJECT_ENVIRONMENT = "$env:LOCALAPPDATA\uv-envs\novadesk-ai"
```

Run Python and tests through uv so the correct environment is used.

**Run the full test suite:**

```powershell
uv run python -m pytest -v
```

Use `python -m pytest` rather than plain `pytest` because it correctly handles the project's module import path in this setup.

**Start the API:**

```powershell
uv run uvicorn src.api.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## 3. Technology Stack

| Area | Technology |
|---|---|
| Language | Python |
| Dependencies and environment | uv |
| LLM | Groq via LangChain |
| Agent | LangChain `create_agent` |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector database | ChromaDB |
| API | FastAPI |
| Validation | Pydantic |
| Automated tests | pytest |

The LLM has been configured using the Groq model `openai/gpt-oss-20b` through `ChatGroq`.

The `.env` file contains the Groq API key and must never be committed to Git.

## 4. Current Architecture

The core application flow is:

```text
Employee question
       |
       v
FastAPI POST /ask
       |
       v
ask_agent(question)
       |
       v
LangChain agent
       |
       v
search_company_docs tool
       |
       v
RAG pipeline
       |
       v
Retrieve relevant document chunks
       |
       v
Generate answer with source information
       |
       v
Tool result returned to agent
       |
       v
Final agent answer
       |
       v
API response
```

The agent can also ask the user a clarifying question when the request is vague and a company-document search is unnecessary.

## 5. Current Project Structure

```text
NovaDesk-AI/
├── data/
│   ├── company_docs/
│   │   ├── HR/
│   │   │   └── leave_policy.txt
│   │   ├── IT/
│   │   │   ├── vpn_troubleshooting.txt
│   │   │   └── software_installation_policy.txt
│   │   └── SECURITY/
│   │       └── password_security_policy.txt
│   └── vector_store/
├── src/
│   ├── agent/
│   │   ├── agent.py
│   │   └── tools.py
│   ├── api/
│   │   └── main.py
│   ├── ingestion/
│   │   └── loader.py
│   └── rag/
│       ├── generator.py
│       ├── pipeline.py
│       └── retriever.py
├── tests/
│   ├── test_api.py
│   └── test_agent.py
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
├── PROJECT_CONTEXT.md
└── LEARNING_LOG.md
```

This is a working representation of the structure. Other project files may exist as development continues.

## 6. Phase 1 — RAG

**Status: Core implementation complete**

The RAG implementation includes:

- Loading company `.txt` documents.
- Splitting documents into chunks.
- Creating embeddings using Sentence Transformers.
- Storing and retrieving vectors with ChromaDB.
- Retrieving the top three chunks for a question.
- Applying a relevance threshold to filter weak matches.
- Generating answers using the retrieved context.
- Returning source information.
- Using a fallback response when relevant information is unavailable.

The ChromaDB collection is named `novadesk_docs`. The persisted vector store is located in `data/vector_store/`.

The RAG implementation is accessed through `RAGPipeline`, which combines retrieval and answer generation.

The fallback response used by the pipeline is:

```text
I could not find relevant information in the company documents.
```

### Company knowledge base

The current synthetic knowledge base covers:

- HR leave policy.
- VPN troubleshooting.
- Software installation policy.
- Password security policy.

The knowledge base previously contained four documents and eleven chunks. These counts should be rechecked if documents or chunking settings change.

## 7. Phase 2 — FastAPI

**Status: Core API implementation and tests complete**

The API currently includes:

- `GET /health` for a health check.
- `POST /ask` for employee questions.
- Pydantic request validation.
- Basic logging and error handling.
- Integration with `ask_agent()`.

The `/ask` endpoint uses the agent rather than calling the RAG pipeline directly.

Swagger UI was used to manually verify the main behaviors:

- A casual leave question returned the documented allowance of 12 days per year.
- A vague question prompted the assistant to ask for clarification.
- An unsupported question about FIFA did not result in an invented company policy.

These are manual checks, not a guarantee that every possible question will be answered correctly.

## 8. Phase 3 — Agentic AI

**Status: Initial implementation exists; learning and testing are ongoing**

### `src/agent/tools.py`

The `search_company_docs` tool is exposed through LangChain's `@tool` decorator.

Its responsibility is to pass the supplied question to the cached RAG pipeline and return the result.

Conceptually:

```text
Agent requests a document search
       |
       v
search_company_docs(question)
       |
       v
get_rag_pipeline().ask(question)
       |
       v
Answer and sources from RAG
```

### `src/agent/agent.py`

The agent implementation includes:

- `create_agent` to configure the LangChain agent.
- `AnswerGenerator().llm` as the model.
- `search_company_docs` as an available tool.
- A system prompt defining the assistant's role and answer boundaries.
- `@lru_cache(maxsize=1)` on `get_agent()` to reuse the configured agent.
- `ask_agent(question)` to invoke the agent and extract the final message content.

The system prompt instructs the agent to:

- Behave as NovaDesk, an IT helpdesk assistant.
- Use company-document search for policy and procedure questions.
- Ask a concise clarifying question when the request is too vague.
- Use company facts supported by the tool results.
- Avoid inventing an answer when the documentation does not provide the required information.

### Concepts already explored

The following behaviors have been manually examined:

1. A VPN question caused the agent to request `search_company_docs`.
2. The tool result was returned to the agent.
3. The agent then produced a final answer.
4. A vague question such as “It does not work. Help me.” resulted in a clarifying question without a tool call.
5. A direct call to `search_company_docs.invoke(...)` returned the RAG pipeline's result.

The tool-calling message sequence was observed as:

```text
HumanMessage
     |
     v
AIMessage with tool call
     |
     v
ToolMessage with tool result
     |
     v
Final AIMessage
```

These experiments provide a practical starting point, but the implementation must still be understood and reviewed carefully.

## 9. Agent Tests

**Test file:** `tests/test_agent.py`

Three tests have been added:

1. `test_search_company_docs_uses_rag_pipeline`
   - Checks that the search tool passes the expected question to the RAG pipeline and returns its answer.

2. `test_ask_agent_returns_final_answer`
   - Checks that `ask_agent()` invokes the configured agent with the expected payload and returns the final answer content.

3. `test_get_agent_reuses_configured_agent`
   - Checks agent configuration, verifies that the model and tool are supplied, checks important system-prompt instructions, and verifies that the cached agent is reused.

The tests use `monkeypatch`, fake objects, and `SimpleNamespace` to isolate behavior. They do not require live model calls to test these specific code paths.

**Important learning task:** The user has not yet understood this test file line by line. Do not skip directly to adding more tests or moving to LangGraph. After documentation is finished and the current changes are committed, teach `tests/test_agent.py` from the beginning, explaining each import, function, fixture-like use of `monkeypatch`, fake object, assertion, and the reason for each test. Show how the test connects to the actual production code.

## 10. Latest Test Status

The latest recorded full test run was:

```text
8 passed in 2.68s
```

This comprised five API tests and three agent tests.

The agent test command is:

```powershell
uv run python -m pytest tests/test_agent.py -v
```

The API test command is:

```powershell
uv run python -m pytest tests/test_api.py -v
```

The full suite should be rerun after any further code changes.

## 11. Git and Pending Changes

**Repository:** https://github.com/rajpatel-09/NovaDesk-AI.git
**Branch:** `main`

The latest previously recorded pushed commit was `be13377` (`feat: integrate agent with FastAPI`).

At the latest review, the intended remaining code changes were:

- `src/agent/agent.py` — an explanatory comment documenting final-answer extraction.
- `tests/test_agent.py` — the three new agent tests.

The documentation is also being updated. Since local files may have changed during this process, verify the actual state with:

```powershell
git status --short
```

Do not assume the listed files are still the complete set of changes.

Before committing:

1. Check that the documentation is saved.
2. Run the full test suite.
3. Inspect the changes using `git diff` and `git diff --check`.
4. Stage only the intended files.
5. Commit and push only after reviewing the staged changes.

Do not discard user changes simply to make the working tree clean.

## 12. Current Tasks — In Order

1. Finish replacing and saving `README.md`.
2. Finish replacing and saving `PROJECT_CONTEXT.md`.
3. Update `LEARNING_LOG.md` with the recently completed learning and testing work.
4. Review the modified and untracked files.
5. Run all eight tests again and confirm the output.
6. Commit and push the reviewed milestone.
7. Begin a careful, line-by-line walkthrough of `tests/test_agent.py`.
8. Only after the user understands the current test code, continue further Agentic AI learning and implementation.

## 13. Learning and Mentoring Instructions

The user is a beginner in Agentic AI and is building this project to gain practical, industry-oriented skills.

When continuing this project:

- Explain **why** a concept or code change is needed before showing the implementation.
- Inspect and explain the existing code before replacing or extending it.
- Use realistic examples from NovaDesk-AI.
- Explain Python, LangChain, testing, and Git concepts in beginner-friendly terms.
- Combine a few related small tasks when appropriate, but do not overwhelm the user with a large batch of changes.
- Prefer a single combined checkpoint over frequent confirmation questions.
- Clearly state where commands must be run: VS Code PowerShell terminal or another location.
- Do not imply that the user has mastered code just because it runs or tests pass.
- Remind the user to update `README.md`, `PROJECT_CONTEXT.md`, and `LEARNING_LOG.md` after meaningful milestones.

**Next learning objective:** Understand the three tests in `tests/test_agent.py` line by line, after completing the documentation and Git milestone.

---

**End of project context.**