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

**Status: Not started.**

Planned work: expose the existing RAG pipeline through HTTP endpoints without rebuilding the completed RAG functionality.

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