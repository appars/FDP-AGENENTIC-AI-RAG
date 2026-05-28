# Quick Start Guide

## 5-Minute Setup

### Step 1: Get Your Credentials (2 minutes)

**OpenAI:**
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy it

**Qdrant Cloud:**
1. Go to https://qdrant.io/
2. Sign up (free tier available)
3. Create a cluster
4. Copy REST API URL and API key from cluster settings

### Step 2: Setup Project (2 minutes)

```bash
# Extract
unzip rag_scholarship_chatbot.zip
cd rag_scholarship_chatbot

# Setup (auto-creates venv and installs dependencies)
bash setup.sh          # Linux/Mac
# or
setup.bat              # Windows
```

### Step 3: Configure (1 minute)

```bash
# Edit .env with your credentials
nano .env
```

Add these three lines:
```
OPENAI_API_KEY=sk-xxxxx
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=xxxxx
```

### Step 4: Run (1 minute)

```bash
# Option A: Web interface
python app.py
# Open http://localhost:7860

# Option B: Command line
python main.py
```

## Quick Examples

### Single Query
```python
from main import initialize_system, process_query

initialize_system()
result = process_query("What scholarships for engineers?")
print(result["full_response"])
```

### Multi-turn Chat
```python
initialize_system()

# First question
result1 = process_query("What scholarships?", session_id="user_1")
print(result1["response"])

# Follow-up (has context from first)
result2 = process_query("Tell me more about AICTE", session_id="user_1")
print(result2["response"])
```

## All Functions

- `initialize_system()` - Setup everything
- `process_query(message, session_id)` - Get response
- `get_or_create_history(session_id)` - Get chat history
- `clear_session(session_id)` - Clear history
- `get_session_info(session_id)` - Get stats

## Configuration

All in `.env` file:

```bash
OPENAI_API_KEY=your-key
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-key

LLM_MODEL=gpt-3.5-turbo    # or gpt-4
TEMPERATURE=0.7             # 0-1
RETRIEVAL_K=3               # docs to retrieve
```

## Troubleshooting

| Error | Fix |
|-------|-----|
| "API key not found" | Check .env file exists |
| "Connection refused" | Check QDRANT_URL is correct |
| "Rate limited" | Use gpt-3.5-turbo, reduce requests |
| "Memory error" | Reduce RETRIEVAL_K in .env |

## File Overview

- `main.py` - All functions (500+ lines)
- `app.py` - Web interface
- `setup.sh/.bat` - Automated setup
- `.env.example` - Config template
- `requirements.txt` - Dependencies

## Next Steps

1. ✅ Extract zip
2. ✅ Run setup script  
3. ✅ Edit .env
4. ✅ Run `python app.py`
5. ✅ Test it!

That's it! 🚀

---

For more help, see README.md
