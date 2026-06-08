# pip install google-adk google-generativeai sentence-transformers faiss-cpu numpy

import os
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.genai import types

# ---------------------------------------------------
# 1. API Key
# ---------------------------------------------------

os.environ["GOOGLE_API_KEY"] = ""

# ---------------------------------------------------
# 2. Sample Department Documents
# ---------------------------------------------------

documents = [

    # Department overview
    "The Department of Quantum Engineering (DQE) has around 140 students and 20 professors, focusing on applied quantum computing and intelligent systems.",
    "Students can choose from 5 courses ranging from core subjects to electives and hands-on project work, with strong industry exposure.",
    "DQE offers a postgraduate module 'Foundations of Quantum AI' and an undergraduate elective 'Quantum Machine Learning' using IBM Qiskit and PennyLane.",
    "All students have access to cloud quantum hardware through IBM Quantum Network and Amazon Braket as part of their coursework.",
    # Quantum AI research
    "DQE's primary research focus is Quantum AI — the intersection of quantum computing and artificial intelligence.",
    "The Quantum AI Lab investigates Quantum Neural Networks (QNNs) using parameterized quantum circuits (PQCs) and collaborates with a national quantum computing centre on 20-qubit and 50-qubit processors.",
    "A key research thread is Quantum Reinforcement Learning (QRL), where quantum agents learn policies faster than classical counterparts on specific problem classes.",
    "Project QuLearn is DQE's flagship initiative building hybrid classical-quantum models for drug discovery and materials science."
]

# ---------------------------------------------------
# 3. Create Embeddings
# ---------------------------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)
doc_embeddings = embedding_model.encode(documents)

# ---------------------------------------------------
# 4. Create FAISS Index
# ---------------------------------------------------

dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(doc_embeddings))

# ---------------------------------------------------
# 5. Retrieval Function (RAG Tool)
# ---------------------------------------------------

def retrieve_context(query: str, top_k: int = 2):
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(
        np.array(query_embedding),
        top_k
    )

    retrieved_docs = [
        documents[i]
        for i in indices[0]
    ]

    return "\n".join(retrieved_docs)

# ---------------------------------------------------
# 6. Google ADK Agent
# ---------------------------------------------------

rag_agent = Agent(
    model="gemini-2.0-flash",
    name="quantum_rag_agent",
    instruction="""
You are a RAG assistant for the
Department of Quantum Engineering.

Answer ONLY using the provided context.

If information is unavailable,
say:
'I could not find this in the department documents.'
"""
)

runner = Runner(agent=rag_agent)

# ---------------------------------------------------
# 7. Ask Question
# ---------------------------------------------------

user_query = "What research happens in DQE?"
context = retrieve_context(user_query)
prompt = f"""
Context:
{context}
Question:
{user_query}
Answer using only the context.
"""

response = runner.run(
    user_id="student_1",
    session_id="session_1",
    new_message=types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    )
)

print(response)
