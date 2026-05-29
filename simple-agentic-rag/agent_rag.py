from langchain.tools import tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = OpenAIEmbeddings()

db = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

@tool
def search_docs(query: str) -> str:
    '''Search the knowledge base'''
    
    docs = db.similarity_search(query, k=2)

    return "\n".join(
        [doc.page_content for doc in docs]
    )

llm = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0
)

tools = [search_docs]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

while True:

    question = input("\nAsk question (type exit to quit): ")

    if question.lower() == "exit":
        break

    prompt = f"""
You are an intelligent Agentic RAG system.

Decide whether document retrieval is needed.

If needed, use the search_docs tool.

Question:
{question}
"""

    response = agent.invoke(prompt)

    print("\nAnswer:")
    print(response["output"])
