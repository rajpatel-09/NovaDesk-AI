# NovaDesk-AI — AI IT Helpdesk Copilot

NovaDesk-AI is an AI-powered IT helpdesk assistant that answers employee questions using internal company documentation.

The project combines Retrieval-Augmented Generation (RAG), Agentic AI with tool calling, and a FastAPI backend.

The goal is to build a practical AI helpdesk application while learning how to develop, test, evaluate, and structure AI applications using industry-style practices.

## Project Goals

- Answer employee questions using internal company documents.
- Retrieve relevant information before generating an answer.
- Use an AI agent that can call tools to search company knowledge.
- Ask clarifying questions when a user's request is vague.
- Avoid inventing company policies when the required information is unavailable.
- Expose the assistant through a REST API using FastAPI.
- Build automated tests for API and agent components.
- Evaluate real-agent behavior using a repeatable evaluation system.

## Current Features

### 1. Retrieval-Augmented Generation (RAG)

- Loads company knowledge from text documents.
- Splits documents into smaller chunks.
- Generates embeddings using Sentence Transformers.
- Stores and retrieves document chunks using ChromaDB.
- Retrieves the top three relevant chunks.
- Applies a relevance-score threshold of `0.25`.
- Uses retrieved information to generate answers.
- Returns source document information with answers.
- Uses a fallback response when relevant information cannot be found.

**Embedding model:**

`sentence-transformers/all-MiniLM-L6-v2`

**Current knowledge base:**

The knowledge base contains four synthetic company documents:

- HR leave policy.
- IT VPN troubleshooting.
- IT software installation policy.
- Security password policy.

The latest recorded knowledge base contains 11 document chunks.

### 2. ChromaDB Cosine-Based Retrieval

The original ChromaDB collection used L2 distance, which caused negative relevance-score warnings with LangChain's default Euclidean relevance conversion.

A separate cosine-based collection was created to address the scoring mismatch.

Current configuration:

| Setting | Value |
|---|---|
| Vector database | ChromaDB |
| Active collection | `novadesk_docs_cosine` |
| Distance metric | Cosine |
| Document chunks | 11 |
| Retrieval threshold | 0.25 |
| Top retrieved chunks | 3 |

A custom cosine relevance-score conversion was implemented in `src/ingestion/retriever.py` to keep relevance scores within the 0–1 range.

The original `novadesk_docs` L2 collection has been preserved as a backup.

The new cosine collection has been manually tested with HR, IT, and unsupported questions. No negative relevance-score warning was observed in the latest verification.

### 3. AI Agent

- Built using LangChain's `create_agent`.
- Uses an LLM configured through `ChatGroq`.
- Uses the Groq model `openai/gpt-oss-20b`.
- Calls the `search_company_docs` tool to access company knowledge.
- Uses the existing RAG pipeline through the search tool.
- Asks clarifying questions when a request is too vague.
- Uses company documentation to answer policy and procedure questions.
- Is instructed not to invent answers when the available documentation does not contain the required information.
- Uses `@lru_cache(maxsize=1)` to reuse the configured agent.

### 4. FastAPI Backend

- `GET /health` — checks whether the API is running.
- `POST /ask` — accepts an employee question and returns the agent's answer.
- Uses Pydantic models for request validation.
- Includes basic logging and error handling.
- Supports interactive API testing through Swagger UI.
- Connects the `/ask` endpoint to `ask_agent()`.

### 5. Automated Testing

The project includes automated API and agent tests using pytest.

**API tests (`tests/test_api.py`):**

- Health endpoint.
- Blank question validation.
- Missing question validation.
- Successful question response.
- Unexpected error handling.

**Agent tests (`tests/test_agent.py`):**

- Checks whether the search tool correctly uses the RAG pipeline.
- Checks whether `ask_agent()` returns the final answer.
- Checks agent configuration and caching.

The agent tests use fake objects and monkeypatching to isolate individual components and avoid unnecessary live LLM calls.

**Latest recorded full test result: 8 tests passed.**

### 6. Agent Evaluation System

NovaDesk-AI includes a basic evaluation system for testing the behavior of the actual LLM-powered agent.

**Evaluation dataset:**

`evaluation/agent_eval_cases.json`

Contains four scenarios:

1. Company leave-policy question.
2. Vague employee question.
3. Unsupported company-policy question.
4. Software installation approval question.

Each evaluation case defines:

- A unique case ID.
- An employee question.
- The expected tool selection.
- Expected behavior.
- Expected source document, where applicable.
- Multiple acceptable answer phrases.

**Evaluation script:**

`scripts/evaluate_agent.py`

The script:

- Loads evaluation cases from the JSON file.
- Invokes the actual configured AI agent.
- Inspects the agent's tool calls.
- Checks whether the expected tools were selected.
- Checks whether the expected source documents were retrieved.
- Checks whether acceptable phrases appear in the final answer.
- Prints individual evaluation results and an overall summary.

**Run Agent Evaluation:**

```powershell
uv run python -m scripts.evaluate_agent
```

**Latest recorded evaluation result:**

```text
Total cases: 4
Passed: 4
Failed: 0
Success rate: 100.0%
```

