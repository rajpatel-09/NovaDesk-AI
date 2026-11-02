# NovaDesk-AI — Learning Log

This file tracks the practical implementation work, concepts explored, experiments performed, tests completed, and remaining learning objectives for NovaDesk-AI.

**Last updated:** November 2, 2026
**Current phase:** Phase 3 — Agentic AI
**Internship completion target:** November 18, 2026
**Current priority:** Improve Agentic AI evaluation, finish essential Agentic AI learning, then learn LangGraph and MCP.

---

## Phase 1 — Retrieval-Augmented Generation (RAG)

**Status: Core implementation complete**

### 1. Work Completed

- Created a synthetic company knowledge base containing HR, IT, and security documents.
- Implemented document loading using Python.
- Implemented document splitting and chunking.
- Generated embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
- Stored document embeddings in ChromaDB.
- Implemented semantic retrieval of relevant document chunks.
- Configured retrieval to return the top three chunks.
- Experimented with relevance-score thresholds to filter irrelevant results.
- Integrated document retrieval with the LLM to generate answers.
- Added source document information to generated answers.
- Implemented a fallback response when relevant information cannot be found.

### 2. Company Knowledge Base

The current knowledge base contains four synthetic company documents:

1. HR leave policy.
2. IT VPN troubleshooting.
3. IT software installation policy.
4. Security password policy.

The latest verified knowledge base contains 11 document chunks.

### 3. Concepts Explored

- What RAG is and why it is useful for company-specific questions.
- The difference between document retrieval and answer generation.
- How embeddings represent text as numerical vectors.
- How semantic similarity helps retrieve relevant documents.
- How the number of retrieved chunks affects the information provided to the LLM.
- Why irrelevant chunks can reduce answer quality.
- Why a relevance threshold is useful.
- Why a fallback response is needed when the knowledge base does not contain relevant information.

### 4. Practical Verification

Tested company-policy questions, VPN troubleshooting questions, and unsupported questions.

Verified that the RAG pipeline can retrieve relevant information and return source document details.

**Outcome:** The core RAG pipeline is implemented and integrated into NovaDesk-AI.

---

## Phase 2 — FastAPI

**Status: Core implementation and API tests complete**

### 1. Work Completed

- Created the FastAPI application.
- Implemented `GET /health`.
- Implemented `POST /ask`.
- Added Pydantic request validation.
- Added basic logging and error handling.
- Exposed interactive API documentation through Swagger UI.
- Integrated the `/ask` endpoint with `ask_agent()`.

### 2. Concepts Explored

- What an API is and why applications need one.
- How HTTP requests reach API endpoints.
- How FastAPI handles incoming requests.
- How Pydantic validates request data.
- How the API communicates with the AI agent.
- How Swagger UI helps manually test API endpoints.
- Why invalid requests and unexpected errors need proper handling.

### 3. Practical Verification

Manually tested the API through Swagger UI.

Verified:

- Health endpoint functionality.
- Casual leave questions.
- Vague questions requiring clarification.
- Unsupported company-policy questions.
- Request validation and error handling.

The API test suite contains five tests.

**Outcome:** The core FastAPI implementation and its automated tests are complete.

---

## Phase 3 — Agentic AI

**Status: Initial implementation complete; learning, evaluation, and improvements ongoing**

### 1. Created the Document-Search Tool

**File:** `src/agent/tools.py`

Implemented the `search_company_docs` tool using LangChain's `@tool` decorator.

The tool connects the agent to the existing RAG pipeline instead of duplicating document retrieval and answer-generation logic.

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
         Answer and sources
