# NovaDesk-AI — Project Context

**Last updated:** November 2, 2026
**Project:** NovaDesk-AI — AI IT Helpdesk Copilot
**Repository:** https://github.com/rajpatel-09/NovaDesk-AI.git
**Current branch:** `main`
**Current learning phase:** Phase 3 — Agentic AI
**Internship completion target:** November 18, 2026

---

## 1. Project Overview

NovaDesk-AI is an AI-powered IT helpdesk assistant that answers employee questions using internal company documentation.

The project combines:

- Retrieval-Augmented Generation (RAG).
- Agentic AI with tool calling.
- FastAPI backend.
- ChromaDB vector storage.
- Automated unit testing.
- Real-agent evaluation.

The objective is to build a practical AI helpdesk application while developing industry-oriented skills in AI application development.

### Planned Learning Sequence

1. Retrieval-Augmented Generation (RAG).
2. FastAPI.
3. Agentic AI.
4. LangGraph.
5. Model Context Protocol (MCP).
6. Production improvements and project finishing.

**Important:** Phase 1 and the core Phase 2 implementation are complete. Phase 3 implementation is ongoing. The user is still developing a deeper understanding of Agentic AI concepts and implementation. Do not treat Phase 3 as mastered or completed.

## 2. Development Environment

**Project directory:**

```text
C:\Users\Lenovo\OneDrive\Desktop\NovaDesk-AI
```

**Environment details:**

- Python: 3.12.10
- Package manager: uv
- Git branch: `main`
- Operating system: Windows
- LLM provider: Groq

The project uses an external uv environment because of earlier Windows and package-linking issues.

### Configure the environment

At the beginning of each new VS Code PowerShell terminal, run:

```powershell
$env:UV_PROJECT_ENVIRONMENT = "$env:LOCALAPPDATA\uv-envs\novadesk-ai"
```

Use `uv run` to execute project commands through the configured environment.

### Run the full test suite

```powershell
uv run python -m pytest -v
```

Use `python -m pytest` rather than plain `pytest` to handle the project's module import path correctly in the current setup.

### Start the FastAPI application

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
| Programming language | Python 3.12 |
| Dependency management | uv |
| LLM provider | Groq |
| LLM integration | LangChain |
| Agent framework | LangChain `create_agent` |
| LLM model | `openai/gpt-oss-20b` |
| Embeddings | Sentence Transformers |
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector database | ChromaDB |
| Retrieval metric | Cosine distance |
| API framework | FastAPI |
| Validation | Pydantic |
| Automated testing | pytest |
| Evaluation dataset | JSON |

Installed versions verified in the configured environment:

- ChromaDB: `1.5.9`
- LangChain Chroma: `1.1.0`

The `.env` file contains the Groq API key. Never commit this file or expose API credentials.

## 4. Current Application Architecture

The main application flow is:

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
LangChain AI Agent
       |
       v
search_company_docs tool
       |
       v
RAG Pipeline
       |
       v
CompanyRetriever
       |
       v
ChromaDB cosine collection
       |
       v
Relevant document chunks
       |
       v
AnswerGenerator
       |
       v
Tool result with sources
       |
       v
AI Agent generates final answer
       |
       v
FastAPI response
```

The agent can also ask a clarifying question when an employee's request is vague and a company-document search is unnecessary.

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
│   │
│   └── vector_store/
│
├── evaluation/
│   └── agent_eval_cases.json
│
├── scripts/
│   └── evaluate_agent.py
│
├── src/
│   ├── agent/
│   │   ├── agent.py
│   │   └── tools.py
│   │
│   ├── api/
│   │   └── main.py
│   │
│   ├── ingestion/
│   │   ├── embeddings.py
│   │   ├── loader.py
│   │   ├── pipeline.py
│   │   ├── retriever.py
│   │   └── vectorstore.py
│   │
│   └── rag/
│       ├── generator.py
│       ├── pipeline.py
│       └── retriever.py
│
├── tests/
│   ├── test_api.py
│   └── test_agent.py
│
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
├── PROJECT_CONTEXT.md
└── LEARNING_LOG.md
```

The project structure may evolve as additional features are implemented.

## 6. Phase 1 — Retrieval-Augmented Generation (RAG)

**Status: Core implementation complete**

The RAG implementation includes:

- Loading company `.txt` documents.
- Splitting documents into chunks.
- Generating embeddings using Sentence Transformers.
- Storing document embeddings in ChromaDB.
- Retrieving the top three relevant chunks.
- Applying a relevance-score threshold.
- Generating answers using retrieved context.
- Returning source document information.
- Using a fallback response when relevant information cannot be found.

### Knowledge Base

The current knowledge base contains four synthetic company documents:

1. HR leave policy.
2. IT VPN troubleshooting.
3. IT software installation policy.
4. Security password policy.

