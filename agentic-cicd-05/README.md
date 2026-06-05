# Agentic CI/CD with Jenkins + LangChain

## Overview

This project runs a Jenkins pipeline that:
1. Installs dependencies
2. Builds Python code
3. Runs tests
4. Uses an LLM agent to analyze test output
5. Applies a deployment gate (`GO`, `RETRY`, `STOP`)
6. Deploys only when allowed by the gate

Pipeline definition: [Jenkinsfile](Jenkinsfile)

---

## Pre-step: Install Jenkins and Essential Plugins

Before running the pipeline, install Jenkins and add the essential plugins:

1. Install Jenkins on your machine or server
2. Open Jenkins and complete the initial setup
3. Install these essential plugins:
	- Pipeline
	- Git
	- Credentials Binding
	- Workspace Cleanup
	- Blue Ocean
4. Create a pipeline job and point it to this repository

---

## CI/CD Flow (Jenkins Stages)

### 1) Install Dependencies
- Creates virtual environment and installs packages from [requirements.txt](requirements.txt)

### 2) Build
- Compiles [app.py](app.py) using:
	- `venv/bin/python -m py_compile app.py`

### 3) Test
- Runs tests from [app.py](app.py) via `pytest app.py`
- Stores output in `test-results.log`

### 4) LangChain Agent Analysis
- Runs [ai_agent.py](ai_agent.py)
- Agent reads `test-results.log` and writes decision to `decision.txt`

### 5) Decision Gate
- Reads `agentic-cicd/decision.txt`
- Behavior:
	- `STOP` -> pipeline fails
	- `RETRY` -> reruns tests once
	- `GO` -> continues to deploy

### 6) Deploy
- Runs [deploy.sh](deploy.sh)

---

## What happens when AGENT says `RETRY` or `STOP`?

### If decision is `RETRY`
1. Jenkins enters the `if (decision == "RETRY")` block in [Jenkinsfile](Jenkinsfile)
2. Executes `retry(1)` block
3. Reruns `venv/bin/pytest app.py` once
4. If retry passes, pipeline continues to Deploy
5. If retry fails, pipeline fails

### If decision is `STOP`
1. Jenkins enters the `if (decision == "STOP")` block in [Jenkinsfile](Jenkinsfile)
2. Calls `error("LangChain blocked deploy")`
3. Pipeline is marked **FAILURE**
4. Deploy stage is skipped

---

## Secrets / Environment

The pipeline reads OpenAI key from Jenkins credentials:
- `OPENAI_API_KEY = credentials('OPENAI_API_KEY')` in [Jenkinsfile](Jenkinsfile)

Create Jenkins credential as:
- Type: **Secret text**
- ID: `OPENAI_API_KEY`

---

## Local Run (optional)

Install dependencies:

`pip3 install -r requirements.txt`

Run tests:

`pytest app.py > test-results.log || true`

Run agent:

`python3 ai_agent.py`
