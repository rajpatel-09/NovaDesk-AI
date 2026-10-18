# NovaDesk AI — Learning Log

This file records my learning, implementation, debugging, and progress throughout the NovaDesk AI project.

## Day 1 — Project Foundation

### Objective

Set up a clean project for NovaDesk AI.

### What I learned

- Git is used to track changes in a project.
- GitHub is an online platform where Git repositories can be stored.
- A Python virtual environment keeps project dependencies separate.
- NovaDesk AI has its own `.venv`, separate from the old YTRAG project.
- Project-based learning means learning a concept and immediately applying it to the project.

### What I implemented

- Created the NovaDesk AI project and initial folder structure.
- Created `PROJECT_CONTEXT.md`, `LEARNING_LOG.md`, and `README.md`.
- Configured `.gitignore`.
- Initialized Git and created initial commits.
- Renamed the project folder from `AI-IT-Helpdesk-Copilot` to `NovaDesk-AI`.

### Problems / Errors

- The old YTRAG virtual environment was initially active.
- Deactivated the old environment and activated the NovaDesk AI environment.

### What I understood

- YTRAG remains my previous learning/tutorial project.
- NovaDesk-AI is my project for internship-oriented learning.
- Each project has its own Python environment.
- Git maintains project history.

---

## RAG Implementation — Core Knowledge Base

### Objective

Build a working Retrieval-Augmented Generation (RAG) system that answers employee questions using company documents.

### Technology used

- Python 3.12
- `uv` for dependency management
- LangChain
- Hugging Face Sentence Transformers
- `all-MiniLM-L6-v2` embeddings
- ChromaDB
- ChatGroq with `openai/gpt-oss-20b`

### What I implemented

- Document loading and splitting in `src/ingestion/`.
- Embedding creation and storage in ChromaDB.
- A company-document retriever in `src/rag/retriever.py`.
- Answer generation in `src/rag/generator.py`.
- An end-to-end pipeline in `src/rag/pipeline.py`.
- Source-document reporting in the final response.
- A fallback-style response when the retrieved context does not support an answer.

### Company documents

The initial knowledge base contained three documents:

- `HR/leave_policy.txt`
- `IT/vpn_troubleshooting.txt`
- `SECURITY/password_security_policy.txt`

A fourth document was subsequently added:

- `IT/software_installation_policy.txt`

The document loader discovers `.txt` files recursively under `data/company_docs/`.

The ChromaDB collection is named `novadesk_docs` and is persisted in `data/vector_store/`.

The ingestion pipeline initially created 9 chunks. After adding the software installation policy, it reported 11 chunks.

### What I learned

- RAG retrieves relevant document chunks and provides them to the LLM as context.
- Document embeddings are created during ingestion. A user's question is embedded when a search is performed.
- The LLM receives the retrieved context, not the entire vector database.
- Embeddings represent text numerically so that semantic similarity can be used for retrieval.
- Source deduplication is separate from embedding creation.
- Source paths help identify which company documents were used.

### RAG flow

Employee question → Embedding and similarity search → Retrieve relevant chunks → Generate an answer using the retrieved context → Return answer and source paths.

---

## Retrieval Experiments

### Objective

Understand how the number of retrieved chunks affects relevance and answer quality.

### What I tested

Compared `top_k=3` with `top_k=5` for the question:

"How many casual leave days do employees get?"

With `top_k=5`, the retrieved context included unrelated password-security information. The answer was still 12 days, but the security policy appeared among the reported sources.

With `top_k=3`, the answer remained 12 days, and the reported source was the relevant HR leave policy.

### What I learned

- `top_k` controls how many chunks are retrieved.
- A higher `top_k` can provide additional context but may introduce irrelevant information.
- More chunks do not automatically mean a better answer.
- Even the top-ranked chunks are not guaranteed to be relevant.
- A source filename alone does not prove that the generated answer is supported by that source.
- `top_k=3` worked well for this particular question, but it is not guaranteed to be optimal for every question.

### Important concept

Retrieval quality and answer quality are related, but they are not the same. Both should be evaluated when testing a RAG system.

---

## Adding a New Company Document

### Objective

Extend the existing knowledge base without unnecessarily duplicating previously ingested documents.

### What I implemented

