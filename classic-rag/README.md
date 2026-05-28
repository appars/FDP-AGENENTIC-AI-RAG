# RAG Workshop Demo Notebooks
  
This repository contains demo notebooks designed for teaching the **fundamentals and practical implementation of Retrieval-Augmented Generation (RAG)**.

Each notebook walks through the full RAG pipeline in a clear, step-by-step manner, suitable for classroom demonstrations and workshops.

---
##  Prerequisites

- Basic understanding of Python
- Familiarity with NLP concepts (embeddings, similarity search)
- Introductory knowledge of Large Language Models (LLMs)
---
##  College Department RAG
 

This notebook demonstrates a **basic RAG system** using a fictional undergraduate department (DISE) as the knowledge source.

### What This Notebook Covers

- Document embedding using **SentenceTransformers** (`all-MiniLM-L6-v2`)
- Vector indexing with **FAISS** for fast similarity search
- Retrieval of relevant documents using **cosine similarity**
- Answer generation using **Llama 3.1-8B** via the Hugging Face Inference API
- End-to-end flow: query → retrieve → generate

### What it is not covered
- Vector database
- Data chunking
- UI
---
##  Scholarships RAG

This notebook demonstrates a **real-world RAG chatbot** built on scholarship data provided by the Government of India.

### Key Components and Workflow:

1.  **Dataset Loading**: The project utilizes a dataset of Indian government scholarships, sourced from scholarships.gov.in and made available on Hugging Face (`NetraVerse/indian-govt-scholarships`).

2.  **Data Chunking**: The raw text data from the scholarships is split into smaller, manageable chunks to improve the relevance and efficiency of information retrieval.
    
3.  **Vector Database**:  [Qdrant](https://www.google.com/url?q=https%3A%2F%2Fqdrant.tech%2F)  is employed as the vector database to store and manage the embeddings of these document chunks.
    
4.  **Embedding Generation**:  [SentenceTransformer](https://www.google.com/url?q=https%3A%2F%2Fwww.sbert.net%2F)  (`all-MiniLM-L6-v2`) is used to convert both the scholarship document chunks and user queries into dense vector representations (embeddings). This model maps sentences and paragraphs into a 384-dimensional vector space, enabling semantic similarity search.
    
5.  **Retrieval**: When a user poses a query, its embedding is generated and used to search the Qdrant vector database. The system retrieves the most semantically similar document chunks to the query.
    
6.  **Language Model (LLM)**:  [TinyLlama](https://www.google.com/url?q=https%3A%2F%2Fhuggingface.co%2FTinyLlama%2FTinyLlama-1.1B-Chat-v1.0)  is the chosen Large Language Model. It's a smaller, efficient model capable of generating coherent responses.
    
7.  **Response Generation (RAG)**: The retrieved document chunks are provided as context to TinyLlama. The LLM then generates a factual and relevant answer to the user's query, grounded in the provided scholarship information.
    
8.  **Interactive Interface**: The entire RAG pipeline is encapsulated within a  [Gradio](https://www.google.com/url?q=https%3A%2F%2Fwww.gradio.app%2F)  interface, allowing users to interact with the chatbot in real-time.

---
# License
This project is intended for **educational and academic use**.
