# NovaDesk AI — Learning Log

This file records my learning, implementation, debugging, testing, and progress throughout the NovaDesk AI project.

**Last updated:** October 24, 2026

---

## Day 1 — Project Foundation

### Objective

Set up a clean project for NovaDesk AI.

### What I learned

- Git tracks changes in a project.
- GitHub hosts Git repositories online.
- A Python virtual environment keeps project dependencies separate.
- NovaDesk AI has its own project environment, separate from the previous YTRAG learning project.
- Project-based learning means learning a concept and immediately applying it to a real implementation.

### What I implemented

- Created the NovaDesk AI project and its initial folder structure.
- Created `PROJECT_CONTEXT.md`, `LEARNING_LOG.md`, and `README.md`.
- Configured `.gitignore`.
- Initialized Git and created initial commits.
- Renamed the project folder from `AI-IT-Helpdesk-Copilot` to `NovaDesk-AI`.

### Problems encountered

The old YTRAG virtual environment was initially active. I deactivated it and switched to the NovaDesk AI project environment.

### What I understood

- YTRAG remains my previous learning/tutorial project.
- NovaDesk-AI is my internship-oriented project.
- Each project needs its own appropriate dependencies and environment.
- Git provides a history of project changes.

---

## Phase 1 — RAG Core Implementation

### Objective

Build a working Retrieval-Augmented Generation (RAG) system that answers employee questions using company documentation.

### Technology used

- Python 3.12
- `uv` for dependency management
- LangChain
- ChatGroq with `openai/gpt-oss-20b`
- Hugging Face Sentence Transformers
- `sentence-transformers/all-MiniLM-L6-v2` embeddings
- ChromaDB through `langchain-chroma`

### What I implemented

- Document loading and splitting in `src/ingestion/`.
- Embedding creation and storage in ChromaDB.
- A company-document retriever in `src/rag/retriever.py`.
- Answer generation in `src/rag/generator.py`.
- An end-to-end pipeline in `src/rag/pipeline.py`.
- Source-document reporting in the final response.
- A fallback response for questions when no relevant documents are retrieved.

### Company knowledge base

Four company documents were added under `data/company_docs/`:

1. `HR/leave_policy.txt`
2. `IT/vpn_troubleshooting.txt`
3. `IT/software_installation_policy.txt`
4. `SECURITY/password_security_policy.txt`

The document loader discovers `.txt` files recursively under `data/company_docs/`.

The ChromaDB collection is named `novadesk_docs` and is persisted in `data/vector_store/`.

The ingestion pipeline initially reported 9 chunks. After adding the software installation policy, it reported 11 chunks.

### What I learned

- RAG retrieves document chunks and gives them to the language model as context.
- Document embeddings are created during ingestion. A user's question is embedded when a search is performed.
- The language model receives the retrieved context rather than the entire vector database.
- Embeddings represent text numerically so semantic similarity can be used for retrieval.
- Source paths help identify the documents associated with retrieved chunks.
- A fallback response helps prevent the application from inventing an unsupported company-specific answer.

### RAG workflow

Employee question → Retrieve relevant chunks → Generate an answer using the retrieved context → Return the answer and source paths.

---

## Retrieval Experiments — Understanding `top_k`

### Objective

Understand how the number of retrieved chunks affects relevance and answer quality.

### What I tested

I compared `top_k=3` with `top_k=5` for this question:

> How many casual leave days do employees get?

With `top_k=5`, the retrieved context included unrelated password-security information. The answer still correctly stated 12 days, but the reported sources included the security policy.

With `top_k=3`, the answer remained 12 days, and the reported source was the relevant HR leave policy.

### What I learned

- `top_k` controls the maximum number of chunks retrieved.
- A higher `top_k` can provide additional context but may introduce irrelevant information.
- More chunks do not automatically mean a better answer.
- The closest matches are not guaranteed to be relevant.
- A source filename alone does not prove that the generated answer is supported by that source.
- `top_k=3` worked well for this particular question but is not necessarily optimal for every question.