- Added `data/company_docs/IT/software_installation_policy.txt`.
- Updated `create_vectorstore()` in `src/ingestion/vectorstore.py` to identify already stored source paths.
- Added chunks from source files that were not already present.
- Ran the ingestion pipeline and confirmed that the collection contained 11 chunks.
- Tested the new policy through the RAG pipeline.

### Test question

"Do employees need IT approval before installing software on company devices?"

### Observed result

The assistant correctly answered that employees must obtain IT department approval before installing software on company devices. The new software installation policy appeared in the reported sources.

The VPN troubleshooting document was also retrieved, showing that retrieval relevance can still be improved.

### Current limitation

The current ingestion logic handles newly added source files. It does not automatically update or replace chunks when an existing source file is modified.

---

## Debugging and Implementation Lessons

### Function-name mismatch

The ingestion pipeline imported `create_vectorstore`, while the vector-store file initially defined `create_vectors`.

I corrected the function name so that the import and function definition matched. I then confirmed that the import worked.

### Retriever error

An error occurred:

`AttributeError: 'Chroma' object has no attribute 'search_kwargs'`

The cause was that `create_retriever()` returned the Chroma vector store itself instead of a LangChain retriever.

I fixed the function to return:

`vectorstore.as_retriever()`

After the change, the RAG pipeline successfully retrieved the new software installation policy and generated an answer.

### What I learned

- Read the traceback to identify which file and line caused an error.
- Understand what a function returns before using its result.
- A vector store and a retriever are related but have different interfaces.
- Fix the underlying cause instead of changing unrelated code.
- Test a change after fixing it.

---

## Answer Grounding and Out-of-Scope Testing

### Objective

Check whether the assistant avoids unsupported answers when company documents do not contain the requested information.

### What I tested

Asked:

"Who won the FIFA World Cup in 2018?"

This question was outside the scope of the company knowledge base.

### Observed result

The assistant responded that it could not find the information in the company documents instead of providing the factual answer from its general knowledge. However, it still retrieved unrelated company documents.

### What I learned

- Company-specific answers should be supported by the retrieved company context.
- When information is insufficient, the assistant should say so instead of guessing.
- A retrieved result can be irrelevant even when it ranks among the top results.
- The absence of a relevant retrieved chunk does not necessarily mean the information is absent from the knowledge base.
- A more robust system needs better relevance checks and an explicit mechanism for handling insufficient evidence.

The current behavior is a useful initial result, but it does not guarantee safe handling of every out-of-scope question.

---

## Understanding the LLM Configuration

The answer generator uses ChatGroq with:

- Model: `openai/gpt-oss-20b`
- Temperature: `0`
- Reasoning format: `hidden`

### What I learned

- A lower temperature generally produces less variation in responses.
- A higher temperature generally allows more variation and creativity.
- Temperature `0` does not guarantee that the answer is factually correct.
- Correctness also depends on the retrieved context, prompt instructions, and model behavior.
- For a company helpdesk, consistency and evidence-based answers are more important than unnecessary creativity.

---

## Git and GitHub Workflow

### Objective

Track the project's implementation and publish the code to GitHub.

### What I learned

- `M` in `git status --short` means a tracked file has been modified.
- `??` means a file is untracked.
- `git add` stages selected changes for a commit.
- `git commit` saves a snapshot in local Git history.
- `git remote add origin` configures the remote repository.
- `git push -u origin main` uploads the branch and configures upstream tracking.
- A clean working tree means there are no uncommitted changes.

### What I implemented

- Reviewed `.gitignore` and verified that `.env` and `data/vector_store/` were ignored.
- Reviewed and staged the intended project files.
- Created a commit containing the RAG implementation and company documents.
- Created the GitHub repository and connected it to the local project.
- Pushed the `main` branch successfully.

### Repository

https://github.com/rajpatel-09/NovaDesk-AI

### Initial RAG implementation commit

`0f71f8d` — `feat: build core RAG pipeline and knowledge base`

The latest commit records the RAG implementation at the time of the initial GitHub push. Subsequent documentation updates must be committed and pushed separately.

### Security lesson

Never commit API keys or other secrets. Keep `.env` excluded through `.gitignore`.

---

## Current Project Status

### Phase 1 — RAG Core

**Status: Completed; initial implementation tested manually.**

Implemented:

