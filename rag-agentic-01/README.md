# Simple Agentic RAG — DQE Knowledge Assistant

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kumarsirish/FDP-AGENENTIC-AI-RAG/blob/main/rag-agentic-01/fictional-depatment-rag-agentic.ipynb)

A minimal **Agentic RAG (Retrieval-Augmented Generation)** system built with LangChain and FAISS. The agent decides at runtime whether to retrieve documents before answering — making it more efficient than naive RAG that always retrieves.

---

## How It Works

```
Traditional RAG:   Question → Always retrieve → Answer

Agentic RAG:       Question → Agent decides
                                  ├─ DQE-specific? → search_answers tool → FAISS retrieval → Answer
                                  └─ General knowledge? → Answer directly
```

**Example queries:**
- *"What is DQE?"* → Agent calls `search_answers`, retrieves from vector store, answers with context
- *"How many students does DQE have?"* → Agent retrieves and answers: ~140 students
- *"What is quantum computing?"* → Agent answers directly from LLM knowledge (no retrieval)

---

## Knowledge Base

The knowledge base contains information about the **Department of Quantum Engineering (DQE)**, a fictional department. Topics covered:

| Category | Details |
|---|---|
| Overview | 140 students, 20 professors, 5 courses, applied quantum computing |
| Courses | Foundations of Quantum AI (PG), Quantum Machine Learning (UG), IBM Qiskit, PennyLane |
| Hardware | IBM Quantum Network, Amazon Braket (cloud access for all students) |
| Research | Quantum AI, QNNs, Quantum Reinforcement Learning (QRL) |
| Project | QuLearn — hybrid classical-quantum models for drug discovery & materials science |

---

## Project Structure

```
rag-agentic-01/
├── fictional-depatment-rag-agentic.ipynb   # Main notebook
├── requirements.txt
└── vectorstore/                             # FAISS index (generated at runtime)
```

---

## Prerequisites

- Python 3.11+
- HuggingFace API token → [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- Google Gemini API key (optional, alternative LLM backend)

---

## Setup

**Option A — Run in Google Colab (recommended):**

Click the "Open in Colab" badge above. Add your secrets in Colab's Secrets panel (key icon in sidebar):
- `HF_TOKEN` — HuggingFace API token
- `GEMINI_API_KEY` — Google Gemini API key (optional)

**Option B — Run locally:**

```bash
pip install python-dotenv
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
HF_TOKEN=hf_your_token_here
GEMINI_API_KEY=your_key_here
```

Then update Cell 5 in the notebook to load from `.env`:
```python
from dotenv import load_dotenv
load_dotenv()
HF_TOKEN = os.environ.get("HF_TOKEN")
```

---

## Models Used

| Purpose | Model |
|---|---|
| Embeddings | `sentence-transformers/all-MiniLM-L12-v2` (local) |
| LLM | `Qwen/Qwen2.5-7B-Instruct` (HuggingFace Inference API) |
| LLM (alt) | `gemini-2.5-flash` (Google Gemini, via `langchain-google-genai`) |

---

## Notebook Walkthrough

| Cell | Step |
|---|---|
| 1 | Install dependencies from `requirements.txt` |
| 2 | Set API keys (Colab secrets or `.env`) |
| 3 | Define DQE knowledge base as inline text |
| 4 | Chunk, embed, and save FAISS vector store |
| 5 | Build `search_answers` tool + ReAct agent |
| 6 | Query the agent |

---

## Dependencies

```
langchain
langchain-community
langchain-core
langchain-text-splitters
langchain-huggingface
langchain-google-genai
huggingface_hub
faiss-cpu
sentence-transformers
tiktoken
pypdf
python-dotenv
```