### Important concept

Retrieval quality and answer quality are related, but they are not the same. Both should be evaluated when testing a RAG system.

---

## Adding a New Company Document

### Objective

Extend the knowledge base without unnecessarily duplicating previously ingested documents.

### What I implemented

- Added `data/company_docs/IT/software_installation_policy.txt`.
- Updated the vector-store logic in `src/ingestion/vectorstore.py` to identify source paths already stored.
- Added chunks from source files that were not already present.
- Ran the ingestion pipeline and confirmed that the collection contained 11 chunks.
- Tested the new policy through the RAG pipeline.

### Test question

> Do employees need IT approval before installing software on company devices?

### Observed result

The assistant correctly answered that IT department approval is required before employees install software on company devices.

The software installation policy appeared in the reported sources. The VPN troubleshooting document was also retrieved, showing that retrieval relevance could still be improved.

### Current limitation

The current ingestion logic handles newly added source files. It does not automatically update or replace chunks when an existing source file is modified.

---

## Debugging and Implementation Lessons

### Function-name mismatch

The ingestion pipeline imported `create_vectorstore`, while the vector-store file initially defined `create_vectors`.

I corrected the function name so the import and function definition matched, then confirmed that the import worked.

### Retriever error

An error occurred:

`AttributeError: 'Chroma' object has no attribute 'search_kwargs'`

The cause was that `create_retriever()` returned the Chroma vector store rather than a LangChain retriever.

I corrected the function to return:

`vectorstore.as_retriever()`

After the change, the RAG pipeline successfully retrieved the software installation policy and generated an answer.

### What I learned

- Read the traceback to identify which file and line caused an error.
- Understand what a function returns before using its result.
- A vector store and a retriever have related but different interfaces.
- Fix the underlying cause rather than changing unrelated code.
- Test a change after fixing it.

---

## Answer Grounding and Out-of-Scope Testing

### Objective

Check whether the assistant avoids unsupported answers when company documents do not contain the requested information.

### What I tested

I asked:

> Who won the FIFA World Cup in 2018?

This question was outside the scope of the company knowledge base.

### Observed result

The assistant returned a fallback-style response rather than answering from general knowledge. However, it still retrieved unrelated company documents.

### What I learned

- Company-specific answers should be supported by retrieved company context.
- When relevant information is unavailable, the assistant should say so rather than guess.
- A retrieved result can be irrelevant even when it ranks among the closest matches.
- The absence of a relevant retrieved chunk does not necessarily mean the information is absent from the knowledge base.
- A robust system needs a mechanism to reject weak retrieval results and handle insufficient evidence.

This initial behavior was useful, but it did not guarantee safe handling of every out-of-scope question. Improving retrieval relevance became a subsequent task.

---

## Understanding the LLM Configuration

The answer generator uses ChatGroq with:

- Model: `openai/gpt-oss-20b`
- Temperature: `0`
- Reasoning format: `hidden`

### What I learned

- A lower temperature generally produces less variation in responses.
- A higher temperature generally allows more variation and creativity.
- Temperature `0` does not guarantee factual correctness.
- Correctness also depends on the retrieved context, instructions, and model behavior.
- For a company helpdesk, consistency and evidence-based answers are more important than unnecessary creativity.

---

## Phase 2 — FastAPI Core Implementation

### Objective

Expose the existing RAG pipeline through an HTTP API so another application can submit employee questions and receive answers.

### What I implemented

- Installed FastAPI with `uv add "fastapi[standard]"`.
- Created `src/api/main.py`.
- Implemented `GET /health` to check that the API responds.
- Implemented `POST /ask` to accept employee questions.
- Created a Pydantic `QuestionRequest` model for incoming requests.
- Initially connected `POST /ask` directly to the existing `RAGPipeline`.
- Tested the endpoints through FastAPI's interactive documentation at `/docs`.
- Confirmed that a company-policy question could be submitted and an answer returned.

### What I learned

