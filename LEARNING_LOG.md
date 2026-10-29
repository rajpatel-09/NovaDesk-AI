# NovaDesk-AI — Learning Log

This file tracks the practical work, concepts explored, tests completed, and remaining learning tasks for NovaDesk-AI.

**Last updated:** October 29, 2026
**Current phase:** Phase 3 — Agentic AI
**Current priority:** Finish the documentation and Git milestone, then understand `tests/test_agent.py` line by line.

---

## Phase 1 — Retrieval-Augmented Generation (RAG)

**Status: Core implementation complete**

### Work completed

- Created a company knowledge base containing HR, IT, and security documents.
- Implemented document loading and text chunking.
- Generated embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
- Stored document embeddings in ChromaDB.
- Implemented retrieval of relevant document chunks.
- Configured retrieval to return the top three chunks.
- Experimented with a relevance threshold to filter weak matches.
- Integrated the retriever with the LLM to generate answers from retrieved context.
- Added source information to answers.
- Added a fallback response when relevant information cannot be found.

### Concepts explored

- Why RAG is useful for company-specific questions.
- The difference between document retrieval and answer generation.
- How embeddings and vector similarity support semantic search.
- How the number of retrieved chunks affects the information available to the LLM.
- Why retrieving irrelevant chunks can reduce answer quality.
- Why the application needs a fallback when the knowledge base does not contain an answer.

### Practical verification

Tested questions about company policies and VPN troubleshooting, along with an out-of-scope question to examine how the application handles unavailable information.

**Outcome:** The core RAG pipeline is implemented and integrated into the project.

---

## Phase 2 — FastAPI

**Status: Core implementation and API tests complete**

### Work completed

- Created the FastAPI application.
- Implemented `GET /health`.
- Implemented `POST /ask`.
- Added Pydantic request validation.
- Added basic logging and error handling.
- Exposed interactive documentation through Swagger UI.
- Integrated the `/ask` endpoint with `ask_agent()`.

### Concepts explored

- What an API does and why the application needs one.
- How an HTTP request reaches an endpoint.
- How Pydantic validates incoming request data.
- How the API calls the application's AI logic.
- How Swagger UI can be used to manually test endpoints.
- Why errors and invalid requests need appropriate handling.

### Verification

Manually tested the API using Swagger UI, including company-policy questions, a vague question requiring clarification, and a question not supported by the company knowledge base.

The API test suite contains five tests.

**Outcome:** The core API implementation and its automated tests are in place.

---

## Phase 3 — Agentic AI

**Status: Initial implementation complete; understanding and verification in progress**

### 1. Created the document-search tool

**File:** `src/agent/tools.py`

Implemented the `search_company_docs` tool using LangChain's `@tool` decorator.

The tool connects the agent to the existing RAG pipeline rather than duplicating document retrieval and answer-generation logic.

Conceptually:

```text
Agent requests a company-document search
                  |
                  v
         search_company_docs
                  |
                  v
       Existing RAG pipeline
                  |
                  v
        Answer and source data
```

### 2. Created the agent

**File:** `src/agent/agent.py`

Implemented an agent using LangChain's `create_agent`.

The configuration includes:

- The LLM provided by `AnswerGenerator`.
- The `search_company_docs` tool.
- A system prompt defining the assistant's role and behavior.
- `@lru_cache(maxsize=1)` to reuse the configured agent.
- `ask_agent(question)` to invoke the agent and return the final message content.

### 3. Defined the agent's behavior

The system prompt instructs the assistant to:

- Act as NovaDesk, an IT helpdesk assistant.
- Use company-document search for relevant policy and procedure questions.
- Ask a concise clarifying question when a request is too vague.
- Base company-specific answers on the available tool results.
- Avoid inventing information when the documents do not support an answer.

### 4. Examined tool-calling behavior

Manually investigated the messages returned by the agent when answering a VPN troubleshooting question.

Observed the following sequence:

```text
HumanMessage
     |
     v
AIMessage requesting a tool call
     |
     v
ToolMessage containing the tool result
     |
     v
Final AIMessage
```

Also tested a vague question. The agent asked for clarification without invoking the search tool.

Directly invoked `search_company_docs` to inspect the tool's returned result.

### Concepts explored

