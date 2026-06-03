# Book Recommendation System with LangChain + RAG

A LangChain tutorial demonstrating real-world RAG (Retrieval-Augmented Generation) patterns using the Kaggle Book Recommendation Dataset and Qdrant vector database.

## Overview

This project implements a complete book recommendation system that showcases:
- Document loading with LangChain CSVLoader
- Qdrant vector store for semantic book retrieval (RAG)
- LangChain Expression Language (LCEL) chaining
- Control flow and routing with RunnableBranch
- Generate-Refine two-step pipeline
- Multi-turn conversation with memory
- Chain serialization and deserialization

**Dataset**: Real Kaggle Book Recommendation Dataset (271K books, 278K users, 1.1M ratings)
**Processing**: Sampled to top 1000 books by rating count

---

## Architecture

```
User Query
    │
    ▼
Qdrant Vector Store  ←── sentence-transformers/all-MiniLM-L6-v2 (embeddings)
    │ top-3 relevant books
    ▼
RAG Prompt  ←── {context} + {user_query}
    │
    ▼
LLM (OpenAI / Gemini / HuggingFace)
    │
    ▼
StrOutputParser → Response
```

---

## Quick Start

### Prerequisites
- Python 3.8+
- Kaggle account (for dataset download)
- One of: OpenAI API key, Google API key, or HuggingFace token
- Qdrant cloud account (free tier at cloud.qdrant.io)

### Installation

1. **Clone/Download the project**
   ```bash
   cd book-recommendation-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** — create a `.env` file:
   ```bash
   # LLM providers (use whichever you have)
   OPENAI_API_KEY=sk-...
   GOOGLE_API_KEY=...
   HF_TOKEN=hf_...

   # Qdrant remote (required)
   QDRANT_HOST=https://your-cluster.qdrant.io
   QDRANT_API_KEY=your-qdrant-api-key
   ```

5. **Run the notebook**
   ```bash
   jupyter notebook book_recommendation.ipynb
   ```
   Execute cells sequentially from top to bottom.

---

## Notebook Structure

### Cell 1 — Install Dependencies
Installs all packages from `requirements.txt` and downloads the Kaggle dataset.

### Cell 2 — Setup and Imports
Loads environment variables and imports core libraries.

### Cell 3 — Load and Explore Dataset
```python
books_df = pd.read_csv('data/Books.csv', encoding='latin-1')
ratings_df = pd.read_csv('data/Ratings.csv')
users_df = pd.read_csv('data/Users.csv')
```

### Cell 4 — Prepare Data
Samples top 1000 books by rating count and saves to `books_for_llm.csv`.

### Cell 5 — Model Initialization (Model Agnostic)
```python
llm = init_chat_model(
    model="huggingface:TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    temperature=0.7,
)
```
Swap the model line to switch providers — no other code changes needed.

**Supported models:**
| Provider | Model string |
|----------|-------------|
| OpenAI | `openai:gpt-4o-mini` |
| Google Gemini | `google_genai:gemini-2.5-flash-lite` |
| HuggingFace 1.1B | `huggingface:TinyLlama/TinyLlama-1.1B-Chat-v1.0` |
| HuggingFace 3.8B | `huggingface:microsoft/Phi-3-mini-4k-instruct` |
| HuggingFace 7B | `huggingface:HuggingFaceH4/zephyr-7b-beta` |

### Cell 6 — Messages
Basic message-based conversation using `SystemMessage` and `HumanMessage`.

### Cell 7 — Document Loader
Loads `books_for_llm.csv` using `CSVLoader` — each row becomes a `Document` object.

### Cell 8 — Qdrant Vector Store
```python
vectorstore = QdrantVectorStore.from_documents(
    documents, embeddings,
    url=QDRANT_URL, api_key=QDRANT_API_KEY,
    collection_name="books",
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
```
Embeds all 992 books and inserts into Qdrant. The retriever fetches top 3 semantically relevant books per query — **not all 992**.

### Cell 9 — Retrieve & Inject into Prompt (RAG)
Demonstrates retrieval in action and defines the RAG prompt template.

### Cell 10 — LCEL RAG Chain
```python
rag_chain = (
    {"context": retriever | format_books, "user_query": lambda x: x}
    | recommendation_prompt
    | llm
    | StrOutputParser()
)
```
Full RAG pipeline: query → Qdrant retrieval → prompt → LLM → answer.

### Cell 11 — Control Flow (RunnableBranch)
Routes to recommendation or analysis chain based on keywords in the query.

### Cell 12 — Generate-Refine Pipeline
Two-step chain: generate initial recommendations → refine with more detail.

### Cell 13 — Message History Memory
Multi-turn conversation with sliding window of last 4 messages (2 exchanges) to stay within token limits.

### Cell 14 — Serialization
Save and reload the prompt chain as JSON.

---

## Project Structure

```
book-recommendation-system/
├── README.md                        # This file
├── requirements.txt                 # All dependencies
├── book_recommendation.ipynb        # Main Jupyter notebook
├── book_recommendation_openai.ipynb # OpenAI version
├── book_chain_kaggle.json           # Serialized prompt (generated)
├── books_for_llm.csv                # Sampled book catalog (generated)
└── data/
    ├── Books.csv                    # Full book dataset
    ├── Ratings.csv                  # Rating records
    └── Users.csv                    # User information
```

---

## Key Concepts

| Concept | Cell | Description |
|---------|------|-------------|
| Messages | 6 | Structured conversation with system/human roles |
| Document Loader | 7 | Load CSV rows as LangChain Documents |
| Qdrant RAG | 8 | Semantic search — retrieve only relevant books |
| LCEL Chain | 10 | `retriever \| prompt \| llm \| parser` pipeline |
| RunnableBranch | 11 | Conditional routing based on query intent |
| Generate-Refine | 12 | Multi-step LLM pipeline |
| Memory | 13 | Multi-turn conversation with history trimming |
| Serialization | 14 | Save/load chains as JSON |

---

## Why RAG Instead of Stuffing?

Without RAG, all 992 books (~330K characters, ~175K tokens) are dumped into every prompt. This exceeds every model's context window and makes every call extremely slow.

With Qdrant RAG, only 3 relevant books (~150 tokens) are sent per query:

| | Without RAG | With Qdrant RAG |
|--|------------|----------------|
| Tokens per call | ~175,000 | ~150 |
| Fits in model context | No | Yes |
| Speed | Very slow | Fast |

---

## Troubleshooting

**401 Unauthorized (HuggingFace)**
The notebook calls `huggingface_hub.login(token=HF_TOKEN)` automatically. Ensure `HF_TOKEN` is set in your `.env` file.

**Token limit exceeded**
Switch to a smaller model or reduce `k` in the retriever (`search_kwargs={"k": 2}`).

**ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**CSV File Not Found**
Re-run Cell 1 which downloads and extracts the Kaggle dataset automatically.

**Qdrant connection error**
Verify `QDRANT_HOST` and `QDRANT_API_KEY` in your `.env` file. Get free credentials at cloud.qdrant.io.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `QDRANT_HOST` | Yes | Qdrant cluster URL |
| `QDRANT_API_KEY` | Yes | Qdrant API key |
| `HF_TOKEN` | For HF models | HuggingFace access token |
| `OPENAI_API_KEY` | For OpenAI | OpenAI API key |
| `GOOGLE_API_KEY` | For Gemini | Google API key |

---

**LangChain Version**: 0.3+
**Python Version**: 3.8+