- FastAPI exposes Python functions through HTTP endpoints.
- GET is commonly used to retrieve information, while POST is commonly used to submit data for processing.
- Pydantic models define and validate the expected structure of incoming requests.
- `request.question` accesses the question in the JSON request body.
- Calling the existing RAG pipeline reuses the retrieval and answer-generation logic.
- FastAPI converts returned Python dictionaries into JSON responses.
- FastAPI automatically provides interactive documentation at `/docs`.

### Problem encountered

Initially, the browser showed `ERR_CONNECTION_REFUSED` because the server had not finished starting. After the terminal confirmed that the application had started, the health-check endpoint worked.

The command `uv run fastapi dev src/api/main.py` also encountered an import-path problem with `src`.

Running the application from the project root with this command worked:

```powershell
uv run uvicorn src.api.main:app --reload
```

### How the API evolved

The first implementation called the RAG pipeline directly:

`get_rag_pipeline().ask(request.question)`

After implementing the agent, I changed the endpoint to call:

`ask_agent(request.question)`

This allowed the API to use the agent's decision-making and tool-calling workflow rather than bypassing the agent.

---

## FastAPI Validation — Empty and Missing Questions

### Objective

Reject invalid employee questions before passing them to the application logic.

### What I implemented

- Added a Pydantic field validator for the `question` field.
- Used `strip()` to remove leading and trailing whitespace.
- Rejected empty or whitespace-only questions with `ValueError`.
- Verified that invalid questions return HTTP 422.
- Tested a request with an empty JSON body and verified that the required `question` field is validated.

### Bug encountered

The validator initially attempted to raise a string, which caused a `TypeError`.

I corrected it by raising an exception:

`raise ValueError("Question must not be empty.")`

Pydantic then handled the invalid input as a validation error rather than an HTTP 500 server error.

### What I learned

- Validate user input before passing it to the application logic.
- `strip()` removes whitespace from both ends of a string.
- Python's `raise` statement must raise an exception.
- HTTP 422 indicates that a request failed validation.
- Pydantic automatically rejects requests that omit required fields.
- Test both invalid and valid requests after changing validation logic.

---

## FastAPI Error Handling — Unexpected Failures

### Objective

Handle unexpected errors without exposing internal exception details in API responses.

### What I implemented

- Added logging using Python's `logging` module.
- Wrapped the request-processing call in a `try`/`except` block.
- Used `logger.exception()` to record technical error information and the traceback.
- Returned an HTTP 500 response with a generic error message for unexpected exceptions.
- Temporarily introduced an intentional exception to test the error-handling path.
- Verified the API returned HTTP 500 and the generic error response.
- Updated the error log message to reflect that the endpoint now processes questions through the agent.

### What I learned

- Unexpected errors should be logged to help developers diagnose the cause.
- API responses should not expose internal exception details to callers.
- `logger.exception()` records the error and traceback when called inside an exception handler.
- `HTTPException` allows FastAPI to return a controlled HTTP error response.
- A simulated failure is useful for testing error-handling code.
- After testing a failure path, restore the real implementation and retest normal behavior.

---

## Automated API Testing

### Objective

Replace repeated manual checks with automated tests for NovaDesk AI's API.

### Tools used

- `pytest` — runs tests and reports results.
- `httpx` — supports HTTP client testing.
- `fastapi.testclient.TestClient` — sends simulated requests to the application without manually starting Uvicorn.

### What I implemented

Created `tests/test_api.py` with five automated tests covering:

1. `GET /health` returns HTTP 200 and the expected JSON response.
2. An empty or whitespace-only question returns HTTP 422.
3. A request missing the required question field returns HTTP 422.
4. A successful `/ask` response using a mocked processing function.
5. An unexpected exception returns HTTP 500 with a generic error response.

The tests initially mocked the RAG pipeline. After integrating the agent into FastAPI, I updated the successful-response and error-handling tests to mock `ask_agent` instead.

This ensures the tests target the function the API actually calls, without making the automated suite depend on live LLM calls.

