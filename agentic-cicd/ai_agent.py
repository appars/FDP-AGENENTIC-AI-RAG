from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from tools import read_logs, retry_recommendation

llm = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0
)

tools = [
    read_logs,
    retry_recommendation
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
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

response = agent.invoke(prompt)

decision = response["output"].strip()

with open("decision.txt", "w") as f:
    f.write(decision)

print("Agent Decision:", decision)
