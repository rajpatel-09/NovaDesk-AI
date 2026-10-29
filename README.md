# NovaDesk-AI — AI IT Helpdesk Copilot

NovaDesk-AI is an AI-powered IT helpdesk assistant that answers employee questions using company documentation. The project combines Retrieval-Augmented Generation (RAG), an AI agent with tool calling, and a FastAPI backend.

The goal is to build a practical helpdesk application while learning how to develop, test, and structure AI applications using industry-style practices.

## Project Goals

- Answer employee questions using internal company documents.
- Retrieve relevant information before generating an answer.
- Use an AI agent that can call a tool to search company knowledge.
- Ask clarifying questions when a user's request is vague.
- Avoid inventing company policies when the required information is unavailable.
- Expose the assistant through a REST API using FastAPI.
- Build automated tests for the API and agent components.

## Current Features

### 1. Retrieval-Augmented Generation (RAG)

- Loads company knowledge from text documents.
- Splits documents into chunks and creates embeddings.
- Stores and retrieves document chunks using ChromaDB.
- Uses retrieved information to generate answers.
- Returns source information with answers.
- Uses a fallback response when relevant information cannot be found.

### 2. AI Agent

- Built with LangChain's `create_agent`.
- Uses an LLM configured through `ChatGroq`.
- Calls the `search_company_docs` tool to access company knowledge.
- Asks clarifying questions when a request is too vague.
- Uses company documentation to answer policy and procedure questions.
- Is instructed not to invent answers when the available documentation does not contain the information.

### 3. FastAPI Backend

- `GET /health` — checks whether the API is running.
- `POST /ask` — accepts a question and returns the agent's answer.
- Uses Pydantic models for request validation.
- Includes basic logging and error handling.
- Supports interactive API testing through Swagger UI.

### 4. Automated Testing

- API tests cover the main endpoint behavior and validation.
- Agent tests check the document-search tool, final-answer extraction, and agent initialization.
- Tests use mocks and fakes where appropriate to avoid unnecessary external API calls.

**Latest recorded test result:** 8 tests passed.

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Dependency management | uv |
| LLM | Groq through LangChain |
| Agent framework | LangChain |
| Embeddings | Sentence Transformers |
| Vector database | ChromaDB |
| API framework | FastAPI |
| Request validation | Pydantic |
| Testing | pytest |

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
├── PROJECT_CONTEXT.md
├── LEARNING_LOG.md
└── README.md
```

The project structure may evolve as additional features are implemented.

## Setup and Installation

### Prerequisites

- Python 3.12 or later
- Git
- uv package manager
- A Groq API key

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

Replace the example value with your own API key. Do not commit your `.env` file or share the key publicly.

### 4. Configure the environment in PowerShell

If you are using the existing external uv environment for this project, run this command in each new VS Code PowerShell terminal:

```powershell
$env:UV_PROJECT_ENVIRONMENT = "$env:LOCALAPPDATA\uv-envs\novadesk-ai"
```

Use the same environment configuration consistently when running the project.

## Running the Application

Start the FastAPI development server:

```powershell
uv run uvicorn src.api.main:app --reload
```

Open Swagger UI in your browser:

```text
http://127.0.0.1:8000/docs
```

Use `GET /health` to check the API and `POST /ask` to submit a question.

Example request body for `POST /ask`:

```json
{
  "question": "How many casual leave days do employees get?"
}
```

The answer should be based on the company documentation available to the application.

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

The latest recorded full test run completed with **8 passing tests**. Test results may change as the project evolves.

## Learning Progress

### Phase 1 — RAG

**Status: Core implementation complete**

Implemented document loading, chunking, embeddings, ChromaDB retrieval, answer generation, and source reporting.

### Phase 2 — FastAPI

**Status: Core API implementation and tests complete**

Implemented the health endpoint, question endpoint, validation, error handling, and API tests.

### Phase 3 — Agentic AI

**Status: Implementation started; learning and verification in progress**

Added an agent using LangChain's `create_agent`, a company-document search tool, and a system prompt defining the assistant's behavior.

The current focus is understanding the implementation line by line, testing the agent's behavior, and strengthening the code and tests.

### Upcoming Phases

- Phase 4 — LangGraph
- Phase 5 — Model Context Protocol (MCP)
- Phase 6 — Production improvements and final project finishing

These phases have not yet been completed.

## Current Limitations

- The assistant can only answer reliably from information available in the company knowledge base.
- A fallback response does not guarantee that every retrieval failure or unsupported question will be handled perfectly.
- Agent tests use mocks and fakes to verify code behavior. They do not, by themselves, prove that a live LLM will always choose the correct tool or follow every instruction.
- Live model behavior and additional production concerns still need further testing.

## Repository

GitHub: https://github.com/rajpatel-09/NovaDesk-AI

---

**NovaDesk-AI** is an ongoing learning and development project focused on building a practical, documentation-grounded AI helpdesk assistant.