The latest verified knowledge base contains 11 document chunks.

### RAG Architecture

**Embedding creation:**

File: `src/ingestion/embeddings.py`

Uses:

`sentence-transformers/all-MiniLM-L6-v2`

**Document loading:**

File: `src/ingestion/loader.py`

Loads company documents from the knowledge-base directory.

**Document ingestion:**

File: `src/ingestion/pipeline.py`

Coordinates document loading, chunking, embedding creation, and vector-store creation.

**Vector storage:**

File: `src/ingestion/vectorstore.py`

Creates the ChromaDB collection and stores document chunks.

**Document retrieval:**

File: `src/ingestion/retriever.py`

Connects to the persisted ChromaDB collection and configures the retriever.

**RAG pipeline:**

File: `src/rag/pipeline.py`

Combines retrieval and answer generation.

**Fallback response:**

```text
I could not find relevant information in the company documents.
```

## 7. ChromaDB Relevance-Score Investigation and Cosine Migration

**Status: New cosine collection implemented and manually verified**

### Original problem

The original ChromaDB collection was:

`novadesk_docs`

Its distance metric was:

`l2`

During real-agent evaluation, LangChain displayed a warning:

```text
UserWarning: Relevance scores must be between 0 and 1
```

One retrieved document produced a negative relevance score:

```text
-0.09705684145467686
```

### Investigation

Inspected the installed ChromaDB and LangChain implementations.

The original collection used L2 distance, while LangChain selected its default Euclidean relevance-score conversion.

The default conversion was:

```python
return 1.0 - distance / math.sqrt(2)
```

This conversion assumes Euclidean distances from normalized embeddings. ChromaDB's L2 configuration uses squared Euclidean distance, which can produce scores outside the expected range.

### Solution

Created a separate cosine-based collection:

`novadesk_docs_cosine`

Updated:

**File:** `src/ingestion/vectorstore.py`

The vector-store initialization now specifies:

```python
vectorstore = Chroma(
    persist_directory="data/vector_store",
    collection_name="novadesk_docs_cosine",
    embedding_function=embeddings,
    collection_configuration={
        "hnsw": {"space": "cosine"}
    },
)
```

**File:** `src/ingestion/retriever.py`

The retriever now connects to the cosine collection and uses a custom relevance-score conversion:

```python
def cosine_relevance_score(distance: float) -> float:
    """Convert cosine distance into a score between 0 and 1."""

    return max(0.0, min(1.0, 1.0 - distance))
```

The retriever uses:

```python
return vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.25},
)
```

### Current collection configuration

| Setting | Value |
|---|---|
| Original collection | `novadesk_docs` |
| Original metric | L2 |
| New collection | `novadesk_docs_cosine` |
| New metric | Cosine |
| Persist directory | `data/vector_store` |
| Document chunks in new collection | 11 |
| Relevance threshold | 0.25 |
| Number of retrieved chunks | Top 3 |

The original L2 collection has been preserved as a backup.

### Direct retrieval verification

The following results were observed when querying the new cosine collection:

| Question | Best relevance score | Chunks passing threshold |
|---|---:|---:|
| Casual leave policy | 0.591 | 3 |
| Software installation policy | 0.651 | 2 |
| FIFA reimbursement | 0.074 | 0 |

The software question also retrieved an unrelated security chunk with a score of `0.177`, which was filtered out by the `0.25` threshold.

The unsupported FIFA question returned zero chunks above the threshold.

No negative relevance-score warning was observed in the latest cosine retrieval and agent-evaluation runs.

**Important:** Relevance scores are similarity indicators, not percentages of answer correctness. The custom conversion and threshold still need broader validation with additional queries.

## 8. Phase 2 — FastAPI

**Status: Core implementation and API tests complete**

The FastAPI backend includes:

- `GET /health` for checking API availability.
- `POST /ask` for employee questions.
- Pydantic request validation.
- Basic logging and error handling.
- Integration with `ask_agent()`.
- Interactive Swagger UI testing.
- Automated API tests.

The `/ask` endpoint calls the agent instead of directly calling the RAG pipeline.

### Manual API verification

Using Swagger UI, the following scenarios were tested:

- Casual leave question returned the documented 12-day allowance.
- A vague question prompted the assistant to ask for clarification.
- An unsupported FIFA-related question did not result in an invented reimbursement policy.

These are manual checks, not a guarantee of correct behavior for every possible question.

## 9. Phase 3 — Agentic AI

**Status: Initial implementation complete; learning and improvement ongoing**

### `src/agent/tools.py`

Contains the `search_company_docs` tool.

The tool:

