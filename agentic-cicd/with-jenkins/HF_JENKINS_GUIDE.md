# Hugging Face + Jenkins + LangChain CI/CD Pipeline

A **completely free CI/CD pipeline** using Hugging Face's free Inference API (no costs, no API charges).

## What You Get

- **LangChain agent** with ReAct pattern
- **Mistral 7B** LLM from Hugging Face (free model serving)
- **Jenkins pipeline** that makes deployment decisions
- **Zero costs** - HF free tier is rate-limited but sufficient for CI/CD

## Quick Start (10 minutes)

### Step 1: Get Free Hugging Face Token

1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Name: `jenkins-cicd`
4. Read permissions (only need to read models)
5. Copy the token

### Step 2: Set Environment Variable

```bash
export HF_TOKEN=hf_...your...token...here...
```

Or in Jenkins, add to System → System Configuration → Environment variables:
```
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx
```

### Step 3: Install Dependencies

```bash
pip install -r requirements-hf.txt
```

### Step 4: Test the Agent

```bash
python3 test_hf_agent.py
```

Expected output:
```
Test 1: All tests pass - should DEPLOY
  Calling Hugging Face agent...
  
  ✓ Decision: DEPLOY
    Confidence: 92%
    Reasoning: All 145 tests pass with 89% coverage. No build errors detected.
    
Test 2: Test failures - should HOLD
  
  ✓ Decision: HOLD
    Confidence: 88%
    Reasoning: Payment integration tests failing, requires developer fixes
```

### Step 5: Setup Jenkins

1. Create Jenkins Pipeline job
2. Point to your Git repo with Jenkinsfile-hf
3. Add environment variable: `HF_TOKEN=hf_...`
4. Done!

## How It Works

```
Developer Push → GitHub → Webhook → Jenkins
                                        ↓
                                  [Build & Test]
                                        ↓
                        Calls hf_agent.py with logs
                                        ↓
                        HuggingFace Inference API
                        (Mistral-7B, free tier)
                                        ↓
                        LangChain Agent + Tools:
                        • analyze_test_results()
                        • analyze_build_errors()
                        • check_commit_keywords()
                        • assess_risk_level()
                                        ↓
                        Claude decides: DEPLOY/HOLD/CANARY
                                        ↓
                        Jenkins deploys or notifies dev
```

## Files You Have

| File | Purpose |
|------|---------|
| **Jenkinsfile-hf** | Jenkins pipeline definition |
| **hf_agent.py** | LangChain agent using HF API |
| **test_hf_agent.py** | Test script (no Jenkins needed) |
| **requirements-hf.txt** | Python dependencies |
| **This guide** | Complete documentation |

## Understanding the Agent

The agent uses **ReAct pattern** (Reasoning + Acting):

### 1. Agent Receives Build Data
```python
{
  "branch": "main",
  "commit_sha": "abc123",
  "commit_message": "Fix auth bug",
  "build_log": "Build successful, no errors",
  "test_log": "✓ 145 passed, 0 failed"
}
```

### 2. Agent Thinks & Acts
Claude (via Mistral) thinks:
```
"I need to check the test results and build status.
Let me call analyze_test_results() and analyze_build_errors()"
```

Calls tools:
- `analyze_test_results(test_log)` → "145 passed, 0 failed"
- `analyze_build_errors(build_log)` → "0 errors, 0 warnings"
- `check_commit_keywords(message)` → "Standard feature/bugfix"
- `assess_risk_level(branch, tests, errors)` → "Risk: LOW"

### 3. Agent Decides
```json
{
  "decision": "DEPLOY",
  "confidence": 0.92,
  "reasoning": "All 145 tests pass with no build errors. Safe to deploy.",
  "risks": [],
  "actions": ["Deploy to production", "Monitor metrics"]
}
```

### 4. Jenkins Acts
```bash
# If DEPLOY:
kubectl set image deployment/app app=myapp:abc123 -n production

# If HOLD:
# Send Slack message: "Build failed - needs fixes"

# If CANARY:
# Deploy to 10% traffic first, monitor metrics
```

## Decision Examples

### Example 1: Perfect Build ✅

```
Commit: "Fix user profile endpoint"
Tests: ✓ 156 passed, 0 failed
Build: No errors

Agent Decision:
- Decision: DEPLOY (confidence 95%)
- Reasoning: "All tests pass, no errors, safe feature implementation"
- Actions: ["Deploy to production", "Monitor error rates"]

Jenkins: Deploys to production immediately
```

### Example 2: Failing Tests ❌

```
Commit: "Add payment integration"
Tests: ✗ 2 failed, 143 passed
Build: No errors

Agent Decision:
- Decision: HOLD (confidence 88%)
- Reasoning: "Payment tests failing, critical system needs stability"
- Risks: ["Test failures", "Payment system risk"]
- Actions: ["Notify developer", "Request test fixes"]

Jenkins: Sends message to developer, does NOT deploy
```

### Example 3: Breaking Schema Change ⚠️

```
Commit: "BREAKING: Add users.phone column"
Tests: ✓ 145 passed (migration tests included)
Build: No errors

Agent Decision:
- Decision: CANARY (confidence 87%)
- Reasoning: "Schema change detected, use careful rollout"
- Risks: ["Breaking database change", "Data migration risk"]
- Actions: ["Deploy to 10% canary", "Monitor database", "Gradual increase"]

Jenkins: Deploys to 10% of traffic, monitors for 5 min, then gradual rollout
```

### Example 4: Security Hotfix 🔒