- Document ingestion and chunking
- Embeddings and ChromaDB storage
- Configurable retrieval
- LLM answer generation
- Source reporting
- Initial out-of-scope testing

### Remaining improvement areas

- Reduce irrelevant retrieval results.
- Add a relevance or similarity threshold.
- Improve handling of insufficient evidence.
- Refresh chunks when existing company documents change.
- Expand automated testing and error handling.

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

### Objective

Start exposing NovaDesk AI functionality through an HTTP API, building on the existing RAG pipeline.

### What I implemented

- Added FastAPI using `uv add "fastapi[standard]"`.

- Verified the FastAPI installation.
- Created `src/api/main.py`.
- Created a `GET /health` endpoint.
- Returned a JSON response containing the API status and project name.
- Started the development server using `uv run fastapi dev src/api/main.py`.
- Verified the health endpoint in the browser.
- Opened FastAPI's interactive API documentation at `/docs`.

### What I learned

- FastAPI allows Python functions to be exposed through HTTP endpoints.
- `@app.get("/health")` registers a GET endpoint at `/health`.
- The endpoint returns data as a JSON response.
- FastAPI automatically generates interactive documentation at `/docs`.
- The development server must finish starting before the browser can connect.
- `pyproject.toml` and `uv.lock` manage project dependencies in this `uv`-based project; a manually maintained `requirements.txt` is not necessary.

### Problem encountered

Initially, the browser showed `ERR_CONNECTION_REFUSED`. The server was still starting. After the terminal confirmed that application startup was complete, the health endpoint worked.

### Current status

The health-check endpoint is working. The RAG pipeline has not yet been connected to FastAPI.

### Next step

Create an API endpoint that accepts an employee question and passes it to the existing `RAGPipeline`.

### Phase 3 — Agentic AI

**Status: Not started.**

### Phase 4 — LangGraph

**Status: Not started.**

### Phase 5 — MCP

**Status: Not started.**

### Phase 6 — Production Improvements

**Status: Not started.**

---

## Learning Approach and Next Steps

### What I still need to improve

- Writing code independently instead of only recognizing or understanding existing code.
- Becoming more confident with Git and GitHub.
- Improving retrieval evaluation and testing.
- Building APIs and later integrating agentic workflows.

I do not need to memorize every line of code immediately. My goal is to understand why the code exists, explain its logic, and gradually implement small parts independently.

### Immediate next steps

1. Update and verify the project documentation.
2. Commit and push the documentation updates to GitHub.
3. Begin Phase 2: FastAPI.
4. Integrate the existing `RAGPipeline` rather than rebuilding it.
5. Continue learning one step at a time, testing each change before moving forward.

---

## Phase 2 — FastAPI: Connecting the RAG Pipeline

### Objective

Expose the existing NovaDesk AI RAG pipeline through an HTTP API so other applications can submit employee questions.

### What I implemented

- Installed FastAPI using `uv add "fastapi[standard]"`.
- Verified FastAPI version 0.143.1.
- Created `src/api/main.py`.
- Implemented `GET /health` to check that the API responds.
- Implemented `POST /ask` to accept employee questions.
- Created a Pydantic `QuestionRequest` model for the incoming JSON request.
- Connected `POST /ask` to the existing `RAGPipeline`.
- Tested the endpoints using FastAPI's interactive documentation at `/docs`.
- Successfully submitted a company-policy question and received an HTTP 200 response containing the answer.

### What I learned

- FastAPI exposes Python functions through HTTP endpoints.
- GET is commonly used to retrieve information, while POST is commonly used to submit data for processing.
- Pydantic models define and validate the expected structure of incoming request data.
- `request.question` accesses the question provided in the JSON request body.
- Calling `rag_pipeline.ask(request.question)` reuses the existing RAG logic.
- FastAPI converts returned Python dictionaries into JSON responses.
- FastAPI automatically provides interactive documentation at `/docs`.

### Problem encountered and solution

The command `uv run fastapi dev src/api/main.py` failed with `ModuleNotFoundError: No module named 'src'` when importing the existing RAG pipeline.

Running the application from the project root with the following command worked:

`uv run uvicorn src.api.main:app --reload`

The server started successfully and loaded the RAG pipeline.

### Current status

Both `GET /health` and `POST /ask` are implemented and tested. FastAPI can call the existing RAG pipeline without rebuilding it.

### Next step

