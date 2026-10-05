# NovaDesk AI

**AI-powered Internal IT Support & Knowledge Copilot**

NovaDesk AI is an AI-powered internal IT support assistant designed to answer employee questions, retrieve information from company documentation, and perform support-related actions through tools.

The project is being developed using a project-based learning approach while studying RAG, Agentic AI, LangGraph, and MCP.

---

## Project Objective

NovaDesk AI will eventually be able to:

* Answer questions from company documentation using RAG
* Decide whether retrieval or another action is required
* Perform support-related actions using tools
* Orchestrate workflows using LangGraph
* Access tools through MCP
* Expose functionality through an API
* Handle errors and edge cases
* Log important application events
* Include automated tests
* Provide project documentation

---

## Learning Path

```text
RAG
  ↓
Agentic AI
  ↓
LangGraph
  ↓
MCP
  ↓
Production-style improvements
```

---

## Learning Method

```text
Learn
  ↓
Implement
  ↓
Test
  ↓
Understand
  ↓
Modify
  ↓
Debug
  ↓
Move Forward
```

The goal is to understand how the system works rather than simply copy tutorial code.

---

## Planned Architecture

```text
                    User
                      │
                      ▼
                NovaDesk AI
                      │
                      ▼
                  AI Agent
                      │
             ┌────────┼────────┐
             │        │        │
             ▼        ▼        ▼
            RAG     Direct    MCP
                    LLM       Tools
             │                 │
             ▼          ┌──────┼──────┐
        Company Docs    │      │      │
                        ▼      ▼      ▼
                     Tickets Employees Assets
```

LangGraph will eventually orchestrate the workflow between these components.

---

## Technology Stack

* Python 3.12
* uv
* Ollama
* Local LLM
* Sentence Transformers
* Chroma
* LangGraph
* MCP
* FastAPI
* pytest

---

## Project Status

**Day 1 — Project foundation completed**

Current focus:

**Understanding and implementing the RAG foundation.**

---

## Project Structure

```text
NovaDesk-AI/
│
├── data/
│   ├── company_docs/
│   ├── database/
│   └── vector_store/
│
├── notebook/
│
├── src/
│   ├── config/
│   ├── ingestion/
│   ├── rag/
│   ├── agent/
│   ├── graph/
│   ├── mcp/
│   ├── tools/
│   └── api/
│
├── tests/
├── docs/
│
├── .gitignore
├── LEARNING_LOG.md
├── PROJECT_CONTEXT.md
├── README.md
├── pyproject.toml
└── uv.lock
```

---

## Future Features

* Company knowledge retrieval
* Source-aware answers
* Agentic routing
* IT support ticket tools
* MCP-based tool access
* LangGraph workflow orchestration
* FastAPI backend
* Logging
* Error handling
* Automated testing
* Documentation

```

Save the file.

**Stop here.** Tell me **“README updated.”**
```