### Lazy initialization

I implemented lazy initialization and caching so that importing the API during tests does not immediately initialize the full model and retrieval stack.

The agent and RAG pipeline also use caching to reuse their configured instances.

### Test command

```powershell
$env:UV_PROJECT_ENVIRONMENT = "$env:LOCALAPPDATA\uv-envs\novadesk-ai"
uv run python -m pytest -v
```

### Latest test results

The latest verified run after the agent integration and cleanup reported:

**5 passed in 1.48 seconds.**

### What I learned

- Automated tests help check that existing functionality still works after changes.
- `TestClient` tests FastAPI endpoints without manually starting the server.
- Assertions compare actual results with expected behavior.
- Tests can check both HTTP status codes and JSON content.
- Mocking allows API behavior to be tested without every test depending on live model calls.
- Lazy initialization prevents unnecessary setup during module imports.
- Running pytest as a Python module with `uv run python -m pytest` resolves the import-path issue encountered when running pytest directly.
- When an endpoint changes its internal dependency, its mocks and tests must be updated accordingly.

### Current limitation

The automated API tests mock `ask_agent` for successful processing and error handling. They verify the API layer but do not directly test the real agent's decision-making, tool invocation, or complete RAG retrieval and generation flow.

The real agent workflow is currently verified through manual API tests. Dedicated automated tests for agent behavior remain future work.

---

## Environment Recovery

**Date:** October 22, 2026

### Objective

Repair the Python dependency environment so the existing project and LangChain agent code could run without rebuilding the working RAG implementation.

### Problems encountered

The original project environment experienced several installation issues:

- LangChain was missing from the environment.
- Some installed packages had incomplete `RECORD` metadata.
- Windows returned `Access is denied` errors during package removal.
- Package installation using hardlinks failed with a Windows cloud-file error.

Restarting Windows did not resolve all the installation issues.

### What I did

- Added `langchain>=1.4.7` to `pyproject.toml` using `uv add langchain --no-sync`.
- Updated the project lockfile.
- Left the original `.venv` untouched.
- Created a separate Python 3.12 environment at `%LOCALAPPDATA%\uv-envs\novadesk-ai`.
- Set `UV_PROJECT_ENVIRONMENT` in the active PowerShell session to direct `uv` to the new environment.
- Successfully installed dependencies using:

```powershell
uv sync --link-mode=copy
```

- Verified that LangChain and `create_agent` import successfully.
- Confirmed that `uv lock --check` completed without an error.
- Ran the existing RAG pipeline successfully in the new environment.
- Re-ran the automated API tests successfully.

### What I learned

- Declaring a dependency and installing it into the active environment are separate steps.
- `uv sync` reconciles the environment with project dependencies and the lockfile.
- A virtual environment can be created outside the project folder, but `uv` must be configured to use it.
- The `--link-mode=copy` option avoids the hardlink operation that caused the installation failure.
- Environment recovery does not require rebuilding project source code.

### Important environment note

The `UV_PROJECT_ENVIRONMENT` setting was applied in the working PowerShell session. A new terminal must have that setting configured again unless it inherits or defines it elsewhere.

The original `.venv` remains untouched.

---

## Agentic AI — Initial Implementation

### Objective

Introduce an agent that can decide when to search company documents and when to ask a clarifying question, while reusing the existing RAG pipeline.

### What I implemented

Created `src/agent/agent.py` using LangChain's `create_agent`.

Created `src/agent/tools.py` with the `search_company_docs` tool, connected to the existing `RAGPipeline`.

The agent's instructions tell it to:

- Use company documents for company-specific policies and IT procedures.
- Ask a concise clarifying question when the request is too vague to understand.
- Use company-specific facts only when supported by tool results.
- Admit when relevant company information cannot be found rather than inventing a policy.

The implementation uses lazy initialization and caching for the agent and its RAG pipeline.

### Test 1 — Relevant question

Question:

> How can I troubleshoot VPN connection problems?