```
Commit: "HOTFIX: SQL injection security patch"
Tests: ✓ 50 smoke tests passed
Build: Security scan clean

Agent Decision:
- Decision: DEPLOY (confidence 99%)
- Reasoning: "Critical security fix, expedite deployment"
- Actions: ["Immediate deployment", "Post-incident review"]

Jenkins: Fast-tracks to production, skips canary
```

## Tools the Agent Has

Each tool returns structured information that helps Claude decide:

```python
@tool
def analyze_test_results(test_log: str) -> str:
    """Count PASS/FAIL in test output"""
    # Returns: "145 passed, 2 failed, 5 skipped"

@tool
def analyze_build_errors(build_log: str) -> str:
    """Count ERROR/WARNING in build output"""
    # Returns: "3 errors, 1 warning"

@tool
def check_commit_keywords(commit_msg: str) -> str:
    """Find keywords: hotfix, breaking, schema, security, docs"""
    # Returns: "BREAKING CHANGE detected; Database migration"

@tool
def assess_risk_level(branch: str, test_count: int, has_errors: bool) -> str:
    """Overall risk assessment"""
    # Returns: "Risk: HIGH - on develop branch, low test coverage"
```

## Customizing the Agent

Add your own rules by adding tools. Example:

```python
@tool
def check_code_coverage(test_log: str) -> str:
    """Extract code coverage percentage"""
    # Claude will consider coverage in decisions
    
@tool
def query_production_metrics(metric: str) -> str:
    """Get current prod CPU, memory, error rate"""
    # Claude considers deployment impact
    
@tool
def analyze_security_scan(scan_log: str) -> str:
    """Check for vulnerabilities"""
    # Claude makes security-aware decisions
```

Then add to agent:
```python
tools = [
    analyze_test_results,
    analyze_build_errors,
    check_commit_keywords,
    assess_risk_level,
    check_code_coverage,           # Your tool
    query_production_metrics,       # Your tool
]
```

## Free Tier Details

**Hugging Face Inference API Free Tier:**
- Rate limit: ~30 requests/hour per model
- Models: Unlimited (free models available)
- Cost: **$0**
- Latency: 5-30 seconds per request (acceptable for CI/CD)

**For your use case:**
- 50 builds/day × 30 days = 1500 builds/month
- 1500 ÷ 30 requests/hour limit = ~2 requests/hour minimum
- **Plenty of headroom on free tier**

If you hit limits, upgrade to paid tier (cheap) or use local Ollama (completely free).

## Troubleshooting

**"HF_TOKEN not set"**
```bash
export HF_TOKEN=hf_...
python3 test_hf_agent.py
```

**"Rate limit exceeded"**
- Wait 1 hour, or
- Upgrade HF plan (very cheap), or
- Switch to local Ollama

**"Connection timeout"**
- HF API is down (rare), or
- Your network blocks it

**"Invalid JSON response"**
- Mistral model formatting issue
- Try reducing `max_new_tokens` to 256

## Comparison: Claude vs Hugging Face vs Ollama

| Feature | Claude | Hugging Face | Ollama |
|---------|--------|--------------|--------|
| Cost | $0.30/decision | Free (rate-limited) | Free (local) |
| Setup | API key | HF token | Download & run |
| Speed | ~5-10s | ~15-30s | ~30-60s (depends on hardware) |
| Complexity | Easy | Easy | Medium |
| Offline? | No | No | Yes |
| Best for | Production | Development/CI | Testing |

**Recommendation:** Start with Hugging Face (free, easy), upgrade to Claude if you need speed.

## Production Checklist

- [ ] Test locally with `python3 test_hf_agent.py`
- [ ] Set HF_TOKEN in Jenkins environment
- [ ] Create Jenkins job with Jenkinsfile-hf
- [ ] Add GitHub webhook
- [ ] Monitor first 10 builds
- [ ] Adjust prompt/tools based on results
- [ ] Set up Slack notifications (optional)
- [ ] Log all decisions
- [ ] Plan for rate limit (upgrade if needed)
- [ ] Create rollback procedure

## Next Steps

1. **Get HF token** - https://huggingface.co/settings/tokens
2. **Run tests locally** - `python3 test_hf_agent.py`
3. **Setup Jenkins** - Copy Jenkinsfile-hf
4. **Add webhook** - GitHub → Jenkins
5. **Monitor** - Watch decisions on first 10 builds
6. **Customize** - Add your own tools/logic
7. **Scale** - Upgrade HF plan if hitting rate limits

---

## Files Reference

**Jenkinsfile-hf**
```groovy
stage('HuggingFace AI Decision') {
    steps {
        script {
            def response = sh(
                script: 'python3 hf_agent.py --branch "${BRANCH}" ...',
                returnStdout: true
            ).trim()
            def decision = readJSON text: response
            // Deploy if decision is DEPLOY
        }
    }
}
```

**hf_agent.py**
```python
from langchain_huggingface import HuggingFaceEndpoint
from langgraph.prebuilt import create_react_agent

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    huggingfacehub_api_token=HF_TOKEN,
    task="text-generation"
)

agent_executor = create_react_agent(llm, tools)
decision = agent_executor.invoke({"messages": [HumanMessage(...)]})
```

**test_hf_agent.py**
```python
result = subprocess.run(
    ["python3", "hf_agent.py", "--branch", "main", ...],
    capture_output=True
)
decision = json.loads(result.stdout)
```

---

**Start here:**
```bash
export HF_TOKEN=hf_...
python3 test_hf_agent.py
```

You now have a **free, AI-powered CI/CD pipeline using Hugging Face**! 🚀

No costs, no credits, no limits (except rate limiting on free tier).
