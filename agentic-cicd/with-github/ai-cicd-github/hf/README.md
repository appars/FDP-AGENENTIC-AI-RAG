# HuggingFace + GitHub Actions (FREE)

**Completely free AI-powered CI/CD using GitHub Actions and Hugging Face.**

## 🚀 Setup (5 Minutes)

### 1. Get Free HF Token

1. Go to https://huggingface.co/settings/tokens
2. Create new token with read access
3. Copy token (starts with `hf_...`)

### 2. Add GitHub Secret

1. Go to your repo
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `HF_TOKEN`
5. Value: `hf_...` (paste your token)
6. Click **Add secret**

### 3. Copy Workflow

Copy `.github/workflows/deploy.yml` from this folder to your repo:

```bash
mkdir -p .github/workflows
cp .github/workflows/deploy.yml your-repo/.github/workflows/
```

### 4. Copy Agent Code

```bash
cp hf_agent.py your-repo/
cp requirements-hf.txt your-repo/
```

### 5. Commit & Push

```bash
git add .github/ hf_agent.py requirements-hf.txt
git commit -m "Add AI-powered CI/CD with HuggingFace"
git push
```

### 6. Watch it Work!

Go to **Actions** tab in GitHub and watch your workflow run! ✨

## 📊 Workflow Overview

```
Push to main/develop
    ↓
GitHub Actions triggers
    ↓
[build-test-decide job]
  • Build your code
  • Run tests
  • Call hf_agent.py with results
    ↓
HuggingFace API (Mistral-7B)
    ↓
Agent analyzes using tools:
  • analyze_test_results()
  • analyze_build_errors()
  • check_commit_keywords()
  • assess_risk_level()
    ↓
Decision: DEPLOY / HOLD / CANARY
    ↓
[deploy job - if DEPLOY]
  • Deploy to production
  • Send Slack notification
```

## 🎯 Decisions

- **DEPLOY** - All tests pass, no errors → Deploy immediately
- **HOLD** - Tests failing → Slack message to developer
- **CANARY** - Breaking changes detected → Deploy to 10% first

Each includes confidence score and reasoning.

## 🔧 Customization

### Change Build/Test Commands

In `.github/workflows/deploy.yml`:

```yaml
- name: Build & Test
  run: |
    npm install && npm run build
    npm test -- --watchAll=false
```

Change to your commands:
```yaml
- name: Build & Test
  run: |
    python -m pytest
    cargo build --release
```

### Add Slack Notifications

Already included! Just add `SLACK_WEBHOOK` secret:

1. **Settings** → **Secrets** → **New secret**
2. Name: `SLACK_WEBHOOK`
3. Value: Your Slack webhook URL (from Slack API)

### Change Deployment Command

In `.github/workflows/deploy.yml`:

```yaml
- name: Deploy to production
  run: |
    docker build -t myapp:${{ github.sha }} .
    docker push myapp:${{ github.sha }}
    kubectl set image deployment/app app=myapp:${{ github.sha }}
```

## 📋 Files You Need

1. **.github/workflows/deploy.yml** - Workflow file (from this folder)
2. **hf_agent.py** - Agent code (in this folder)
3. **requirements-hf.txt** - Python dependencies (in this folder)

That's it! Everything else stays in your existing repo.

## 🧪 Test Locally

```bash
export HF_TOKEN=hf_...
pip install -r requirements-hf.txt
python3 test_hf_agent.py
```

See real decisions before deploying to GitHub!

## 💻 How Agents Works

The agent:
1. Receives build logs, test results, commit message
2. Calls tools to analyze data
3. Uses HuggingFace API (Mistral-7B)
4. Returns decision + confidence + reasoning

All free on HuggingFace Inference API tier!

## 📊 Cost

- **HuggingFace API**: FREE (rate-limited ~30 req/hour)
- **GitHub Actions**: FREE (2,000 minutes/month for private repos)
- **Total**: $0/month

Perfect for 50-100 builds/day!

## 🚀 Example Decision

```
Commit: "Fix user auth bug"
Tests: ✓ 145 passed, 0 failed
Build: 0 errors, 0 warnings

Agent thinks:
  "All tests pass, no errors, safe to deploy"

Decision: DEPLOY (confidence 95%)
Action: Workflow continues to deploy step
Result: Code goes to production ✅
```

## 🔍 Troubleshooting

### "HF_TOKEN not set"
→ Go to Settings → Secrets → Add HF_TOKEN

### "Agent script not found"
→ Make sure hf_agent.py is in repo root

### "pip: command not found"
→ Already handled in workflow with Python 3.10

### Workflow not triggered
→ Make sure workflow file is in `.github/workflows/deploy.yml`
→ File must be in main/develop branch

## 📈 Monitor Workflow

1. Go to **Actions** tab
2. Click the workflow run
3. Expand jobs to see logs
4. Click each step for details

Every decision is logged with full reasoning!

## 🎁 Bonus

- Complete test suite (5 scenarios)
- Well-commented agent code
- Slack integration
- GitHub Actions best practices

## 📖 More Info

- HuggingFace docs: https://huggingface.co/docs
- GitHub Actions: https://docs.github.com/actions
- LangChain: https://docs.langchain.com

---

**You're ready! Push your code and watch it go!** 🚀

Questions? Check the workflow logs in GitHub Actions tab.
