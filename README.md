# FDP — Agentic AI & RAG Workshop

A hands-on Faculty Development Programme (FDP) workshop series covering the full RAG (Retrieval-Augmented Generation) stack — from a basic LangChain pipeline all the way to multi-agent systems built with Google ADK, evaluated with RAGAS, and augmented with GitHub Copilot and Claude.

All notebooks run on **Google Colab** (free tier). Each module is self-contained and builds on the previous one.

---

## Repository Structure

```
FDP-AGENENTIC-AI-RAG/
├── rag-langchain-00/          # Module 0 — Basic RAG with LangChain
├── rag-agentic-01/            # Module 1 — Agentic RAG (tool-calling agent)
├── rag-langgraph-02/          # Module 2 — Corrective RAG with LangGraph
├── rag-ragas-03/              # Module 3 — RAG Evaluation with RAGAS
├── rag-complete-04/           # Module 4 — Real-world RAG (book recommendations)
├── rag-adk-06/                # Module 6 — Google ADK (single & multi-agent)
└── github-copilot-claude-07/  # Module 7 — AI-assisted coding tools
```

---

## Modules

### Module 0 — Basic RAG with LangChain [`rag-langchain-00/`](rag-langchain-00/)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kumarsirish/FDP-AGENENTIC-AI-RAG/blob/main/rag-langchain-00/fictional-department-rag-langchain.ipynb)

**Problem:** How does a language model answer questions about information it has never seen — private documents, internal knowledge bases, or domain-specific data?

**What it does:** Builds a complete RAG pipeline from scratch using a fictional university department (DQE — Department of Quantum Engineering) as the knowledge base. Demonstrates the core RAG loop: embed documents → store in FAISS → retrieve on query → generate grounded answer — then compares the result to the same question answered without retrieval, making hallucination clearly visible.

**Key concepts:** LangChain LCEL chains, HuggingFace local embeddings (`all-MiniLM-L12-v2`), FAISS vector store, model-agnostic LLM initialisation (`init_chat_model`).

**LLM options:** Gemini 2.5 Flash (default) · OpenAI GPT-4o · HuggingFace TinyLlama · Groq

---

### Module 1 — Agentic RAG [`rag-agentic-01/`](rag-agentic-01/)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kumarsirish/FDP-AGENENTIC-AI-RAG/blob/main/rag-agentic-01/fictional-depatment-rag-agentic.ipynb)

**Problem:** Naive RAG always retrieves — even for general questions that the LLM already knows the answer to. This wastes compute and can inject irrelevant context.

**What it does:** Upgrades the Module 0 pipeline to an **agentic** design. A LangChain ReAct agent wraps the vector store as a `search_answers` tool and decides at runtime whether retrieval is necessary. Department-specific questions trigger retrieval; general knowledge questions are answered directly from the LLM.

```
Traditional RAG:  Question → Always retrieve → Answer
Agentic RAG:      Question → Agent decides
                               ├─ DQE-specific? → search_answers → FAISS → Answer
                               └─ General?      → Answer directly
```

**Key concepts:** LangChain tool use, ReAct agent loop, conditional retrieval, FAISS persistence.

**LLM options:** Qwen 2.5-7B (HuggingFace, default) · Gemini 2.5 Flash · OpenAI GPT-4o

---

### Module 2 — Corrective RAG with LangGraph [`rag-langgraph-02/`](rag-langgraph-02/)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kumarsirish/FDP-AGENENTIC-AI-RAG/blob/main/rag-langgraph-02/fictional-depatment-rag-langraph.ipynb)

**Problem:** A single retrieval pass can fail — the retrieved chunks may be irrelevant, or the generated answer may hallucinate facts not in the context. There is no feedback loop to catch these failures.

**What it does:** Implements **Corrective RAG (CRAG)** as a stateful LangGraph graph. The pipeline retrieves documents, has an LLM judge their relevance, optionally rewrites the query and re-retrieves, generates an answer, and then has a second LLM judge check whether the answer is grounded — retrying generation if it detects hallucination (max 2 retries).

