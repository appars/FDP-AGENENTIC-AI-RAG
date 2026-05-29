# Agentic CI/CD with Jenkins + LangChain

## Setup

1. Install Jenkins
2. Create a pipeline job
3. Point to this repository

## Install Python dependencies

pip3 install -r requirements.txt

Set OpenAI API key:

export OPENAI_API_KEY=<your_key>

Run tests:

pytest > test-results.log || true

Run agent:

python3 ai_agent.py
