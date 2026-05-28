# RAG Scholarship Chatbot (LangChain + Qdrant)

Procedural RAG chatbot for Indian government scholarship discovery.

It uses:
- LangChain + LCEL
- OpenAI embeddings + chat model
- Qdrant Cloud vector database
- Session-based chat history (multi-turn)

## Major Steps

The notebook follows these core steps:

1. **Install dependencies**
    - `langchain`, `langchain-openai`, `langchain-qdrant`, `datasets`, `gradio`, `python-dotenv`

2. **Load base imports + environment variables**
    - Read API keys and runtime settings from `.env`

3. **Initialize global config and state**
    - `CONFIG`, `RETRIEVER`, `LLM`, `CHAINS`, `CHAT_HISTORIES`

4. **Validate configuration**
    - Ensure required values exist: OpenAI key, Qdrant URL, Qdrant API key

5. **Load scholarship dataset**
    - Source: `NetraVerse/indian-govt-scholarships` (Hugging Face)

6. **Split documents into chunks**
    - Convert records into LangChain `Document` chunks with metadata

7. **Create vector store + retriever**
    - Build embeddings
    - Push chunked texts to Qdrant Cloud via `QdrantVectorStore.from_texts(...)`
    - Create retriever with top-$k$ search

8. **Initialize LLM**
    - `ChatOpenAI` with model/temperature/max token settings

9. **Create formatting helpers**
    - Format retrieved docs as prompt context
    - Extract unique sources for response citation

10. **Prepare query input**
    - Normalize query text and create standardized input dict

11. **Build one LangChain chain (no query classification)**
    - Single system prompt
    - `RunnableLambda(assign_context_to_input)` → prompt → LLM → output parser

12. **Run chain directly**
    - No simple/moderate/complex routing
    - Direct invocation of main chain

13. **Manage chat history**
    - Per-session message storage and session helpers

14. **Process query end-to-end**
    - Add user message
    - Run chain
    - Retrieve sources
    - Add assistant message
    - Return structured response

15. **Test with sample queries**

16. **Test multi-turn conversation**
    - Reuse same `session_id` across turns

## Quick Start

### 1) Install requirements

```bash
pip install -r requirements.txt
```

### 2) Configure `.env`

Set at least:

```env
OPENAI_API_KEY=your_openai_key
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_key
```

Optional knobs:

```env
COLLECTION_NAME=scholarships
LLM_MODEL=gpt-3.5-turbo
TEMPERATURE=0.7
MAX_TOKENS=500
RETRIEVAL_K=3
CHUNK_SIZE=500
CHUNK_OVERLAP=100
EMBEDDING_MODEL=text-embedding-3-small
```

### 3) Run

- Notebook flow: open `notebook.ipynb` and run cells in order.
- App UI:

```bash
python app.py
```

## Project Files

- `notebook.ipynb` — primary step-by-step implementation
- `main.py` — script/module variant
- `app.py` — Gradio interface
- `requirements.txt` — dependencies
- `docs/` — architecture + function notes

## Notes

- Current flow uses **one chain only** (no complexity/relevance classification).
- Multi-turn behavior is session-based via `CHAT_HISTORIES`.