```

### 2. Created the AI Agent

**File:** `src/agent/agent.py`

Implemented an agent using LangChain's `create_agent`.

The configuration includes:

- The LLM provided by `AnswerGenerator`.
- The `search_company_docs` tool.
- A system prompt defining the assistant's role and behavior.
- `@lru_cache(maxsize=1)` to reuse the configured agent.
- `ask_agent(question)` to invoke the agent and return the final message content.

### 3. Defined the Agent's Behavior

The system prompt instructs the assistant to:

- Act as NovaDesk, an IT helpdesk assistant.
- Use company-document search for relevant policy and procedure questions.
- Ask concise clarifying questions when a request is too vague.
- Base company-specific answers on available tool results.
- Avoid inventing information when company documentation does not support an answer.

### 4. Examined Tool-Calling Behavior

Manually investigated the messages returned by the real agent when answering questions.

Observed the following message sequence:

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

Also tested a vague question and observed that the agent asked for clarification without calling the search tool.

Directly invoked `search_company_docs.invoke(...)` to inspect the tool's behavior.

### 5. Concepts Explored

- Difference between an ordinary LLM call and an agent workflow.
- Roles of the LLM, agent, and tool.
- What `create_agent()` configures.
- How `@tool` exposes a Python function to an agent.
- Why tools must be registered with the agent.
- Purpose of a system prompt.
- How `invoke()` passes input to an agent.
- Roles of `HumanMessage`, `AIMessage`, and `ToolMessage`.
- How LangChain executes tool calls and returns results to the model.
- Why `@lru_cache(maxsize=1)` avoids repeatedly creating the same configured agent.
- How `ask_agent()` extracts the final response instead of returning the full message history.

**Outcome:** The initial agent implementation is complete. Practical understanding and further evaluation are ongoing.

---

## Agent Testing — `tests/test_agent.py`

**Status: Three unit tests implemented, executed, and understood**

Created `tests/test_agent.py` to verify the important responsibilities of the Agentic AI implementation.

### Test 1 — Document-Search Tool

`test_search_company_docs_uses_rag_pipeline()`

Purpose:

- Checks whether the search tool correctly connects with the RAG pipeline.
- Checks whether the expected question is passed to the pipeline.
- Checks whether the expected answer is returned.

Uses:

- `FakeRAGPipeline`.
- `monkeypatch`.
- `.invoke()`.
- `assert`.

### Test 2 — Final-Answer Extraction

`test_ask_agent_returns_final_answer()`

Purpose:

- Checks whether `ask_agent()` passes the expected input to the agent.
- Checks whether the final answer content is correctly extracted and returned.

Uses:

- `SimpleNamespace`.
- Fake agent.
- Fake `invoke()` function.
- `monkeypatch`.
- Assertions.

### Test 3 — Agent Configuration and Caching

`test_get_agent_reuses_configured_agent()`

Purpose:

- Checks whether the correct LLM is supplied.
- Checks whether the document-search tool is registered.
- Checks important system-prompt instructions.
- Verifies that caching prevents unnecessary agent recreation.

Uses:

- Fake LLM.
- Fake agent.
- Fake `create_agent()` function.
- `**kwargs`.
- `create_calls`.
- `try...finally`.
- `@lru_cache`.
- `.cache_clear()`.
- Object identity using `is`.

### Testing Concepts Learned

- Software testing.
- Unit testing.
- Pytest test discovery.
- Pytest fixtures.
- `monkeypatch`.
- Fake classes and objects.
- `SimpleNamespace`.
- `assert`.
- `lambda`.
- `self`.
- `return`.
- `**kwargs`.
- `try...finally`.
- Cache clearing.
- Object identity.

### Learning Milestone

Completed a detailed walkthrough of all three tests.

Understood:

1. Why the test file was created.
2. What each test function verifies.
3. Why real dependencies are temporarily replaced with fake objects.
4. How `monkeypatch` works.
5. How assertions check expected behavior.
6. How the third test checks agent configuration and caching.
7. How pytest discovers and executes test functions.

Also prepared a mentor-ready explanation of the testing strategy.

**Important distinction:** Passing these tests verifies the relevant Python behavior with controlled fake dependencies. It does not guarantee that the live LLM will always choose the correct tool or follow all system-prompt instructions.

---

## Real-Agent Evaluation Experiments

**Status: Three initial scenarios manually verified**

After learning the unit tests, performed three practical experiments using the actual Groq-powered agent.

### Experiment 1 — Company-Policy Question

Question:

"How many casual leave days do employees get?"

Observed behavior:

- The real LLM received the question.
- It selected `search_company_docs`.
- The tool executed the RAG pipeline.
- The HR leave policy was retrieved.
- The agent generated its final answer.

Answer:

Employees are entitled to 12 days of casual leave per calendar year.

**Result:** Expected behavior observed.

### Experiment 2 — Vague Question

Question:

"It does not work. Help me."

Observed behavior:

- The agent received the question.
- It did not call the search tool.
- It asked the employee to explain the specific issue.

**Result:** Expected behavior observed.

### Experiment 3 — Unsupported Policy Question

Question:

"Does NovaTech Solutions reimburse employees for FIFA World Cup tickets?"

Observed behavior:

- The agent selected `search_company_docs`.
- RAG could not find relevant information.
- The tool returned the fallback response.
- The agent did not invent a reimbursement policy.

Fallback response:

```text
I could not find relevant information in the company documents.
```

**Result:** Expected behavior observed.

### Important Learning

Understood the difference between:

- Unit testing with fake dependencies.
- Manual real-agent evaluation using the actual LLM and tools.

Three successful manual experiments demonstrate the behavior of those particular runs, not overall agent reliability.

---

## Agent Evaluation System

**Status: Initial evaluation system implemented and expanded to four scenarios**

### 1. Created the Evaluation Dataset

**File:** `evaluation/agent_eval_cases.json`

Initially created three evaluation scenarios.

Later expanded the dataset to four scenarios:

1. Company leave-policy question.
2. Vague employee question.
3. Unsupported FIFA reimbursement question.
4. Software installation approval question.

Each evaluation case contains:

- `case_id`: Unique scenario identifier.
- `question`: Employee question.
- `expected_tool`: Expected tool selection or `null`.
- `expected_behavior`: Description of the expected behavior.
- `expected_source`: Expected source document where applicable.
- `expected_answer_contains_any`: Multiple acceptable phrases for checking the final answer.

### 2. Created the Evaluation Script

**File:** `scripts/evaluate_agent.py`

The script performs the following operations:

1. Loads evaluation cases from JSON.
2. Gets the configured agent.
3. Sends each question to the actual agent.
4. Inspects the returned messages.
5. Collects the selected tool calls.
6. Checks expected tool selection.
7. Checks the expected source document when specified.
8. Extracts the final answer.
9. Checks whether at least one acceptable phrase appears in the final answer.
10. Records the matched phrase.
11. Prints individual results and an overall evaluation summary.

### 3. Python Concepts Practised

- `json.load()` for reading JSON data.
- `pathlib.Path` for working with file paths.
- `__file__` for locating the current Python script.
- `getattr()` for safely accessing object attributes.
- List iteration.
- Dictionary access.
- Conditional expressions.
- Boolean results.
- List comprehensions and generators.
- `next()` for retrieving the first matching phrase.
- `casefold()` for case-insensitive text comparisons.
- Counting passing evaluation cases.
- Calculating evaluation success percentages.

### 4. Improved Answer Matching

During the initial evaluation, the vague-question case failed because the script expected the phrase "Can you tell me", while the agent responded with "Could you let me know".

The agent's behavior was appropriate, but strict keyword matching produced a false failure.

Updated the evaluation format to support multiple acceptable phrases through:

`expected_answer_contains_any`

The script now finds the first matching phrase and displays it in the report.

This is more flexible than checking a single exact phrase.

However, it remains keyword-based evaluation rather than semantic evaluation.

---

## ChromaDB Relevance-Score Investigation and Cosine Migration

**Status: New cosine collection implemented and manually verified**

### 1. Original Problem

The original ChromaDB collection was:

`novadesk_docs`

Its distance metric was:

`l2`

During software-policy evaluation, the following warning appeared:

```text
UserWarning: Relevance scores must be between 0 and 1
```

One retrieved document returned a negative relevance score:

```text
-0.09705684145467686
```

### 2. Investigation

Inspected the actual installed ChromaDB and LangChain implementations.

Verified:

- ChromaDB version: `1.5.9`.
- LangChain Chroma version: `1.1.0`.
- Original collection distance metric: `l2`.
- The original collection used squared Euclidean distance.
- LangChain selected its default Euclidean relevance-score conversion.

The conversion inspected was:

```python
return 1.0 - distance / math.sqrt(2)
```

The conversion assumes ordinary Euclidean distances from normalized embeddings. The original distance configuration could produce relevance scores outside the expected range.

### 3. Created a New Cosine Collection

Created a separate collection:

`novadesk_docs_cosine`

Updated:

**File:** `src/ingestion/vectorstore.py`

The new collection configuration uses:

```python
collection_configuration={
    "hnsw": {"space": "cosine"}
}
```

The vector-store creation code now stores the company's document chunks in the cosine collection.

The original L2 collection has been preserved as a backup.

### 4. Implemented Custom Cosine Relevance Scoring

**File:** `src/ingestion/retriever.py`

Added:

```python
def cosine_relevance_score(distance: float) -> float:
    """Convert cosine distance into a score between 0 and 1."""

    return max(0.0, min(1.0, 1.0 - distance))
