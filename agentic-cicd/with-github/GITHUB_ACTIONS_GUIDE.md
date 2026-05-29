# GitHub Actions AI CI/CD Toolkit

**Complete AI-powered CI/CD toolkit using GitHub Actions (NOT Jenkins).**

## 📦 Download: `ai-cicd-github.zip` (38 KB)

## 🎯 What's Inside

**5 complete GitHub Actions implementations:**

| # | Option | Cost | Setup | Best For |
|---|--------|------|-------|----------|
| 1️⃣ | **HuggingFace** | FREE | 5m | Production ✅ |
| 2️⃣ | **Claude** | $0.30/call | 5m | High accuracy |
| 3️⃣ | **Simple** | FREE | 3m | Learning |
| 4️⃣ | **Full System** | $0-100/mo | 10m | Enterprise |
| 5️⃣ | **RAG** | Variable | 15m | Knowledge |

## 📁 Structure

```
ai-cicd-github/
├── README.md                    # Start here!
├── hf/                          # 🆓 HuggingFace (FREE)
│   ├── .github/workflows/deploy.yml
│   ├── hf_agent.py
│   ├── test_hf_agent.py
│   ├── requirements-hf.txt
│   └── README.md
├── langchain/                   # 🧠 Claude
│   ├── .github/workflows/deploy.yml
│   ├── langchain_agent.py
│   ├── test_langchain_agent.py
│   ├── requirements-langchain.txt
│   └── README.md
├── simple/                      # ⚡ Simple
│   ├── .github/workflows/deploy.yml
│   ├── simple_agent.py
│   ├── test_agent.py
│   └── README.md
├── full-agents/                 # 🚀 Enterprise
│   ├── .github/workflows/deploy.yml
│   ├── cicd_agent.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── test_agent.py
│   └── README.md
└── rag/                         # 📚 RAG
    └── README.md
```

## ⚡ Quick Start (5 Minutes)

### Step 1: Extract Zip
```bash
unzip ai-cicd-github.zip
cd ai-cicd-github
```

### Step 2: Choose an Option
```bash
# Pick ONE:
cd hf/        # HuggingFace (recommended)
cd langchain/ # Claude
cd simple/    # No AI
cd full-agents/ # Enterprise
```

### Step 3: Setup Secrets
In your GitHub repo:
1. **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add your token:
   - HuggingFace: `HF_TOKEN=hf_...`
   - Claude: `ANTHROPIC_API_KEY=sk-...`

### Step 4: Copy Files
```bash
# Copy workflow to your repo
mkdir -p your-repo/.github/workflows
cp .github/workflows/deploy.yml your-repo/.github/workflows/

# Copy agent code
cp *_agent.py your-repo/
cp requirements*.txt your-repo/
```

### Step 5: Push & Watch
```bash
git add .github/ *_agent.py requirements*.txt
git commit -m "Add AI CI/CD"
git push
# Go to Actions tab in GitHub and watch! 🎉
```

## 🔑 GitHub Secrets

### For HuggingFace (FREE)
```
HF_TOKEN = hf_xxxxxxxxxxxx
SLACK_WEBHOOK = https://hooks.slack.com/...  (optional)
```

Get HF token: https://huggingface.co/settings/tokens

### For Claude
```
ANTHROPIC_API_KEY = sk-xxxxxxxxxxxx
SLACK_WEBHOOK = https://hooks.slack.com/...  (optional)
```

Get API key: https://console.anthropic.com/keys

### Setting Secrets via CLI
```bash
# Using GitHub CLI
gh secret set HF_TOKEN -b "hf_..."
gh secret set SLACK_WEBHOOK -b "https://hooks.slack.com/..."
```

## 📊 How It Works

```
Push to GitHub
    ↓
Actions workflow triggers (from .github/workflows/deploy.yml)
    ↓
[build-test-decide job]
  - Install dependencies
  - Build code
  - Run tests
  - Capture logs
    ↓
Call AI Agent with logs
    ↓
Agent analyzes using tools
    ↓
Decision: DEPLOY / HOLD / CANARY
    ↓
[deploy job - if DEPLOY]
  - Deploy to production
  - Slack notification
```

## 🎯 Examples

### Perfect Build ✅
```yaml
Tests: ✓ 145 passed
Build: 0 errors

Workflow: 
  Decision: DEPLOY
  Action: Deploy to production
```

### Failing Tests ❌
```yaml
Tests: ✗ 2 failed, 143 passed
Build: 0 errors

Workflow:
  Decision: HOLD
  Action: Slack message to dev
```

### Breaking Change ⚠️
```yaml
Tests: ✓ 145 passed
Change: schema migration

Workflow:
  Decision: CANARY
  Action: Deploy to 10%, monitor, then 100%
```

## 🔄 Workflow vs Jenkins

| Feature | GitHub Actions | Jenkins |
|---------|---|---|
| Setup | Built into GitHub | Separate server |
| Cost | FREE | Server cost |
| Secrets | Built-in management | Manual |
| Logs | GitHub UI | Web interface |
| Integration | Native to GitHub | Plugin-based |

