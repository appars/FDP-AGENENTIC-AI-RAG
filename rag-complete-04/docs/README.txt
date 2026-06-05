# LangChain Book Recommendation System

## 📦 Package Contents

This zip file contains a complete, production-ready LangChain system for building book recommendations with model-agnostic setup.

### Files Included:

1. **book_recommendation.ipynb** (20 KB)
   - Full Jupyter notebook with sample data (10 books)
   - All 9 key LangChain concepts
   - Perfect for learning and experimentation

2. **book_recommendation_kaggle.ipynb** (21 KB)
   - Advanced notebook using real Kaggle dataset
   - 1000+ actual books from Kaggle
   - Production-ready examples

3. **book_recommendation.py** (12 KB)
   - Standalone Python script
   - Run directly: `python book_recommendation.py`
   - Demonstrates all concepts in sequence

4. **QUICK_REFERENCE.pdf** (5.8 KB)
   - Quick lookup guide for all concepts
   - Code patterns and examples
   - Debugging tips
   - Offline reference

5. **DATASETS_GUIDE.pdf** (7.2 KB)
   - Complete guide to public book datasets
   - 4 popular Kaggle datasets
   - Download instructions (3 methods)
   - Usage examples

---

## 🚀 Quick Start

### Option 1: Jupyter Notebook (Recommended for Learning)
```bash
jupyter notebook book_recommendation.ipynb
```

### Option 2: Python Script (Quick Demo)
```bash
# Install dependencies first
pip install langchain langchain-core langchain-openai langchain-google-genai python-dotenv pandas pydantic

# Run the script
python book_recommendation.py
```

### Option 3: Use Real Kaggle Data
1. Download dataset from: https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset
2. Extract books.csv, ratings.csv, users.csv
3. Run: `jupyter notebook book_recommendation_kaggle.ipynb`

---

## 📋 Setup Instructions

### 1. Install Python Packages
```bash
pip install langchain langchain-core langchain-openai langchain-google-genai langchain-huggingface python-dotenv pandas pydantic
```

### 2. Create .env File (For API Keys)
```bash
# Create a .env file in your project directory
echo "OPENAI_API_KEY=your_key_here" > .env
# OR for Google Gemini
echo "GOOGLE_API_KEY=your_key_here" > .env
# OR for HuggingFace
echo "HF_TOKEN=your_token_here" > .env
```

### 3. Get Your API Keys
- **OpenAI**: https://platform.openai.com/api-keys
- **Google Gemini**: https://aistudio.google.com/app/apikey
- **HuggingFace**: https://huggingface.co/settings/tokens

---

## 🎯 What You'll Learn

✅ **Messages** - Structured conversation management  
✅ **Document Loader** - Load CSV, PDF, and external data  
✅ **Document Injection** - Inject data into prompts  
✅ **Output Parser** - Structured JSON/object output  
✅ **LCEL Chaining** - Connect components with | operator  
✅ **Control Flow** - RunnableBranch for routing  
✅ **Generate-Refine** - Multi-step pipelines  
✅ **Message History** - Multi-turn conversations with memory  
✅ **Serialization** - Save & load chains as JSON  

---

## 🔄 Model Agnostic Setup

Change this ONE line to switch models:

```python
llm = init_chat_model(
    model="openai:gpt-4o-mini",  # ← Change this
    temperature=0.7
)
```

**Supported Models:**
- OpenAI: `"openai:gpt-4o-mini"` or `"openai:gpt-4"`
- Google Gemini: `"google_genai:gemini-2.5-flash-lite"`
- HuggingFace: `"huggingface:meta-llama/Llama-2-7b-chat"`

---

## 📊 Using Real Kaggle Dataset

The `book_recommendation_kaggle.ipynb` notebook includes:
- Instructions to download real Kaggle data
- Loading 271K+ books from real dataset
- Sampling top 1000 books for speed
- Full LangChain workflow with real data

**Download Dataset:**
```bash
# Method 1: Manual download from Kaggle
# https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset

# Method 2: Using Kaggle API
pip install kaggle
kaggle datasets download -d arashnic/book-recommendation-dataset
unzip book-recommendation-dataset.zip
```

---

## 💡 Key Features

✨ **Model Agnostic** - Switch between OpenAI, Gemini, HuggingFace  
✨ **Production Ready** - All concepts scale to real applications  
✨ **Well Documented** - Clear comments and guides  
✨ **Working Code** - Copy-paste ready, fully functional  
✨ **Real Data** - Option to use actual Kaggle dataset  
✨ **Comprehensive** - All major LangChain concepts covered  

---

## 📖 File Recommendations

**For Beginners:**
1. Read `QUICK_REFERENCE.pdf` (5 min)
2. Run `book_recommendation.ipynb` cell-by-cell
3. Modify examples to learn concepts

**For Production:**
1. Read `DATASETS_GUIDE.pdf` for data options
2. Use `book_recommendation_kaggle.ipynb` with real data
3. Adapt patterns for your use case

**For Quick Testing:**
1. Run `book_recommendation.py` script
2. Check output in terminal
3. Modify model string to try different providers

---

## 🔧 Troubleshooting

### Issue: Module not found
```bash
pip install langchain langchain-core langchain-openai python-dotenv pandas pydantic
```

### Issue: API Key not found
- Create `.env` file in your project directory
- Add your API key: `OPENAI_API_KEY=sk-...`
- Load with: `from dotenv import load_dotenv; load_dotenv()`

### Issue: Kaggle dataset encoding error
```python
# Use latin-1 encoding
pd.read_csv('books.csv', encoding='latin-1')
```

### Issue: Dataset too large
```python
# Sample the data
df = pd.read_csv('books.csv', nrows=1000, encoding='latin-1')
```

---

## 📚 Next Steps

1. **Master the Basics** - Run the simple notebook first
2. **Try Real Data** - Download Kaggle dataset and experiment
3. **Build Your System** - Adapt patterns for your use case
4. **Deploy** - Use LangChain patterns in production
5. **Optimize** - Add caching, logging, monitoring

---

## 🤝 Support Resources

- **LangChain Docs**: https://docs.langchain.com
- **Kaggle Datasets**: https://www.kaggle.com/datasets
- **API Documentation**:
  - OpenAI: https://platform.openai.com/docs
  - Google Gemini: https://ai.google.dev
  - HuggingFace: https://huggingface.co/docs

---

## 📝 License

These notebooks and scripts are provided as educational material for learning LangChain concepts.

---

## ✨ What's New

✅ **Model Agnostic** - Works with any LLM provider  
✅ **Real Dataset Support** - Kaggle integration included  
✅ **PDF Guides** - Professional reference documents  
✅ **Multiple Formats** - Notebooks, scripts, and guides  
✅ **Complete Examples** - All major concepts covered  

---

## 🎉 Get Started Now!

1. Extract this zip file
2. Install dependencies: `pip install -r requirements.txt` (or run the setup in first notebook cell)
3. Choose your starting point:
   - Learning: `book_recommendation.ipynb`
   - Quick Demo: `book_recommendation.py`
   - Production: `book_recommendation_kaggle.ipynb`
4. Set your API key in `.env`
5. Run and experiment!

Happy learning! 🚀

---

**Generated**: May 27, 2026  
**Version**: 1.0  
**LangChain**: Latest (as of generation date)
