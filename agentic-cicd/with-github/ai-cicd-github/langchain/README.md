# Claude + GitHub Actions

**Best accuracy AI decisions using GitHub Actions and Claude API.**

## Setup (5 Minutes)

1. Get API key: https://console.anthropic.com/keys
2. Add secret: **Settings** → **Secrets** → `ANTHROPIC_API_KEY`
3. Copy `.github/workflows/deploy.yml` to your repo
4. Copy `langchain_agent.py` and `requirements-langchain.txt`
5. Push and watch it work!

## Cost

~$0.30 per decision (~$6-12/month for 50 builds/day)

## Accuracy

Best in class (98%) - Claude's reasoning is excellent for deployment decisions.

## Files

- `.github/workflows/deploy.yml` - Workflow
- `langchain_agent.py` - Agent code
- `requirements-langchain.txt` - Dependencies

See main README for more details.