```
START → retrieve → assess_docs ──relevant──→ generate_answer → grade_answer → END
                       │                            ↑               │
                   not relevant               (retry ≤ 2)      hallucination
                       ↓                                            │
                  rewrite_query ──────────────────────────────────→ ↑
```

**Key concepts:** LangGraph state machines, conditional edges, LLM-as-judge, self-correcting pipelines.

**LLM options:** Gemini 2.5 Flash (default) · HuggingFace · OpenAI · Anthropic Claude · Ollama (local)

---

### Module 3 — RAG Evaluation with RAGAS [`rag-ragas-03/`](rag-ragas-03/)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kumarsirish/FDP-AGENENTIC-AI-RAG/blob/main/rag-ragas-03/fictional-department-rag-ragas.ipynb)

**Problem:** How do you know if your RAG system is actually working? Traditional NLP metrics (BLEU, ROUGE) measure word overlap against a reference — they cannot detect hallucination, irrelevant retrieval, or missing evidence.

**What it does:** Builds the same agentic RAG system from Module 1, then evaluates it using **RAGAS** — a framework purpose-built for RAG evaluation. Runs four metrics against three test questions with ground-truth answers and prints a scored results table.

| Metric | What it measures |
|---|---|
| **Faithfulness** | Are all claims in the answer supported by the retrieved chunks? |
| **Answer Relevancy** | Does the answer actually address the question asked? |
| **Context Precision** | Are the top-ranked retrieved chunks the useful ones? |
| **Context Recall** | Did retrieval surface all the evidence needed to answer? |

Scores range 0–1 (higher is better). The notebook also explains why BLEU/ROUGE and classical ML metrics fall short for RAG and how to diagnose low scores.

**Key concepts:** RAGAS metrics, LLM-as-judge evaluation, `EvaluationDataset`, `SingleTurnSample`.

---

### Module 4 — Real-world RAG: Book Recommendations [`rag-complete-04/`](rag-complete-04/)

**Problem:** Academic RAG examples use tiny inline knowledge bases. How does RAG hold up on a real-world dataset where stuffing all documents into a prompt is impossible?

**What it does:** Builds a production-style book recommendation system using the **Kaggle Book Recommendation Dataset** (271K books, 278K users, 1.1M ratings). Demonstrates why RAG is essential at scale — sending all 992 sampled books to the LLM would require ~175K tokens per call; Qdrant RAG sends only ~150 tokens (top-3 relevant books).

Covers the full LangChain feature set in one notebook:

| Cell | Pattern |
|---|---|
| 7 | CSVLoader — load rows as Documents |
| 8 | Qdrant vector store (cloud) |
| 10 | LCEL RAG chain |
| 11 | RunnableBranch — conditional routing by query intent |
| 12 | Generate-Refine two-step pipeline |
| 13 | Multi-turn memory (sliding window) |
| 14 | Chain serialisation / deserialisation |

**Key concepts:** Qdrant cloud vector store, RunnableBranch routing, generate-refine, conversation memory, chain serialisation.

**Requires:** Qdrant cloud account (free tier), Kaggle account for dataset download.

---

### Module 6 — Google ADK: Single & Multi-Agent [`rag-adk-06/`](rag-adk-06/)

**Problem:** Real-world assistant tasks span multiple domains (schedule, syllabus, quiz generation). A single monolithic agent struggles to handle all of them cleanly.

This module contains two notebooks:

#### 6a — Single Agent Hands-On Lab [`google_adk_single_agent.ipynb`](rag-adk-06/google_adk_single_agent.ipynb)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kumarsirish/FDP-AGENENTIC-AI-RAG/blob/main/rag-adk-06/google_adk_single_agent.ipynb)

**What it does:** Introduces the **Google Agent Development Kit (ADK)** by building a single `LlmAgent` with weather lookup, maths, time, and notes tools. Teaches the core ADK concepts: `LlmAgent`, `InMemorySessionService`, `Runner`, `ToolContext`, and the event stream. The `ask_verbose()` helper exposes every tool call and result so the agent's reasoning is fully observable.

