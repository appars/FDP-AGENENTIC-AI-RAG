# Simple LangGraph RAG Application

## Overview

This project demonstrates a **simple Retrieval Augmented Generation (RAG)** application using **LangGraph**.

Unlike normal LangChain RAG, LangGraph organizes the application as a **workflow graph**.

This project intentionally keeps things simple for learning purposes.

The flow is:

Question
   ↓
Retrieve Documents
   ↓
Generate Answer
   ↓
Final Response

---

## Why LangGraph?

LangGraph is useful when applications need:

- Multiple steps
- Workflow orchestration
- State management
- Conditional branching
- Multi-agent systems
- Loops and retries

This example shows a very simple graph with two nodes.

### Node 1: Retriever

Searches vector database and retrieves relevant context.

### Node 2: Generator

Uses the retrieved context to generate the answer.

---

## Project Structure

simple-langgraph-rag/

├── app.py
├── ingest.py
├── langgraph_rag.py
├── requirements.txt
├── docs/
│   └── knowledge.txt
└── vectorstore/

---

## Architecture

Question
   ↓
[Retrieve Node]
   ↓
[Generate Answer Node]
   ↓
Final Answer

---

## Step 1: Create Virtual Environment

Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```cmd
python -m venv venv
venv\Scripts\activate
```

---

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 3: Configure OpenAI API Key

Linux/Mac:

```bash
export OPENAI_API_KEY="your_key"
```

Windows:

```cmd
set OPENAI_API_KEY=your_key
```

Verify:

```bash
echo $OPENAI_API_KEY
```

---

## Step 4: Create Vector Database

Run:

```bash
python3 ingest.py
```

Expected output:

```text
Vector database created successfully
```

This creates:

vectorstore/

folder with embeddings.

---

## Step 5: Run Application

Run:

```bash
python3 langgraph_rag.py
```

Example Questions:

```text
What is RAG?
What is LangGraph?
What is FAISS?
```

Type:

```text
exit
```

to quit.

---

## Example Execution

Question:

```text
What is LangGraph?
```

Execution:

```text
[Retriever Node Executed]
[Generator Node Executed]
```

Answer:

```text
LangGraph is used to create multi-step workflows for AI agents.
```

---

## Understanding the Code

### State

LangGraph uses a shared state object.

Example:

```python
class GraphState(TypedDict):
    question: str
    retrieved_docs: str
    answer: str
```

State moves across nodes.

---

### Retriever Node

Purpose:

- Search vector DB
- Retrieve similar content

Input:

Question

Output:

Retrieved documents

---

### Generator Node

Purpose:

- Read retrieved context
- Ask LLM to answer

Input:

Question + Retrieved Context

Output:

Answer

---

## Difference from LangChain Agentic RAG

LangChain Agentic RAG:

Agent decides what tools to call.

LangGraph RAG:

Workflow is explicitly defined.

Example:

retrieve → answer

In advanced systems:

planner → retrieve → grade → rewrite → answer

This is why LangGraph is useful for complex workflows.

---

## Next Improvements

Possible extensions:

1. Add query rewriting node
2. Add document grading node
3. Add retry logic
4. Add web search
5. Add multiple agents
6. Add memory