- The difference between an ordinary LLM call and an agent workflow.
- The roles of the agent, LLM, and tool.
- What `create_agent()` configures.
- How `@tool` exposes a function for agent use.
- Why the tool must be included in the agent's configuration.
- The purpose of a system prompt.
- How `invoke()` passes input to the agent.
- The roles of `HumanMessage`, `AIMessage`, and `ToolMessage`.
- How the framework executes tools and returns their results to the model.
- Why `@lru_cache(maxsize=1)` avoids repeatedly creating the same configured agent.
- How `ask_agent()` extracts the final response instead of returning the full message history.

**Important learning note:** These concepts have been explored through explanations and practical experiments. The next step is to strengthen understanding by reviewing the test code and connecting every assertion to the production implementation.

---

## Agent Testing

**File:** `tests/test_agent.py`

Added three automated tests.

### Test 1: Document-search tool

`test_search_company_docs_uses_rag_pipeline`

Checks that the search tool passes the expected question to the RAG pipeline and returns the expected answer.

### Test 2: Final-answer extraction

`test_ask_agent_returns_final_answer`

Checks that `ask_agent()` passes the expected input to the configured agent and returns the final answer content.

### Test 3: Agent configuration and caching

`test_get_agent_reuses_configured_agent`

Checks that agent creation receives the expected model, document-search tool, and important system-prompt instructions. It also checks that repeated calls reuse the cached agent.

### Testing techniques introduced

- `monkeypatch` to replace dependencies during a test.
- Fake classes and objects to simulate dependencies.
- `SimpleNamespace` to create lightweight objects with attributes.
- Assertions to verify expected behavior.
- Cache clearing to isolate the agent initialization test.
- Test isolation to avoid unnecessary live model calls.

**Current status:** All three agent tests passed in the latest recorded run.

**Remaining learning task:** The user has not yet fully understood `tests/test_agent.py`. Explain the complete file line by line before adding more agent functionality. Cover the imports, fake objects, monkeypatching, test inputs, assertions, caching behavior, and how each test relates to the corresponding production code.

---

## Automated Test Results

The latest recorded full test run was:

```text
8 passed in 2.68s
```

The test suite currently contains:

| Test file | Number of tests |
|---|---:|
| `tests/test_api.py` | 5 |
| `tests/test_agent.py` | 3 |
| **Total** | **8** |

Run the full suite with:

```powershell
uv run python -m pytest -v
```

Run only the agent tests with:

```powershell
uv run python -m pytest tests/test_agent.py -v
```

Run only the API tests with:

```powershell
uv run python -m pytest tests/test_api.py -v
```

These are the latest recorded results, not a guarantee that the tests will still pass after future changes. Rerun them before committing.

---

## Development Environment Notes

The project uses Python 3.12 and uv.

The working environment is configured outside the project directory because of earlier Windows environment and package-linking issues.

In each new VS Code PowerShell terminal, set the environment with:

```powershell
$env:UV_PROJECT_ENVIRONMENT = "$env:LOCALAPPDATA\uv-envs\novadesk-ai"
```

Run project commands using `uv run` to use the configured environment.

The application can be started with:

```powershell
uv run uvicorn src.api.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Current Git and Documentation Tasks

Before the latest documentation milestone is considered complete:

1. Save `README.md`, `PROJECT_CONTEXT.md`, and this file.
2. Inspect `git status --short` to confirm the actual changed files.
3. Review the code changes and remove only unintended edits.
4. Run the complete test suite.
5. Run `git diff --check`.
6. Review the staged changes before committing.
7. Commit and push the intended milestone to GitHub.

The latest previously recorded pushed commit was `be13377` (`feat: integrate agent with FastAPI`). Confirm the actual repository state before making a new commit.

---

## Upcoming Learning Plan

### Immediate next step

Understand `tests/test_agent.py` line by line, using the existing source files to explain how the test code works.

### Remaining Phase 3 work

Continue practical Agentic AI learning and verification. Do not mark Phase 3 complete until the implementation and behavior have been reviewed sufficiently.

### Future phases

- **Phase 4:** LangGraph
- **Phase 5:** Model Context Protocol (MCP)
- **Phase 6:** Production improvements, final testing, documentation, and project finishing

These phases have not yet been completed.

---

## Learning Approach

The project should continue with a practical, beginner-friendly approach:

- Explain why a concept is needed before introducing code.
- Review existing code before changing it.
- Connect theory to the NovaDesk-AI implementation.
- Use small, related tasks and practical experiments.
- Explain terminal commands and Git operations clearly.
- Use tests to check understanding, not just to obtain a passing result.
- Update the documentation after meaningful milestones.

**Next learning objective:** Understand how the three tests in `tests/test_agent.py` work and why they are written this way.

---

**End of learning log.**
