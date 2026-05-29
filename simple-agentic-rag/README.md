# Simple Agentic RAG using LangChain

## Overview

This project demonstrates a **very simple Agentic RAG (Retrieval Augmented Generation)** system using:

- LangChain Agent
- FAISS Vector Database
- OpenAI LLM
- Embeddings
- Tool Calling

The agent decides:

1. Whether retrieval is required
2. When to search documents
3. How to answer using retrieved context

---

## Project Structure

simple-agentic-rag/
│
├── app.py
├── ingest.py
├── agent_rag.py
├── docs/
│   └── knowledge.txt
├── requirements.txt
└── vectorstore/

---

## Installation

Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configure API Key

Set OpenAI API key:

Linux/Mac:

```bash
export OPENAI_API_KEY="your_key"
```

Windows:

```cmd
set OPENAI_API_KEY=your_key
```

---

## Step 1: Create Vector Database

Run:

```bash
python3 ingest.py
```

Expected output:

```text
Vector DB created successfully
```

---

## Step 2: Run Agentic RAG

Run:

```bash
python3 agent_rag.py
```

Example questions:

```text
What is RAG?
What is FAISS?
What is LangChain?
```

Type:

```text
exit
```

to quit.

---

## Why This Is Agentic RAG

Traditional RAG:

Question → Retrieve → Answer

Agentic RAG:

Question
   ↓
Agent decides:
Need retrieval?
   ↓
YES → Search documents
NO → Answer directly

Example:

Question:
What is 2 + 2?

Agent:
No retrieval needed

Question:
What is FAISS?

Agent:
Uses search_docs tool
