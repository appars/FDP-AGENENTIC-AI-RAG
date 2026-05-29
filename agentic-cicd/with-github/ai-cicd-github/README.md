# AI-Powered CI/CD with GitHub Actions

**Build intelligent CI/CD pipelines using GitHub Actions and AI agents.**

Complete toolkit with 5 different implementations - pick what fits your needs.

## 🚀 Quick Start (5 Minutes)

### 1. Pick an Option

| Option | Cost | Best For |
|--------|------|----------|
| **HuggingFace** 🆓 | FREE | Production (recommended) |
| **Claude** 🧠 | $0.30/call | High accuracy |
| **Simple** ⚡ | FREE | Learning |
| **Full System** 🚀 | $0-100/mo | Enterprise |

### 2. Setup Secrets in GitHub

Go to **Settings → Secrets and variables → Actions**:

**For HuggingFace:**
```
HF_TOKEN = hf_...  # From huggingface.co/settings/tokens
SLACK_WEBHOOK = https://hooks.slack.com/...  # Optional
```

**For Claude:**
```
ANTHROPIC_API_KEY = sk-...  # From console.anthropic.com
SLACK_WEBHOOK = https://hooks.slack.com/...  # Optional
```

### 3. Copy Workflow File

Copy `.github/workflows/deploy.yml` from your chosen option to your repo:

```bash
# Choose one:

# Option 1: HuggingFace
cp -r hf/.github ./

# Option 2: Claude
cp -r langchain/.github ./

# Option 3: Simple
cp -r simple/.github ./

# Option 4: Full System
cp -r full-agents/.github ./
```

### 4. Copy Agent Code

Copy the agent to your repo root:

```bash
# Choose one:
cp hf/hf_agent.py ./
cp hf/requirements-hf.txt ./
# OR
cp langchain/langchain_agent.py ./
cp langchain/requirements-langchain.txt ./
# etc...
```

### 5. Push and Watch

```bash
git add .github/ *_agent.py requirements*.txt
git commit -m "Add AI-powered CI/CD"
git push
```

Go to **Actions** tab to watch it work! 🎉

## 📁 Directory Structure

```
Your Repo
├── .github/
│   └── workflows/
│       └── deploy.yml          # ← Workflow file (from chosen option)
├── hf_agent.py                 # ← Agent code (from chosen option)
├── requirements-hf.txt         # ← Dependencies
└── (your code...)
```

## 🎯 How It Works

### GitHub Push

```
Developer push → GitHub → Workflow triggers
                             ↓
                         Build & Test
                             ↓
                         AI Agent decides
                             ↓
                    DEPLOY / HOLD / CANARY
                             ↓
                  Deploy or Slack notification
```

### Workflow Steps

1. **Build** - Compile code
2. **Test** - Run test suite
3. **AI Decision** - Call agent with logs
4. **Deploy** - If decision == DEPLOY
5. **Monitor** - Check health (Full System only)
6. **Alert** - Slack notification

## 💡 Decision Examples

### Perfect Build ✅
```
Tests: ✓ 145 passed
Decision: DEPLOY (95%)
Action: Deploy to production immediately
```

### Failing Tests ❌
```
Tests: ✗ 2 failed, 143 passed
Decision: HOLD (88%)
Action: Slack message to developer
```

### Breaking Change ⚠️
```
Tests: ✓ 145 passed (breaking schema detected)
Decision: CANARY (87%)
Action: Deploy to 10% traffic first
```

## 📊 Workflow vs Jenkinsfile

### GitHub Actions (This Approach)
✅ Native to GitHub
✅ No separate server
✅ Easy secret management
✅ Built-in artifact storage
✅ Free for public repos
✅ 2,000 minutes/month free (private)

### Jenkins (Traditional)
✅ Powerful but needs server
✅ Good for on-prem

**→ GitHub Actions is simpler for GitHub repos!**

## 🔑 Setting Up Secrets

### GitHub UI

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add HF_TOKEN (or ANTHROPIC_API_KEY)
4. Click **Add secret**

### Via CLI

```bash
# Using GitHub CLI
gh secret set HF_TOKEN -b "hf_..."
gh secret set SLACK_WEBHOOK -b "https://hooks.slack.com/..."
```

### Via Script

```bash
#!/bin/bash
gh secret set HF_TOKEN -b "$HF_TOKEN"
gh secret set SLACK_WEBHOOK -b "$SLACK_WEBHOOK"
```

## 📝 Customizing Workflows

### Change Deployment Command

In `.github/workflows/deploy.yml`, find:

