# Book Recommendation System with LangChain

A comprehensive LangChain tutorial demonstrating real-world RAG (Retrieval-Augmented Generation) patterns using the Kaggle Book Recommendation Dataset.

## 📚 Overview

This project implements a complete book recommendation system that showcases:
- Document loading and injection
- LangChain Expression Language (LCEL) chaining
- Control flow and routing
- Multi-turn conversation with memory
- Chain serialization and deserialization

**Dataset**: Real Kaggle Book Recommendation Dataset (271K books, 278K users, 1.1M ratings)  
**Processing**: Sampled to 1000 popular books for faster LLM processing

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key (or alternative LLM provider)

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

4. **Set up API key**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   # OR create .env file in parent directory (../.env)
   OPENAI_API_KEY=your-api-key-here
   ```

5. **Download dataset** (if not already present)
   - Download from: https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset
   - Extract CSV files to `data/` folder:
     - `data/Books.csv`
     - `data/Ratings.csv`
     - `data/Users.csv`

---

## 📖 Step-by-Step Guide

### Step 1: Download the Dataset
- Manual download from Kaggle or use Kaggle API
- Place CSV files in the `data/` directory

### Step 2: Setup and Imports
- Install LangChain, OpenAI, and supporting libraries
- Load environment variables (API keys)
- Import core dependencies

### Step 3: Load and Explore Dataset
```python
# Load Kaggle datasets
books_df = pd.read_csv('data/Books.csv', encoding='latin-1')
ratings_df = pd.read_csv('data/Ratings.csv')
users_df = pd.read_csv('data/Users.csv')
```
Explore the structure, shape, and sample rows from each dataset.

### Step 4: Prepare Data for LangChain
- Sample top 1000 books by rating count
- Rename columns for clarity
- Save as `books_for_llm.csv` for document loader

### Step 5: Model Initialization (Model Agnostic)
```python
llm = init_chat_model(
    model="openai:gpt-4o-mini",  # Easily switch models
    temperature=0.7,
    max_tokens=500
)
```
**Supported models:**
- OpenAI: `openai:gpt-4o-mini`, `openai:gpt-4`
- Google Gemini: `google_genai:gemini-2.5-flash-lite`
- HuggingFace: `huggingface_hub:meta-llama/Llama-2-7b-chat-hf`

### Step 6: Messages - Simple Conversation
Demonstrate basic message-based conversation with system and human roles.

### Step 7: Document Loader
Load CSV documents using LangChain's CSVLoader:
```python
loader = CSVLoader(file_path="books_for_llm.csv")
documents = loader.load()
```
Each row becomes a Document object with structured content.

### Step 8: Inject Documents into Prompts
Create a `ChatPromptTemplate` that includes the book catalog context:
```python
recommendation_prompt = ChatPromptTemplate.from_template(
    "You are a book recommendation expert...\n"
    "Here are available books:\n{books_context}\n"
    "User request: {user_query}\n..."
)
```
Books context is **hardcoded** into the prompt template for consistency.

### Step 9: Basic LCEL Chaining
Create a simple chain: **Prompt → LLM → Output Parser**
```python
simple_chain = recommendation_prompt | llm | StrOutputParser()
result = simple_chain.invoke({"user_query": "..."})
```

### Step 10: Control Flow - RunnableBranch
Route to different chains based on user intent:
```python
router = RunnableBranch(
    (lambda x: "recommend" in x["user_query"].lower(), recommendation_chain),
    (lambda x: "compare" in x["user_query"].lower(), analysis_chain),
    recommendation_chain  # default
)
```

### Step 11: Generate-Refine Pipeline
Two-step process:
1. **Generate**: Initial recommendations using the prompt
2. **Refine**: Polish recommendations with formatting and details

```python
generate_refine_chain = (
    recommend_chain
    | (lambda x: {"recommendation": x})
    | refine_chain
)
```

### Step 12: Message History Memory
Multi-turn conversations with persistent memory:
```python
memory_chain = RunnableWithMessageHistory(
    conversational_chain,
    get_session_history,
    input_messages_key="user_query",
    history_messages_key="history"
)
```
The model remembers previous interactions within a session.

### Step 13: Serialization
Save and load chains:
```python
# Save
serialized = dumps(recommendation_prompt)
with open("book_chain_kaggle.json", "w") as f:
    f.write(serialized)

# Load
with open("book_chain_kaggle.json", "r") as f:
    loaded_serialized = f.read()
