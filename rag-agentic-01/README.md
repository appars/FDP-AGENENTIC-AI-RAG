# Simple Agentic RAG

A minimal **Agentic RAG (Retrieval-Augmented Generation)** system built with LangChain and FAISS. The agent decides at runtime whether to retrieve documents before answering — making it more efficient than naive RAG that always retrieves.

---

## How It Works

```
Traditional RAG:   Question → Always retrieve → Answer

Agentic RAG:       Question → Agent decides
                                  ├─ Need retrieval? → search_docs tool → Answer with context
                                  └─ No retrieval needed? → Answer directly
```

**Example:**
- *"What is 2 + 2?"* → Agent answers directly (no retrieval)
- *"How many students are in DISE?"* → Agent calls `search_docs`, retrieves from vector store, answers with context

---

## Project Structure

```
simple-agentic-rag/
├── simple_agentic_rag.ipynb   # Notebook walkthrough
├── docs/
│   └── knowledge.txt          # Knowledge base documents
├── requirements.txt
└── vectorstore/               # FAISS index (generated)
```

---

## Prerequisites

- Python 3.9+
- A HuggingFace account with a valid API token → [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

---

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install jupyter
jupyter notebook simple_agentic_rag.ipynb
```

---

## Run

Open `simple_agentic_rag.ipynb` and run all cells top to bottom.

Set your HuggingFace token in **Cell 2**:
```python
HF_TOKEN = "hf_your_token_here"
```

**Models used:**
| Purpose | Model |
|---|---|
| Embeddings | `sentence-transformers/all-MiniLM-L12-v2` (local cache) |
| LLM | `Qwen/Qwen2.5-7B-Instruct` (HuggingFace Inference API) |

---

## Dependencies

```
langchain
langchain-community
langchain-huggingface
langchain-core
langchain-text-splitters
faiss-cpu
sentence-transformers
tiktoken
pypdf
```

---

## Knowledge Base

The default knowledge base (`docs/knowledge.txt`) contains information about a fictitious department (DISE). Replace it with any plain text file to build a RAG system over your own documents, then re-run Cell 3 to rebuild the vector store.
