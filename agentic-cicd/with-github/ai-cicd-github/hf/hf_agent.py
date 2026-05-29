#!/usr/bin/env python3
"""
LangChain CI/CD Agent using Hugging Face Inference API (Free Tier)
No costs, no Claude API key needed - uses HF's free model serving
"""

import json
import sys
import argparse
from typing import Dict, Any

from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
import os

# Get HF token from environment
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    print(json.dumps({
        "decision": "HOLD",
        "confidence": 0.0,
        "reasoning": "HF_TOKEN environment variable not set. Get free token from https://huggingface.co/settings/tokens"
    }))
    sys.exit(1)

# Initialize HuggingFace LLM (free models via Inference API)
# Using Mistral-7B which is free and performant
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",  # Free model
    huggingfacehub_api_token=HF_TOKEN,
    task="text-generation",
    model_kwargs={
        "max_new_tokens": 512,
        "temperature": 0.3,
        "top_p": 0.9
    }
)


# Define tools for the agent
@tool
def analyze_test_results(test_log: str) -> str:
    """Analyze test results from build log"""
    passed = test_log.count("PASS") + test_log.count("passed")
    failed = test_log.count("FAIL") + test_log.count("failed")
    skipped = test_log.count("skip")
    return f"Test Results: {passed} passed, {failed} failed, {skipped} skipped"


@tool
def analyze_build_errors(build_log: str) -> str:
    """Check for compilation/build errors"""
    errors = build_log.count("ERROR") + build_log.count("error")
    warnings = build_log.count("WARNING") + build_log.count("warning")
    if errors == 0 and warnings == 0:
        return "Build Status: SUCCESS - No errors or warnings"
    return f"Build Status: {errors} errors, {warnings} warnings"


@tool
def check_commit_keywords(commit_msg: str) -> str:
    """Analyze commit message for deployment context"""
    keywords = {
        "hotfix": "Emergency fix - expedite deployment",
        "breaking": "Breaking change - requires canary strategy",
        "schema": "Database change - requires monitoring",
        "migration": "Database migration - requires caution",
        "security": "Security fix - high priority",
        "docs": "Documentation only - safe to deploy",
    }
    
    found = [v for k, v in keywords.items() if k.lower() in commit_msg.lower()]
    if found:
        return "Commit context: " + "; ".join(found)
    return "Commit context: Standard feature/bugfix"


@tool
def assess_risk_level(branch: str, test_count: int, has_errors: bool) -> str:
    """Assess overall deployment risk"""
    risk = "MEDIUM"
    reasons = []
    
    if branch != "main":
        risk = "HIGH"
        reasons.append("Not on main branch")
    else:
        reasons.append("On main branch - lower risk")
    
    if has_errors:
        risk = "HIGH"
        reasons.append("Build has errors")
    
    if test_count < 50:
        reasons.append("Low test coverage")
    elif test_count > 100:
        reasons.append("Good test coverage")
    
    return f"Risk Level: {risk}. Details: {'; '.join(reasons)}"


# Create agent with tools
tools = [
    analyze_test_results,
    analyze_build_errors,
    check_commit_keywords,
    assess_risk_level
]

agent_executor = create_react_agent(llm, tools)


def get_deployment_decision(build_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Use LangChain agent with Hugging Face to decide deployment.
    
    Args:
        build_data: {
            branch: str,
            commit_sha: str,
            commit_message: str,
            build_log: str,
            test_log: str,
            build_number: int
        }
    
    Returns:
        {
            decision: 'DEPLOY' | 'HOLD' | 'CANARY',
            confidence: float (0-1),
            reasoning: str,
            risks: [str],
            actions: [str]
        }
    """
    
    branch = build_data.get('branch', 'unknown')
    commit_sha = build_data.get('commit_sha', '')[:8]
    commit_msg = build_data.get('commit_message', '')
    build_log = build_data.get('build_log', '')
    test_log = build_data.get('test_log', '')
    
    # Build prompt for agent
    prompt = f"""You are a CI/CD deployment decision agent for software releases.

Build Information:
- Branch: {branch}
- Commit: {commit_sha}
- Message: {commit_msg}

Build Log Summary:
{build_log[:800]}

Test Log Summary:
{test_log[:800]}

Use the available tools to:
1. Analyze test results
2. Check for build errors
3. Extract deployment context from commit message
4. Assess overall risk

Then decide: Should we DEPLOY, use CANARY strategy, or HOLD for fixes?

Your decision criteria:
- DEPLOY: All tests pass + no errors + low risk
- CANARY: Tests pass but has breaking changes or database migrations
- HOLD: Tests fail OR has build errors

Respond with ONLY a valid JSON object (no markdown, no extra text):
{{
  "decision": "DEPLOY" or "CANARY" or "HOLD",
  "confidence": number between 0 and 1,
  "reasoning": "Brief explanation of decision",
  "risks": ["risk1", "risk2"],
  "actions": ["action1", "action2"]
}}"""

    try:
        # Run agent
        print(f"DEBUG: Calling HF agent for commit {commit_sha}...", file=sys.stderr)
        
        result = agent_executor.invoke({
            "messages": [HumanMessage(content=prompt)]
        })
        
        # Extract final message
        final_message = result["messages"][-1].content
        
        print(f"DEBUG: Agent response received", file=sys.stderr)
        
        # Extract JSON from response
        if "```json" in final_message:
            final_message = final_message.split("```json")[1].split("```")[0]
        elif "{" in final_message:
            start = final_message.find("{")
            end = final_message.rfind("}") + 1
            if start >= 0 and end > start:
                final_message = final_message[start:end]
        
        decision = json.loads(final_message)
        
        return {
            "decision": decision.get("decision", "HOLD"),
            "confidence": float(decision.get("confidence", 0.5)),
            "reasoning": decision.get("reasoning", "Analysis complete"),
            "risks": decision.get("risks", []),
            "actions": decision.get("actions", [])
        }
        
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON response: {e}", file=sys.stderr)
        return {
            "decision": "HOLD",
            "confidence": 0.3,
            "reasoning": f"Agent response parsing failed: {str(e)}",
            "risks": ["Agent response format error"],
            "actions": ["Review logs manually", "Check agent output"]
        }
    except Exception as e:
        print(f"ERROR: Agent error: {e}", file=sys.stderr)
        return {
            "decision": "HOLD",
            "confidence": 0.0,
            "reasoning": f"Agent error: {str(e)}. Make sure HF_TOKEN is set.",
            "risks": ["Agent failed"],
            "actions": ["Check HF_TOKEN", "Review manually"]
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--message", required=True)
    parser.add_argument("--build-log", default="")
    parser.add_argument("--test-log", default="")
    parser.add_argument("--build-number", type=int, default=0)
    
    args = parser.parse_args()
    
    build_data = {
        "branch": args.branch,
        "commit_sha": args.commit,
        "commit_message": args.message,
        "build_log": args.build_log,
        "test_log": args.test_log,
        "build_number": args.build_number
    }
    
    decision = get_deployment_decision(build_data)
    
    # Output JSON to stdout for Jenkins to parse
    print(json.dumps(decision))


if __name__ == "__main__":
    main()