```

The retriever now connects to:

`novadesk_docs_cosine`

It uses the custom cosine relevance-score conversion and retains the existing threshold:

`0.25`

### 5. Rebuilt and Verified the Collection

Created the new cosine collection and stored 11 document chunks.

Verified its configuration:

```text
Collection: novadesk_docs_cosine

Configuration:
space = cosine

Document count: 11
```

### 6. Direct Retrieval Experiments

Tested three questions against the new cosine collection.

| Question | Best relevance score | Chunks passing threshold |
|---|---:|---:|
| Casual leave policy | 0.591 | 3 |
| Software installation policy | 0.651 | 2 |
| FIFA reimbursement | 0.074 | 0 |

The unrelated security document in the software-policy search received a score of `0.177` and was filtered out by the `0.25` threshold.

The unsupported FIFA question returned zero chunks above the threshold.

No negative relevance-score warning was observed in the latest cosine retrieval and agent-evaluation runs.

### Important Learning

- A vector database uses distance metrics to compare embeddings.
- L2 and cosine distance are different measures.
- Relevance-score conversion must be compatible with the selected distance metric.
- A relevance score is not a percentage of answer correctness.
- A threshold filters retrieved results based on the configured scoring method.
- Existing ChromaDB collections cannot simply have their distance metric changed in place; a separate collection was created.
- Preserving the old collection provides a backup during migration.

The custom conversion and threshold still require broader validation against additional questions.

---

## Latest Agent Evaluation Results

The latest evaluation dataset contains four scenarios.

| Scenario | Expected behavior | Result |
|---|---|---|
| Company leave policy | Search HR document and return 12 days | Passed |
| Vague question | Ask for clarification without tool use | Passed |
| Unsupported FIFA policy | Search and return fallback response | Passed |
| Software installation | Retrieve IT approval policy | Passed |

Latest recorded evaluation output:

```text
Total cases: 4
Passed: 4
Failed: 0
Success rate: 100.0%
```

This result confirms that all four configured scenarios passed in the latest recorded run.

It does not guarantee that the agent will always behave correctly for every possible question or future LLM response.

---

## Automated Test Results

The complete pytest suite contains:

| Test file | Number of tests |
|---|---:|
| `tests/test_api.py` | 5 |
| `tests/test_agent.py` | 3 |
| **Total** | **8** |

The latest recorded full test run after the cosine migration was:

```text
8 passed in 2.96s
```

### Run the complete test suite

```powershell
uv run python -m pytest -v
```

### Run only the API tests

```powershell
uv run python -m pytest tests/test_api.py -v
```

### Run only the agent tests

```powershell
uv run python -m pytest tests/test_agent.py -v
```

### Run the real-agent evaluation

```powershell
uv run python -m scripts.evaluate_agent
```

The unit-test suite and evaluation script serve different purposes:

- Unit tests use controlled fake dependencies to verify individual code components.
- Agent evaluation uses the actual LLM-powered agent to inspect tool selection, retrieval results, and final responses.

Both should be run after meaningful code changes.

---

## Development Environment Notes

The project uses Python 3.12 and uv.

The working environment is configured outside the project directory because of earlier Windows environment and package-linking issues.

In each new VS Code PowerShell terminal, set:

```powershell
$env:UV_PROJECT_ENVIRONMENT = "$env:LOCALAPPDATA\uv-envs\novadesk-ai"
```

Run project commands through `uv run`.

Start the API:

```powershell
uv run uvicorn src.api.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

