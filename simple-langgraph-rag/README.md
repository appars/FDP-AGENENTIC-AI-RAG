# Simple LangGraph RAG

## Steps to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your OpenAI API key
```bash
export OPENAI_API_KEY="sk-..."
```

### 3. Build the vector store (one-time)
```bash
python ingest.py
```
You should see: `Vector database created successfully`

### 4. Run the RAG app
```bash
python langgraph_rag.py
```

Type a question at the prompt, and type `exit` to quit.
