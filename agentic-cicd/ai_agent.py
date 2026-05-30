from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from tools import read_logs, retry_recommendation
from dotenv import load_dotenv
import os

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