- Uses LangChain's `@tool` decorator.
- Makes the Python function available to the agent.
- Passes the question to the existing RAG pipeline.
- Returns the RAG result to the agent.

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
RAG answer and sources
```

### `src/agent/agent.py`

Contains the agent implementation.

It uses:

- LangChain's `create_agent`.
- `AnswerGenerator().llm` as the model.
- `search_company_docs` as an available tool.
- A system prompt defining the assistant's behavior.
- `@lru_cache(maxsize=1)` to reuse the configured agent.
- `ask_agent(question)` to invoke the agent and extract the final message content.

The system prompt instructs NovaDesk to:

- Act as an IT helpdesk assistant.
- Use company-document search for policy and procedure questions.
- Ask concise clarifying questions for vague requests.
- Use facts supported by the tool results.
- Avoid inventing company information when relevant documentation is unavailable.

### Concepts explored

The following behaviors have been manually examined:

1. A VPN question caused the agent to request `search_company_docs`.
2. The search tool returned the RAG result.
3. The agent generated a final answer.
4. A vague question resulted in clarification without a tool call.
5. A direct `search_company_docs.invoke(...)` call returned the RAG result.

The observed tool-calling message sequence was:

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

The agent has been manually tested with actual Groq calls, not only mocked unit tests.

## 10. Agent Unit Tests

**Test file:** `tests/test_agent.py`

Three unit tests are implemented.

### Test 1 — `test_search_company_docs_uses_rag_pipeline`

Verifies that:

- The search tool passes the correct question to the RAG pipeline.
- The expected answer is returned.

Uses a fake RAG pipeline and monkeypatching to isolate the search tool.

### Test 2 — `test_ask_agent_returns_final_answer`

Verifies that:

- `ask_agent()` passes the expected input to the configured agent.
- The final answer content is extracted and returned.

Uses a fake agent and a simulated `invoke()` response.

### Test 3 — `test_get_agent_reuses_configured_agent`

Verifies that:

- The correct LLM is supplied.
- The company-document search tool is included.
- Important system-prompt instructions are present.
- The configured agent is created only once and reused.

Uses fake dependencies, `**kwargs`, `create_calls`, and cache clearing.

### Testing concepts learned

- Software testing and unit testing.
- Pytest test discovery and fixtures.
- `monkeypatch`.
- Fake objects and fake dependencies.
- `SimpleNamespace`.
- `assert`.
- `lambda`.
- `try...finally`.
- `@lru_cache`.
- `.cache_clear()`.
- Object identity using `is`.

The user has completed a detailed walkthrough of the file and can explain the purpose of its three tests.

The user has also added explanatory comments to the test file as personal learning notes.

**Limitation:** Passing mocked unit tests does not prove that a real LLM will always choose the correct tool or follow every system-prompt instruction.

## 11. Agent Evaluation System

**Status: Initial evaluation system implemented; four scenarios passing**

Created an evaluation dataset and Python script to test the actual LLM-powered agent.

### Evaluation files

```text
evaluation/
└── agent_eval_cases.json