A Hugging Face unauthenticated-request warning may appear when loading the embedding model. The embedding model has loaded successfully in the latest recorded runs. This warning is separate from the previous ChromaDB relevance-score issue.

---

## Current Git and GitHub Status

**Repository:**

https://github.com/rajpatel-09/NovaDesk-AI.git

**Branch:** `main`

### Latest previously pushed commit

```text
b37230d

feat: add automated agent evaluation system
```

The following work has been completed after that commit:

- Expanded the evaluation dataset from three to four scenarios.
- Added multiple acceptable answer phrases.
- Added matched-phrase reporting.
- Created the new cosine collection.
- Updated vector-store and retriever configurations.
- Implemented custom cosine relevance-score conversion.
- Rebuilt and manually verified the 11-chunk cosine collection.
- Verified four real-agent evaluation scenarios.
- Verified that all eight unit tests still pass.

The above changes have not yet been confirmed as committed or pushed.

Before the next commit:

1. Check the actual Git state using `git status --short`.
2. Review changed files.
3. Run all eight unit tests.
4. Run all four evaluation scenarios.
5. Run `git diff --check`.
6. Review staged changes.
7. Commit and push the intended milestone.

Do not assume the working tree is clean or discard user changes without inspecting them.

The original L2 collection must remain preserved until the cosine migration is fully validated.