loaded_prompt = loads(loaded_serialized, allowed_objects="all")
loaded_chain = loaded_prompt | llm | StrOutputParser()
```

---

## 📁 Project Structure

```
book-recommendation-system/
├── README.md                           # This file
├── book_recommendation.ipynb           # Main Jupyter notebook
├── book_recommendation.py              # Python script version
├── book_chain_kaggle.json              # Serialized prompt
├── books_for_llm.csv                   # Sampled book catalog
├── data/
│   ├── Books.csv                       # Full book dataset
│   ├── Ratings.csv                     # Rating records
│   └── Users.csv                       # User information
└── docs/
    ├── README.txt                      # Original documentation
    ├── DATASETS_GUIDE.pdf              # Dataset details
    └── QUICK_REFERENCE.pdf             # Quick reference guide
```

---

## 🛠️ Usage

### Run Jupyter Notebook
```bash
jupyter notebook book_recommendation.ipynb
```
Execute cells sequentially to see each LangChain concept in action.

### Run Python Script
```bash
python book_recommendation.py
```

### Switch Models
In Cell 5, uncomment/comment different model options:
```python
# Option 1: OpenAI
model="openai:gpt-4o-mini"

# Option 2: Google Gemini
model="google_genai:gemini-2.5-flash-lite"

# Option 3: HuggingFace
model="huggingface_hub:meta-llama/Llama-2-7b-chat-hf"
```

---

## 🔑 Key Concepts Demonstrated

| Concept | Location | Purpose |
|---------|----------|---------|
| **Messages** | Step 6 | Structured conversation with roles |
| **Document Loader** | Step 7 | Load external data (CSV) |
| **Prompt Injection** | Step 8 | Embed context into prompts |
| **LCEL Chaining** | Step 9 | Compose modular pipelines |
| **Control Flow** | Step 10 | Route based on conditions |
| **Generate-Refine** | Step 11 | Multi-stage processing |
| **Memory/History** | Step 12 | Persistent conversation context |
| **Serialization** | Step 13 | Save/load chains |

---

## ⚙️ Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=sk-...

# Optional (for other providers)
GOOGLE_API_KEY=...
HUGGINGFACE_API_TOKEN=...
```

### Model Parameters
```python
llm = init_chat_model(
    model="openai:gpt-4o-mini",
    temperature=0.7,        # 0-1: Lower = deterministic, Higher = creative
    max_tokens=500          # Max response length
)
```

---

## 📊 Performance Notes

- **Dataset**: Sampled to 1000 books (from 271K) for demo purposes
- **Context Size**: ~500KB book catalog hardcoded into prompt
- **Response Time**: 2-5 seconds per request (depends on LLM)
- **Cost**: OpenAI free trial credits (~$18 value)

---

## 🐛 Troubleshooting

### Missing API Key
```
Error: Could not authenticate with OpenAI
```
**Solution**: Set `OPENAI_API_KEY` environment variable

### Module Import Error
```
ModuleNotFoundError: No module named 'langchain'
```
**Solution**: Run `pip install -r requirements.txt`

### CSV File Not Found
```
FileNotFoundError: data/Books.csv
```
**Solution**: Download Kaggle dataset and place in `data/` folder

### Rate Limit Error
```
RateLimitError: 429 Too Many Requests
```
**Solution**: Wait 1-2 minutes before retrying

---

## 📚 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Kaggle Book Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)
- [LCEL Tutorial](https://python.langchain.com/docs/expression_language/)

---

## ✅ Checklist for Running

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] OpenAI API key set (`export OPENAI_API_KEY=...`)
- [ ] Dataset files in `data/` folder
- [ ] Jupyter notebook installed (`pip install jupyter`)
- [ ] Start notebook: `jupyter notebook`

---

## 🎯 Next Steps

1. **Customize prompts**: Modify system messages in each step
2. **Add filters**: Implement book filtering by genre, year, etc.
3. **Integrate database**: Replace CSV with vector DB (Chroma, Pinecone)
4. **Deploy**: Create Flask/FastAPI endpoint
5. **Monitor**: Log and analyze model responses

---

## 📄 License

This project uses the Kaggle Book Recommendation Dataset. See [docs/DATASETS_GUIDE.pdf](docs/DATASETS_GUIDE.pdf) for dataset details.

---

## 📞 Support

For issues or questions:
1. Check [docs/README.txt](docs/README.txt)
2. Review [docs/QUICK_REFERENCE.pdf](docs/QUICK_REFERENCE.pdf)
3. Refer to LangChain docs: https://python.langchain.com/

---

**Last Updated**: May 28, 2026  
**LangChain Version**: 1.3+  
**Python Version**: 3.8+
