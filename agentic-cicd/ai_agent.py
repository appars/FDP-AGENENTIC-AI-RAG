from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


@tool
def read_logs(log_path: str) -> str:
    """Read Jenkins test logs"""
    with open(log_path, "r") as f:
        return f.read()


@tool
def retry_recommendation(error_text: str) -> str:
    """Check whether retry is useful"""
    flaky_keywords = [
        "timeout",
        "connection",
        "network"
    ]

    for word in flaky_keywords:
        if word in error_text.lower():
            return "RETRY"

    return "STOP"

load_dotenv(override=True)

llm = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0
)

tools = [
    read_logs,
    retry_recommendation
]

agent = create_agent(
    model=llm,
    tools=tools
)

prompt = '''
You are a CI/CD agent.

1. Read test-results.log
2. Determine if deployment should:
   GO
   RETRY
   STOP

Rules:
- Test failures → STOP
- Network/timeout issue → RETRY
- Success → GO

Return only one word:
GO, RETRY, STOP
'''

if __name__ == "__main__":
    if not os.path.exists("test-results.log"):
        decision = "STOP"
        with open("decision.txt", "w") as f:
            f.write(decision)
        print("Agent Decision:", decision)
        raise SystemExit(0)

    response = agent.invoke({
        "messages": [{"role": "user", "content": prompt}]
    })

    decision = response["messages"][-1].content.strip()

    with open("decision.txt", "w") as f:
        f.write(decision)

    print("Agent Decision:", decision)