Observed result:

- The agent called `search_company_docs`.
- The tool retrieved information from the VPN troubleshooting guide.
- The agent used the tool result to produce an answer.

I inspected the agent's message sequence and observed a `ToolMessage` associated with `search_company_docs`, confirming that the tool was called.

### Test 2 — Vague question

Question:

> It does not work. Help me.

Observed result:

- The agent asked what specific issue the user was experiencing.
- No document-search tool call occurred.

This matched the agent's instruction to clarify a vague request before searching the knowledge base.

### Test 3 — Unsupported question

Question:

> What is NovaTech Solutions policy on reimbursing FIFA World Cup tickets?

Observed result:

- The agent called the document-search tool.
- The retrieval pipeline returned a fallback response.
- The agent stated that it could not locate the reimbursement policy rather than inventing one.

Initially, the retriever also listed unrelated company documents. This exposed a remaining weakness in retrieval relevance, which was addressed in the next milestone.

### What I learned

- An agent can decide when to use an available tool based on the question and its instructions.
- A tool returns information that the agent can use to formulate its response.
- A vague question may require clarification rather than immediate retrieval.
- Agent instructions guide behavior, but the behavior must be tested.
- Inspecting `HumanMessage`, `AIMessage`, and `ToolMessage` objects helps reveal the agent's execution path.

---

## Retrieval Improvement — Similarity Score Threshold

### Objective

Prevent weak document matches from being presented as relevant evidence for unsupported questions.

### Problem encountered

The original retriever returned the closest documents even when their relevance was weak. This meant that unrelated source documents could appear in the RAG pipeline's fallback response.

### Diagnostic experiment

I compared retrieval relevance scores for two questions.

**Relevant question:**

> How can I troubleshoot VPN connection problems?

The returned scores were:

- `0.476` — VPN troubleshooting guide
- `0.410` — VPN troubleshooting guide
- `0.190` — VPN troubleshooting guide

**Unsupported question:**

> What is NovaTech Solutions policy on reimbursing FIFA World Cup tickets?

The returned scores were:

- `0.196` — software installation policy
- `0.102` — leave policy
- `0.092` — password security policy

The results showed a clear difference for these two tested questions.

### What I changed

Updated `src/ingestion/retriever.py` to use ChromaDB's `similarity_score_threshold` retrieval strategy with an initial threshold of `0.25`.

The retriever now rejects matches that score below the configured threshold.

### What I tested

**Unsupported FIFA reimbursement question**

The retriever rejected the weak matches. The RAG pipeline returned its fallback response without listing unrelated sources.

**Relevant VPN troubleshooting question**

The pipeline continued to retrieve the VPN troubleshooting guide and produce a useful answer.

**Agent behavior**

I re-tested the agent with both the unsupported FIFA question and the relevant VPN question. The unsupported question returned a fallback response, and the relevant question continued to produce a grounded answer.

### What I learned

- Retrieval should not assume that the closest available matches are sufficiently relevant.
- A relevance threshold can filter weak matches before answer generation.
- Relevance scores are useful diagnostic evidence, but a threshold is not universally correct.
- The initial `0.25` threshold needs evaluation against a broader set of relevant and unsupported questions.
- Retrieval filtering improves the context supplied to the generator and reduces irrelevant source reporting.

### Current limitation

The threshold has been manually tested with selected questions. Additional experiments and automated retrieval tests are needed before treating it as suitable for every question.

---

## Latest Milestone — Agentic AI Integrated into FastAPI

**Date:** October 24, 2026

### Objective

Connect the existing LangChain agent to the real FastAPI `/ask` endpoint and verify that supported questions, vague requests, and unsupported questions behave as expected.

### Why this change was needed

Previously, `POST /ask` called the RAG pipeline directly. The agent had been implemented and tested separately, but the API did not yet use its decision-making and tool-calling capabilities.

Changing the endpoint to call `ask_agent()` allows requests through FastAPI to use the agent.

### What I changed