---

## Current Learning Status

The user has completed:

- Core RAG implementation.
- Core FastAPI implementation.
- Initial Agentic AI implementation.
- Detailed walkthrough of all three agent unit tests.
- Practical real-agent experiments.
- Initial automated agent evaluation.
- Four-scenario evaluation.
- Investigation of negative ChromaDB relevance scores.
- Creation and initial verification of a cosine-based ChromaDB collection.

### Important Learning Approach

The user is a beginner in Agentic AI and wants practical, industry-oriented mentoring.

The internship completion target is November 18, 2026, so the learning and implementation process must be accelerated.

When continuing:

- Explain why a concept or change is needed before showing the code.
- Connect new concepts to existing NovaDesk-AI files.
- Use practical examples from the project.
- Explain Python and framework features in beginner-friendly language.
- Combine two or three related concepts when appropriate.
- Avoid unnecessary theory and repeated confirmation questions.
- Clearly identify where commands must be executed.
- Help the user understand enough to explain the implementation to an internship mentor.
- Do not assume concepts are mastered merely because the tests pass.
- After meaningful milestones, remind the user to update all three documentation files.

### Upcoming Work

1. Complete documentation updates for the cosine migration and evaluation improvements.
2. Review and push the pending Git changes.
3. Expand evaluation scenarios and improve answer-quality evaluation beyond basic keyword matching.
4. Continue essential Agentic AI learning and implementation.
5. Learn and integrate LangGraph.
6. Learn and integrate MCP.
7. Complete production improvements, testing, documentation, and project presentation.

**Priority:** Complete the essential project milestones before November 18, 2026, without sacrificing the user's understanding of the implementation.

---

**End of Learning Log.**