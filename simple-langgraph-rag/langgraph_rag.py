from typing import TypedDict

from langgraph.graph import StateGraph, END

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


# ----------------------
# State Definition
# ----------------------

class GraphState(TypedDict):
    question: str
    retrieved_docs: str
    answer: str


# ----------------------
# Load Vector Database
# ----------------------

embeddings = OpenAIEmbeddings()

db = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)


# ----------------------
# Node 1: Retrieve Docs
# ----------------------

def retrieve(state):

    question = state["question"]

    docs = db.similarity_search(
        question,
        k=2
    )

    retrieved_text = "\n".join(
        [doc.page_content for doc in docs]
    )

    print("\n[Retriever Node Executed]")

    return {
        "retrieved_docs": retrieved_text
    }


# ----------------------
# Node 2: Generate Answer
# ----------------------

llm = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0
)


def generate_answer(state):

    question = state["question"]
    docs = state["retrieved_docs"]

    prompt = f"""
Answer the question using the context below.

Context:
{docs}

Question:
{question}
"""

    response = llm.invoke(prompt)

    print("\n[Generator Node Executed]")

    return {
        "answer": response.content
    }


# ----------------------
# Build LangGraph
# ----------------------

graph = StateGraph(GraphState)

graph.add_node("retrieve", retrieve)
graph.add_node("generate_answer", generate_answer)

graph.set_entry_point("retrieve")

graph.add_edge(
    "retrieve",
    "generate_answer"
)

graph.add_edge(
    "generate_answer",
    END
)

app = graph.compile()


# ----------------------
# Run Application
# ----------------------

while True:

    question = input(
        "\nAsk Question (type exit to quit): "
    )

    if question.lower() == "exit":
        break

    result = app.invoke({
        "question": question
    })

    print("\nAnswer:")
    print(result["answer"])