```yaml
- name: Deploy
  run: |
    echo "✓ Deploying to production"
    # Add your actual deploy command:
    # docker build -t myapp:${{ github.sha }} .
    # docker push myapp:${{ github.sha }}
    # kubectl set image deployment/app app=myapp:${{ github.sha }}
```

### Add Notifications

```yaml
- name: Notify Slack
  uses: slackapi/slack-github-action@v1.24.0
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {"text": "✅ Deployed: ${{ github.sha }}"}
```

### Add PR Comments

```yaml
- name: Comment on PR
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v6
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '✅ AI says: DEPLOY-SAFE'
      })
```

## 🔍 Debugging Workflow

### View Logs

1. Go to **Actions** tab
2. Click your workflow run
3. Click **build-test-decide** job
4. Expand any step to see output

### Common Issues

**Error: "HF_TOKEN not set"**
→ Add secret to GitHub Settings

**Error: "curl: command not found"**
→ Use `python3` instead or install curl

**Agent not being called**
→ Check `.github/workflows/deploy.yml` is in repo
→ Make sure Python version is 3.10+

### Manual Trigger

Test without pushing:

```yaml
on:
  workflow_dispatch:  # Allows manual trigger

jobs:
  build-test-decide:
    # ... rest of workflow
```

Then: **Actions** → **AI Deploy** → **Run workflow**

## 📦 Example Repo Layout

```
my-awesome-app/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   ├── test_main.py
│   └── test_utils.py
├── hf_agent.py                 # Agent code
├── requirements-hf.txt         # Agent dependencies
├── requirements.txt            # App dependencies
├── package.json
└── README.md
```

## 🌟 Features by Option

### HuggingFace (FREE)
- ✅ Completely free
- ✅ Fast enough (15-30s)
- ✅ Production quality
- ✅ Simple setup

### Claude
- ✅ Best accuracy
- ✅ Fast (5-10s)
- ✅ Excellent reasoning
- ✅ ~$0.30 per decision

### Simple
- ✅ No AI (heuristics)
- ✅ Instant (<1s)
- ✅ Good for learning
- ✅ No dependencies

### Full System
- ✅ Monitoring
- ✅ Auto-rollback
- ✅ Slack alerts
- ✅ Docker support
- ✅ Prometheus metrics

## 🚀 Deployment Strategies

The agent can recommend:

- **DEPLOY** - Direct to production
- **CANARY** - 10% traffic first, then full
- **HOLD** - Wait for developer fix
- **ROLLBACK** - Automated rollback on failure

## 📊 Comparison: GitHub Actions vs Jenkins

| Feature | GitHub Actions | Jenkins |
|---------|---|---|
| Setup | Native to GitHub | Separate server |
| Cost | Free (public) | Server cost |
| Secrets | Built-in | Manual |
| Logs | GitHub UI | Web interface |
| Learning curve | Low | Medium |
| Power | Good | Excellent |

**For GitHub repos, use GitHub Actions!** 🎯

## 🎁 What's Included

Per option:
- ✅ Workflow file (`.github/workflows/deploy.yml`)
- ✅ Agent code (`*_agent.py`)
- ✅ Test suite (`test_*.py`)
- ✅ Dependencies (`requirements*.txt`)
- ✅ Complete README

Total:
- 5 workflow files
- 5 agent implementations
- 5 test suites
- Comprehensive documentation

## 🔐 Security

### Secrets Best Practices

✅ Never commit secrets
✅ Use GitHub Secrets for sensitive data
✅ Rotate keys regularly
✅ Use specific scopes (read-only where possible)
✅ Audit access logs

### Workflows Best Practices

✅ Use `actions/checkout@v4` (latest)
✅ Pin action versions
✅ Limit access to main branch
✅ Review workflow changes in PRs
✅ Monitor workflow execution

## 📚 Next Steps

1. **Choose your option** (HuggingFace recommended)
2. **Copy workflow file** to `.github/workflows/`
3. **Copy agent code** to repo root
4. **Add secrets** to GitHub Settings
5. **Push code** and watch it work
6. **Monitor runs** in Actions tab
7. **Adjust** based on results

## 🆘 Need Help?

1. Check the README in your chosen option folder
2. Look at example workflow (already provided)
3. Check GitHub Actions docs: https://docs.github.com/en/actions
4. Review agent code comments
5. Check workflow logs for errors

## 📖 Documentation

- **This file** - Overview and setup
- **hf/README.md** - HuggingFace option
- **langchain/README.md** - Claude option
- **simple/README.md** - Simple option
- **full-agents/README.md** - Full system

---

**Ready to go?** Pick an option and copy the workflow! 🚀

All implementations are production-ready. Start with HuggingFace (free!).