**Important:** This is an initial evaluation system based on tool selection, source matching, and keyword checks. It does not perform full semantic evaluation or guarantee overall AI reliability.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python 3.12 |
| Dependency management | uv |
| LLM | Groq |
| LLM integration | LangChain |
| Agent framework | LangChain `create_agent` |
| Embeddings | Sentence Transformers |
| Embedding model | all-MiniLM-L6-v2 |
| Vector database | ChromaDB |
| Retrieval metric | Cosine similarity |
| API framework | FastAPI |
| Request validation | Pydantic |
| Automated testing | pytest |
| Evaluation data | JSON |

## Project Structure

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
│       ├── novadesk_docs
│       └── novadesk_docs_cosine
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

The vector-store directory is managed by ChromaDB. Its internal files and layout may vary.

The project structure may evolve as additional features are implemented.

## Setup and Installation

### Prerequisites

- Python 3.12 or later.
- Git.
- uv package manager.
- A Groq API key.

### 1. Clone the repository

```powershell
git clone https://github.com/rajpatel-09/NovaDesk-AI.git

cd NovaDesk-AI
```

### 2. Install project dependencies

```powershell
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root and add your Groq API key:

```text
GROQ_API_KEY=your_groq_api_key
```

Replace the example value with your own API key.

Do not commit your `.env` file or share your API key publicly.

### 4. Configure the existing development environment

For the current local development setup, the project uses an external uv environment.

Run this command in each new VS Code PowerShell terminal:

```powershell
$env:UV_PROJECT_ENVIRONMENT = "$env:LOCALAPPDATA\uv-envs\novadesk-ai"
```

Use the same environment consistently when running the project.

For a fresh installation on another machine, use the environment created by `uv sync` instead of assuming this machine-specific environment path exists.

## Running the Application

Start the FastAPI development server:

```powershell
uv run uvicorn src.api.main:app --reload
```

Open Swagger UI in your browser:

```text
http://127.0.0.1:8000/docs
```

Use `GET /health` to check the API and `POST /ask` to submit an employee question.

**Example request body for `POST /ask`:**

```json
{
  "question": "How many casual leave days do employees get?"
}
```

The answer should be based on information available in the company knowledge base.

## Running Tests

Run the complete test suite:

```powershell
uv run python -m pytest -v
```

Run only the API tests:

```powershell
uv run python -m pytest tests/test_api.py -v
```

Run only the agent tests:

```powershell
uv run python -m pytest tests/test_agent.py -v
```

The latest recorded full test run completed with **8 passing tests**.

Test results may change as the project evolves. Run the tests again after making changes.

## Running Agent Evaluation

Run the real-agent evaluation script:

```powershell
uv run python -m scripts.evaluate_agent
```

The evaluation script uses the scenarios defined in:

```text
evaluation/agent_eval_cases.json
```

It evaluates tool selection, document-source retrieval, and expected answer phrases.

The latest recorded result is:

- Total scenarios: 4
- Passed: 4
- Failed: 0
- Success rate: 100%

The evaluation uses the actual LLM-powered agent, so results may vary between runs. Keyword matching is a basic check and does not establish complete answer correctness.

## Learning Progress

### Phase 1 — RAG

**Status: Core implementation complete**

Implemented:

- Document loading and chunking.
- Embedding generation.
- ChromaDB vector storage.
- Similarity-based retrieval.
- Relevance threshold filtering.
- Answer generation using retrieved context.
- Source reporting and fallback responses.

The original L2 collection and the newer cosine collection are both retained.

### Phase 2 — FastAPI

**Status: Core API implementation and tests complete**

Implemented:

- Health endpoint.
- Question endpoint.
- Pydantic request validation.
- Logging and error handling.
- Agent integration.
- Automated API tests.

### Phase 3 — Agentic AI

**Status: Initial implementation complete; learning and improvements ongoing**

Implemented:

- LangChain agent using `create_agent`.
- Company-document search tool.
- System prompt defining assistant behavior.
- Agent caching.
- Agent unit tests.
- Real-agent manual experiments.
- Initial automated agent-evaluation system.
- Cosine-based retrieval migration.

The current focus is improving evaluation quality, understanding the implementation, and strengthening the agent's reliability.

### Upcoming Phases

- Phase 4 — LangGraph.
- Phase 5 — Model Context Protocol (MCP).
- Phase 6 — Production improvements and final project finishing.

These phases have not yet been completed.

## Current Limitations

- The assistant can only answer reliably from information available in the company knowledge base.
- A fallback response does not guarantee that every unsupported question will be handled perfectly.
- Agent unit tests use mocks and fake dependencies. They do not prove that a live LLM will always choose the correct tool.
- The evaluation dataset currently contains only four scenarios.
- The evaluation script uses keyword matching rather than semantic answer evaluation.
- Real LLM behavior may vary between runs.
- Further testing is required for production reliability, security, and error handling.
- Hugging Face Hub may display an unauthenticated-request warning when loading embedding models. The model has loaded successfully in the latest recorded runs.

## Repository

GitHub: https://github.com/rajpatel-09/NovaDesk-AI

---

**NovaDesk-AI** is an ongoing learning and development project focused on building a practical, documentation-grounded AI IT helpdesk assistant.