Review request validation and error handling, then test edge cases before extending the API further.

### FastAPI Validation — Empty Question Handling

#### What I implemented

- Added a Pydantic `field_validator` for the `question` field in `QuestionRequest`.
- Used `strip()` to remove leading and trailing whitespace.
- Rejected empty or whitespace-only questions with `ValueError`.
- Verified that invalid questions return HTTP `422 Unprocessable Entity`.
- Retested a valid question and confirmed the RAG pipeline still works.
- Tested a request with an empty JSON body (`{}`) and verified that FastAPI returns HTTP 422 when the required `question` field is missing.

#### Bug encountered

The validator initially used `raise value`, which caused a `TypeError` because Python cannot raise a regular string.

I fixed it by using:

`raise ValueError("Question must not be empty.")`

FastAPI and Pydantic then handled the invalid input as a validation error instead of an HTTP 500 server error.

#### What I learned

- Validate user input before passing it to the RAG pipeline.
- `strip()` removes whitespace from both ends of a string.
- Python's `raise` statement must raise an exception.
- HTTP 422 indicates that a request failed validation.
- Test both invalid and valid requests after changing validation logic.
- Pydantic automatically rejects requests that omit required model fields, even without a custom validator.

---

## FastAPI Error Handling — Unexpected RAG Failures

### Objective

Handle unexpected errors from the RAG pipeline without exposing technical exception details in the API response.

### What I implemented

- Added Python logging using `logging.getLogger(__name__)`.
- Wrapped the `rag_pipeline.ask()` call in a `try`/`except` block.
- Used `logger.exception()` to record technical error information and the traceback.
- Returned an HTTP 500 response with a generic error message when an unexpected exception occurs.
- Tested the error handler by temporarily raising an intentional `RuntimeError`.
- Verified that the API returned HTTP 500 with the generic error message.
- Removed the temporary test error and restored the real RAG pipeline call.
- Retested a valid company-policy question and confirmed it returned HTTP 200.

### What I learned

- Unexpected errors should be logged to help developers diagnose the underlying problem.
- API responses should avoid exposing internal exception details to callers.
- `logger.exception()` records the error and traceback when called inside an exception handler.
- `HTTPException` lets FastAPI return a controlled HTTP error response.
- Simulating a controlled failure is a useful way to test error-handling code.
- After testing a failure path, restore the real implementation and retest normal behavior.

### Current status

The basic error-handling path has been tested. Valid questions still reach the existing RAG pipeline, and unexpected exceptions are handled with a generic HTTP 500 response.

---

## Automated API Testing — First Test Suite

### Objective

Replace repeated manual checks with automated tests that verify the behavior of NovaDesk AI's FastAPI endpoints.

### Tools used

- `pytest` — runs the tests and reports their results.
- `httpx` — provides the underlying HTTP client used by FastAPI's `TestClient`.
- `fastapi.testclient.TestClient` — sends simulated requests to the application without manually starting the Uvicorn server.

### What I implemented

Created `tests/test_api.py` with three automated tests:

1. `test_health_check` — verifies that `GET /health` returns HTTP 200 and the expected JSON response.
2. `test_ask_rejects_blank_question` — verifies that a whitespace-only question returns HTTP 422.
3. `test_ask_rejects_missing_question` — verifies that a request without the required `question` field returns HTTP 422.
4. Added `test_ask_returns_answer`, using a mock to return a predictable answer without calling the real LLM.

### Test results

Command used:

`uv run python -m pytest tests/test_api.py -v`

Result: **4 tests passed.**

### What I learned

- Automated tests help check existing functionality after code changes.
- `TestClient` can send requests to the FastAPI application without manually starting Uvicorn.
- `assert` checks whether the actual result matches the expected result.
- Tests can check both HTTP status codes and JSON response content.
- Pydantic automatically rejects requests that omit required fields.
- Whitespace-only questions are rejected by our custom field validator.
- Running `pytest` directly initially caused `ModuleNotFoundError: No module named 'src'`. Running it as a Python module with `uv run python -m pytest` successfully resolved the import issue.

### Current limitations

The test suite covers the health endpoint, invalid questions, and a successful `/ask` response using a mock. Automated testing of unexpected-error handling is still pending.

### Next step

Expand the test suite to cover successful `/ask` responses and unexpected errors without making tests depend on live model calls or external services.