**In `src/api/main.py`:**

- Imported `ask_agent` from `src.agent.agent`.
- Replaced the direct RAG pipeline call with `ask_agent(request.question)`.
- Removed the API-level lazy RAG pipeline factory because the agent and tool now manage their own cached components.
- Updated the exception log message to refer to processing a question through the agent.

**In `tests/test_api.py`:**

- Updated the successful-response test to mock `src.api.main.ask_agent`.
- Updated the unexpected-error test to mock `src.api.main.ask_agent`.
- Preserved the five existing API test cases.

**In the agent files:**

- Kept the existing configured agent, system instructions, company-document search tool, and cached RAG pipeline.
- Added explanatory comments while reviewing the code.
- Preserved the existing RAG behavior instead of rebuilding it.

### Manual integration test results

I started the API using:

```powershell
$env:UV_PROJECT_ENVIRONMENT = "$env:LOCALAPPDATA\uv-envs\novadesk-ai"
uv run uvicorn src.api.main:app --reload
```

I then tested three requests through FastAPI's Swagger UI.

**Test 1 — Supported company-policy question**

Question:

> How many casual leave days do employees get?

Observed result: The endpoint returned the correct answer of 12 days per year and cited the leave policy.

**Test 2 — Vague question**

Question:

> It does not work. Help me.

Observed result: The agent asked for clarification rather than searching immediately.

**Test 3 — Unsupported company policy**

Question:

> What is NovaTech Solutions policy on reimbursing FIFA World Cup tickets?

Observed result: The agent acknowledged that the available company documents did not provide the answer rather than inventing a reimbursement policy.

All three requests returned HTTP `200 OK`, and the observed responses matched the expected behavior.

### Automated verification

After updating the endpoint and test mocks, I ran:

```powershell
uv run python -m pytest -v
```

The latest verified output reported:

**5 passed in 1.48 seconds.**

I also ran:

```powershell
git diff --check
```

It returned no whitespace errors.

I reviewed the changed files and removed unrelated test-command comments from `src/ingestion/pipeline.py`. I also corrected the API exception log message to refer to the agent.

### What I learned

- An API endpoint should call the correct application entry point for the intended workflow.
- The agent and the RAG pipeline have different responsibilities.
- The agent decides whether to use a tool; the tool delegates to the RAG pipeline when called.
- The RAG pipeline retrieves relevant context and generates a response.
- API tests must mock the dependency the endpoint actually calls.
- Mocked automated tests and manual integration tests verify different aspects of a system.
- Three successful manual requests provide useful initial evidence, but they do not prove that every possible request will work.
- `git diff` helps review implementation changes, while `git diff --check` checks for common whitespace mistakes.
- A working implementation should be documented and committed only after the changes and tests have been reviewed.

### Current architecture

The integrated request flow is:

```text
Employee Question
       |
       v
FastAPI POST /ask
       |
       v
ask_agent(question)
       |
       v
LangChain Agent
       |
       v
Decide Whether to Call a Tool
       |
       v
search_company_docs
       |
       v
Existing RAGPipeline
       |
       v
Retrieved Information and RAG-Generated Answer
       |
       v
Agent Final Response
       |
       v
FastAPI Response
```

For a vague question, the agent can ask for clarification without calling the search tool.

### Current limitation

The tool currently calls `RAGPipeline.ask()`, which performs both retrieval and answer generation. The agent then uses the tool result to produce its own final response.

This preserves the existing tested RAG pipeline but may involve an additional generation step. We will evaluate whether a retrieval-only tool would be a better design before changing it.

Dedicated automated tests for agent decisions and tool calls have not yet been added.

### Git status

The source changes have been reviewed locally, and the test suite passes. The implementation and documentation updates for this milestone still need final review, staging, committing, and pushing to GitHub.

---

## Git and GitHub Workflow

### Objective

Track implementation changes and publish the project to GitHub.

### What I learned