**→ For GitHub repos, GitHub Actions is simpler!**

## 📋 Files in Each Option

### hf/ (HuggingFace - Recommended)
- `.github/workflows/deploy.yml` - GitHub Actions workflow
- `hf_agent.py` - Agent using HF API
- `test_hf_agent.py` - Test suite
- `requirements-hf.txt` - Dependencies
- `README.md` - Setup guide

### langchain/ (Claude)
- `.github/workflows/deploy.yml` - GitHub Actions workflow
- `langchain_agent.py` - Claude agent
- `test_langchain_agent.py` - Test suite
- `requirements-langchain.txt` - Dependencies
- `README.md` - Setup guide

### simple/ (No AI)
- `.github/workflows/deploy.yml` - GitHub Actions workflow
- `simple_agent.py` - Heuristic logic
- `test_agent.py` - Test suite
- `README.md` - Setup guide

### full-agents/ (Enterprise)
- `.github/workflows/deploy.yml` - Advanced workflow
- `cicd_agent.py` - Full agent
- `Dockerfile` - Container image
- `docker-compose.yml` - Local testing
- `test_agent.py` - Test suite
- `README.md` - Setup guide

## 🚀 Typical Workflow File

All options follow this pattern:

```yaml
name: AI Deploy

on:
  push:
    branches: [main, develop]

jobs:
  build-test-decide:
    runs-on: ubuntu-latest
    outputs:
      decision: ${{ steps.ai.outputs.decision }}

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
      
      - run: |
          npm install && npm run build
          npm test -- --watchAll=false
      
      - name: AI Decision
        id: ai
        run: |
          python3 *_agent.py \
            --branch "${{ github.ref_name }}" \
            --commit "$(git rev-parse --short HEAD)" \
            --message "$(git log -1 --pretty=%B)" \
            --build-log "$(cat build.log)" \
            --test-log "$(cat test.log)"

  deploy:
    needs: build-test-decide
    if: needs.build-test-decide.outputs.decision == 'DEPLOY'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying..."
```

## 🔧 Customization

### Change Build Command
```yaml
- run: |
    python -m pytest
    cargo build --release
```

### Add Docker Push
```yaml
- run: |
    docker build -t myapp:${{ github.sha }} .
    docker push myapp:${{ github.sha }}
```

### Change Deployment
```yaml
- run: |
    kubectl set image deployment/app \
      app=myapp:${{ github.sha }} -n production
```

### Add More Notifications
```yaml
- uses: slackapi/slack-github-action@v1.24.0
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {"text": "✅ Deployed!"}
```

## 📊 Cost Comparison

| Option | Monthly Cost | Setup | Accuracy |
|--------|---|---|---|
| HuggingFace | **$0** | 5m | 95% |
| Claude | ~$6-12 | 5m | 98% |
| Simple | **$0** | 3m | 85% |
| Full System | $0-100 | 10m | 98% |

## 🔐 Security

✅ Secrets are encrypted in GitHub
✅ Never commit tokens to repo
✅ Use GitHub Secrets UI for all sensitive data
✅ Review workflow changes in PRs
✅ Use branch protection rules

## 🆘 Common Issues

### "Secret not found"
→ Go to Settings → Secrets → Check name matches workflow

### "Workflow not triggering"
→ Make sure file is: `.github/workflows/deploy.yml`
→ File must be in main/develop branch

### "Agent script not found"
→ Make sure Python file is in repo root

### "Python not found"
→ Already handled: `uses: actions/setup-python@v4`

## 📈 Monitoring

1. Go to **Actions** tab in GitHub
2. Click your workflow run
3. Expand **build-test-decide** job
4. Click **AI Decision** step
5. See full logs and agent reasoning

## 📖 Documentation

- **This file** - Overview
- **ai-cicd-github/README.md** - Main guide
- **hf/README.md** - HuggingFace setup
- **langchain/README.md** - Claude setup
- **simple/README.md** - Simple setup
- **full-agents/README.md** - Enterprise setup

## 🎁 What You Get

✅ 5 complete implementations
✅ 5 GitHub Actions workflows
✅ 5 test suites
✅ Agent code (production-ready)
✅ Comprehensive documentation
✅ Docker support
✅ Slack integration examples
✅ Best practices

## 🚀 Next Steps

1. **Extract zip:** `unzip ai-cicd-github.zip`
2. **Read main README:** `cat ai-cicd-github/README.md`
3. **Pick an option:** `cd hf/` (recommended)
4. **Setup secrets:** GitHub Settings → Secrets
5. **Copy files:** `.github/workflows/deploy.yml` and agent code
6. **Push and watch:** Go to Actions tab
7. **Celebrate:** Your AI CI/CD is live! 🎉

---

**GitHub Actions is perfect for GitHub repos - no Jenkins server needed!** 🚀

Start with HuggingFace (completely free).