scripts/
└── evaluate_agent.py
```

### Evaluation dataset

File:

`evaluation/agent_eval_cases.json`

The dataset currently contains four scenarios:

1. Company leave-policy question.
2. Vague employee question.
3. Unsupported FIFA reimbursement question.
4. Software installation approval question.

Each evaluation case contains:

- `case_id`: Unique scenario identifier.
- `question`: Employee question.
- `expected_tool`: Expected tool selection, or `null` when no tool should be called.
- `expected_behavior`: Description of the intended behavior.
- `expected_source`: Expected source document, when applicable.
- `expected_answer_contains_any`: Multiple acceptable answer phrases.

### Evaluation script

File:

`scripts/evaluate_agent.py`

The script:

1. Loads evaluation cases from JSON.
2. Gets the configured agent.
3. Sends each question to the actual agent.
4. Collects tool calls.
5. Checks whether the expected tool was selected.
6. Inspects tool results for expected source documents.
7. Extracts the final answer.
8. Checks whether at least one acceptable phrase appears in the answer.
9. Prints individual scenario results.
10. Produces an overall evaluation summary.

### Run agent evaluation

```powershell
uv run python -m scripts.evaluate_agent
```

### Latest recorded evaluation result

```text
Total cases: 4
Passed: 4
Failed: 0
Success rate: 100.0%
```

All four scenarios passed after switching the retrieval system to the cosine collection.

### Important evaluation limitation

The script uses exact substring matching with multiple acceptable phrases.

It is more flexible than checking only one exact phrase, but it does not understand semantic meaning.

For example, a correct answer with different wording may still fail if none of the configured phrases appears.

The evaluation system is an initial repeatable evaluation framework, not a complete AI quality or safety evaluation system.

Four passing scenarios do not establish overall agent reliability.

## 12. Latest Automated Test Status

The latest recorded complete pytest run after the cosine migration was:

```text
8 passed in 2.96s
```

Breakdown:

| Test file | Tests |
|---|---:|
| `tests/test_api.py` | 5 |
| `tests/test_agent.py` | 3 |
| **Total** | **8** |

Run the complete suite:

```powershell
uv run python -m pytest -v
```

Run only the agent tests:

```powershell
uv run python -m pytest tests/test_agent.py -v
```

Run only the API tests:

```powershell
uv run python -m pytest tests/test_api.py -v
```

The complete suite must be rerun after further changes.

## 13. Git and GitHub Status

**Repository:**

https://github.com/rajpatel-09/NovaDesk-AI.git

**Branch:** `main`

### Latest previously pushed commit

```text
b37230d
feat: add automated agent evaluation system
```

This commit includes:

- Updated README and project documentation.
- Initial evaluation dataset.
- Evaluation script.
- Agent-test learning comments.

### Changes made after that commit

The following implementation improvements were made after the latest pushed commit:

- Expanded the evaluation dataset from three to four scenarios.
- Added multiple acceptable answer phrases.
- Updated answer-match reporting in `scripts/evaluate_agent.py`.
- Created `novadesk_docs_cosine`.
- Updated `src/ingestion/vectorstore.py`.
- Updated `src/ingestion/retriever.py`.
- Added custom cosine relevance-score conversion.
- Rebuilt and manually verified the 11-chunk cosine collection.
- Evaluated all four real-agent scenarios successfully.
- Updated documentation is currently being prepared.

**Important:** These changes have not yet been confirmed as committed or pushed. Verify the actual working-tree state before staging or committing.

Check using:

```powershell
git status --short
```

Never assume the working tree is clean or that the listed files are the complete set of changes.

Before committing:

1. Save all documentation.
2. Run the full pytest suite.
3. Run the four-scenario agent evaluation.
4. Run `git diff --check`.
5. Review the changed files.
6. Stage only intended files.
7. Review the staged changes.
8. Commit and push to `main`.

The original L2 collection must be preserved until the cosine migration is fully verified and the backup is no longer needed.

## 14. Current Limitations and Pending Improvements

- The evaluation dataset currently contains only four scenarios.
- Answer evaluation uses keyword matching rather than semantic evaluation.
- The relevance threshold of `0.25` needs broader testing with more representative questions.
- Retrieval quality should be evaluated with more HR, IT, security, and unsupported questions.
- Real LLM output may vary across runs.
- The cosine conversion has been manually verified on current scenarios but needs broader validation.
- The original L2 collection remains as a backup.
- Hugging Face Hub may display an unauthenticated-request warning. The embedding model has loaded successfully in the latest recorded runs.
- Production-level security, monitoring, and reliability improvements are still pending.

## 15. Current Tasks — In Order

1. Finish replacing and saving `README.md`, `PROJECT_CONTEXT.md`, and `LEARNING_LOG.md` with consistent, up-to-date information.
2. Review the actual changes using `git status --short`.
3. Rerun the complete test suite.
4. Rerun all four agent evaluation cases.
5. Review and commit the cosine migration and evaluation improvements.
6. Continue essential Agentic AI learning and implementation.
7. Learn and integrate LangGraph.
8. Learn and integrate MCP.
9. Improve final testing, error handling, documentation, and project presentation.
10. Complete the internship project by November 18, 2026.

Do not move to LangGraph or MCP until the necessary Agentic AI concepts and current implementation have been sufficiently understood.

## 16. Learning and Mentoring Instructions

The user is a beginner in Agentic AI and is building NovaDesk-AI to gain practical, industry-oriented skills.

The remaining internship time is limited, with a target completion date of November 18, 2026.

When continuing this project:

- Explain why a concept or code change is needed before showing the implementation.
- Connect explanations directly to the actual NovaDesk-AI files.
- Use realistic examples from the project.
- Explain Python, LangChain, testing, and Git concepts in beginner-friendly language.
- Move efficiently and combine two or three related concepts when appropriate.
- Avoid lengthy theoretical explanations that are not needed for implementation.
- Prefer practical experiments and real project improvements.
- Clearly specify where commands should be run, especially VS Code PowerShell.
- Use a combined understanding checkpoint rather than repeated confirmation questions.
- Do not assume the user understands a concept simply because the code runs.
- Help the user prepare to explain important implementation decisions to their internship mentor.
- Remind the user to update `README.md`, `PROJECT_CONTEXT.md`, and `LEARNING_LOG.md` after meaningful milestones.

The user prefers free and open-source technologies and does not want paid subscriptions for the project.

### Next learning objective

Complete the cosine migration documentation, review and push the pending changes, then continue improving the real-agent evaluation system.

After the current Agentic AI work is sufficiently understood, prioritize LangGraph, MCP, and final project preparation before the November 18 deadline.

---

**End of Project Context.**