- `M` in `git status --short` means a tracked file has been modified.
- `??` means a file is untracked.
- `git add` stages selected changes for a commit.
- `git commit` saves a snapshot in local Git history.
- `git push` uploads local commits to the configured remote repository.
- A clean working tree means there are no uncommitted changes.
- `git diff` and `git diff --cached` help review unstaged and staged changes before committing.

### What I implemented

- Reviewed `.gitignore` and verified that `.env` and `data/vector_store/` are excluded.
- Reviewed intended source and dependency changes before staging.
- Staged selected files, created commits, and pushed project changes to GitHub.
- Reviewed the latest local source changes before preparing the current integration milestone.

### Repository

https://github.com/rajpatel-09/NovaDesk-AI

### Important existing commits

- `0f71f8d` — `feat: build core RAG pipeline and knowledge base`
- `6c078f0` — `test: add automated API endpoint tests`
- `1789145` — `perf: initialize RAG pipeline lazily`
- `b634858` — `feat: add agent and relevance filtering`
- `3b23a17` — `docs: update project documentation`

The previously recorded commits were successfully pushed to `origin/main`.

The latest Agentic AI/FastAPI integration changes have been tested locally but still need to be committed and pushed as a new milestone.

### Security lesson

Never commit API keys, credentials, or other secrets. Keep `.env` excluded through `.gitignore`.

---

## Current Project Status

### Phase 1 — RAG Core

**Status: Completed; relevance filtering added and manually tested.**

Implemented:

- Document ingestion and chunking.
- Embeddings and ChromaDB storage.
- Configurable retrieval.
- LLM answer generation.
- Source-document reporting.
- An initial relevance threshold of `0.25`.

### Phase 2 — FastAPI

**Status: Core implementation completed; agent integration verified.**

Implemented and tested:

- `GET /health` and `POST /ask`.
- Pydantic request validation.
- Error handling and logging.
- Lazy initialization and caching.
- Five automated API tests, all passing at the latest verified run.
- Integration of `POST /ask` with `ask_agent()`.
- Manual verification of three scenarios through Swagger UI.

### Phase 3 — Agentic AI

**Status: Initial implementation and FastAPI integration completed; further development ongoing.**

Implemented and manually tested:

- LangChain agent using `create_agent`.
- `search_company_docs` tool connected to the existing RAG pipeline.
- Tool usage for relevant VPN troubleshooting questions.
- Clarification of vague requests without calling the tool.
- Fallback handling for unsupported questions.
- Integration with the FastAPI `/ask` endpoint.
- Successful API behavior for the three documented manual scenarios.

Remaining work includes automated agent tests, wider behavior evaluation, and possible architecture improvements.

### Phase 4 — LangGraph

**Status: Not started.**

### Phase 5 — MCP

**Status: Not started.**

### Phase 6 — Production Improvements

**Status: Not started.**

---

## What I Still Need to Improve

- Writing code independently rather than only recognizing or understanding existing code.
- Becoming more confident with Git and GitHub.
- Evaluating retrieval relevance using a wider range of questions.
- Writing automated tests for retrieval and agent behavior.
- Understanding trade-offs between agent tools and RAG pipelines.
- Improving error handling, configuration, and production readiness.

I do not need to memorize every line of code immediately. My goal is to understand why the code exists, explain its logic, and gradually implement parts independently.

## Immediate Next Steps

1. Finish updating and reviewing `README.md`, `PROJECT_CONTEXT.md`, and `LEARNING_LOG.md`.
2. Run the automated API tests and `git diff --check`.
3. Review the final source-code and documentation changes.
4. Stage, commit, and push the verified integration milestone to GitHub.
5. Add automated tests for agent behavior and tool invocation.
6. Evaluate whether `search_company_docs` should return document passages directly rather than a complete RAG-generated answer.
7. Continue with LangGraph, then MCP.
8. Improve testing, configuration, reliability, and security incrementally.

Continue developing in manageable batches. Preserve the working RAG foundation, understand why each change is needed, test meaningful changes, and document each milestone.