#### 6b — Professor's AI Assistant (Multi-Agent) [`professor_assistant_adk.ipynb`](rag-adk-06/professor_assistant_adk.ipynb)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kumarsirish/FDP-AGENENTIC-AI-RAG/blob/main/rag-adk-06/professor_assistant_adk.ipynb)

**What it does:** Builds a multi-agent system for professors with three specialised sub-agents orchestrated by a root agent:

| Agent | Responsibility |
|---|---|
| **Syllabus Agent** | Answers questions from an uploaded syllabus PDF |
| **Timetable Agent** | Reads a timetable PDF; finds schedules and free slots by professor name |
| **Quiz Agent** | Generates MCQ quizzes from syllabus content and saves them to session state |

The root agent routes questions to the right sub-agent using `AgentTool`. Demonstrates multi-agent delegation, PDF ingestion with PyPDF2, and session state sharing across agents. Includes live demo outputs showing each delegation step (`→ [agent_called]`).

**Key concepts:** Google ADK, `LlmAgent`, `AgentTool`, `InMemorySessionService`, `Runner`, multi-agent orchestration, `ToolContext` state.

---

### Module 7 — AI-Assisted Coding with GitHub Copilot & Claude [`github-copilot-claude-07/`](github-copilot-claude-07/)

**Problem:** How do AI coding assistants accelerate real software development tasks — from writing new code to testing, refactoring, and building full applications?

**What it does:** A collection of practical examples showing GitHub Copilot and Claude in the development loop:

| File | Description |
|---|---|
| [`student_grader.py`](github-copilot-claude-07/student_grader.py) | Student marks calculator with average and grade logic |
| [`test_student_grader.py`](github-copilot-claude-07/test_student_grader.py) | Unit tests for the grader (Copilot-assisted) |
| [`StudentMarks.java`](github-copilot-claude-07/StudentMarks.java) | Java equivalent — cross-language code generation demo |
| [`teaching_assistant.py`](github-copilot-claude-07/teaching_assistant.py) | Streamlit app using TinyLlama to generate explanations, MCQs, assignments, and references from a syllabus PDF |
| [`movies_recos.py`](github-copilot-claude-07/movies_recos.py) | Movie recommendation script |
| [`app.py`](github-copilot-claude-07/app.py) | Main Streamlit entry point |
| [`chat-application-prompt.txt`](github-copilot-claude-07/chat-application-prompt.txt) | Prompt used to scaffold the chat app with Claude |

**Key concepts:** Prompt-driven code generation, AI-assisted unit testing, Streamlit UI, TinyLlama local inference, GitHub Copilot workflow.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Google account | For Colab and Google AI Studio |
| Gemini API key | Free at [aistudio.google.com](https://aistudio.google.com) |
| HuggingFace token | Free at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| Qdrant account | Free tier at [cloud.qdrant.io](https://cloud.qdrant.io) — Module 4 only |
| Kaggle account | Dataset download — Module 4 only |

Add secrets in Colab's **Secrets panel** (🔑 icon in sidebar):

```
GEMINI_API_KEY   → your Gemini key (also set as GOOGLE_API_KEY)
HF_TOKEN         → your HuggingFace token
QDRANT_HOST      → your Qdrant cluster URL (Module 4)
QDRANT_API_KEY   → your Qdrant API key (Module 4)
```

---

## Learning Path

```
Module 0  →  Module 1  →  Module 2  →  Module 3
 Basic RAG    Agent RAG    Corrective    Evaluate
 LangChain    tool-use      LangGraph     RAGAS
                                           ↓
                                       Module 4
                                       Real-world
                                        Qdrant
                                           ↓
                                       Module 6
                                       Google ADK
                                      Multi-agent
                                           ↓
                                       Module 7
                                        Copilot
                                        Claude
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | LangChain · LangGraph · Google ADK |
| Embeddings | `sentence-transformers/all-MiniLM-L12-v2` (local) |
| Vector stores | FAISS (local) · Qdrant (cloud) |
| LLMs | Gemini 2.5 Flash · Qwen 2.5-7B · TinyLlama · OpenAI · Anthropic |
| Evaluation | RAGAS |
| UI | Streamlit |
| Runtime | Google Colab · Python 3.11+ |
