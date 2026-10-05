# NovaDesk AI

## Product Name

NovaDesk AI

## Product Description

AI-powered Internal IT Support & Knowledge Copilot

---

## Project Goal

Build an industry-style AI internal IT helpdesk assistant that can:

* Answer questions from company documentation using RAG
* Decide whether retrieval or another action is required
* Use an agentic workflow
* Orchestrate the workflow with LangGraph
* Use MCP tools for external actions
* Provide a clean API
* Include logging, error handling, testing, and documentation

---

## Learning Order

1. RAG
2. Agentic AI
3. LangGraph
4. MCP
5. Production-style improvements

---

## Learning Method

Learn → Implement → Test → Understand → Modify → Debug → Move forward

Tutorials and documentation will be used as learning resources, but the final project will be implemented progressively rather than copied from one tutorial.

---

## Current Stage

Day 1 — Project foundation completed

---

## Tech Stack

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

## Main Project Components

### Knowledge Base

Company documentation such as:

* IT policies
* VPN troubleshooting guides
* Laptop policies
* Security guidelines
* Software installation policies
* Support procedures

### Agent

The agent will determine whether the user's request requires:

* Knowledge retrieval
* A direct response
* A tool/action

### RAG

The RAG system will:

* Load company documents
* Split documents into chunks
* Generate embeddings
* Store embeddings
* Retrieve relevant information
* Provide context to the LLM

### LangGraph

LangGraph will orchestrate the application workflow using:

* State
* Nodes
* Edges
* Conditional routing

### MCP

MCP will expose tools such as:

* Get ticket status
* Create a support ticket
* Update a support ticket
* Get employee information
* Get assigned device information

---

## Learning Goals

By the end of the project, I should be able to:

* Explain the complete RAG pipeline.
* Build and debug a RAG system.
* Explain the difference between normal RAG and agentic workflows.
* Build an agentic workflow.
* Understand LangGraph state, nodes, edges, and conditional routing.
* Build and use MCP tools.
* Explain how RAG, Agentic AI, LangGraph, and MCP work together.
* Write cleaner project-level Python code.
* Handle errors and edge cases.
* Write tests.
* Expose functionality through an API.
* Explain the architecture to a mentor or interviewer.

---

## Important Decisions

* The existing YTRAG project remains untouched.
* NovaDesk AI is the clean project for the internship.
* The core application should not require paid LLM APIs.
* Local/open-source technologies will be preferred.
* Synthetic company data will be used.
* The project will be built incrementally.
* Understanding is more important than tutorial completion.

---

## Current Status

Project foundation completed.

Next major stage:

RAG foundation.
