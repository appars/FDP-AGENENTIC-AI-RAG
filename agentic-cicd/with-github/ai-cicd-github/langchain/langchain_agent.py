"""
LangChain-based Decision Agent for Jenkins CI/CD
Uses Claude to intelligently analyze build logs and decide deployments
"""

from flask import Flask, request, jsonify
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
import json
import os

app = Flask(__name__)

# Initialize LLM
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.3,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


# Define tools for the agent
@tool
def analyze_test_results(test_log: str) -> str:
    """Analyze test results from build log"""
    passed = test_log.count("PASS") + test_log.count("passed")
    failed = test_log.count("FAIL") + test_log.count("failed")
    return f"Test Results: {passed} passed, {failed} failed"


@tool
def analyze_build_errors(build_log: str) -> str:
    """Check for compilation/build errors"""
    errors = build_log.count("ERROR") + build_log.count("error")
    warnings = build_log.count("WARNING") + build_log.count("warning")
    return f"Build Issues: {errors} errors, {warnings} warnings"


@tool
def check_commit_message(commit_msg: str) -> str:
    """Analyze commit message for deployment context"""
    keywords = {
        "hotfix": "Emergency fix - expedite deployment",
        "breaking": "Breaking change - requires canary",
        "schema": "Database change - requires monitoring",
        "security": "Security fix - high priority",
        "docs": "Documentation only - safe to deploy",
    }
    
    found = [v for k, v in keywords.items() if k.lower() in commit_msg.lower()]
    return "; ".join(found) if found else "No special keywords detected"


@tool
def assess_deployment_risk(branch: str, commit_msg: str) -> str:
    """Assess overall deployment risk"""
    risk = "MEDIUM"
    reasons = []
    
    if branch != "main":
        risk = "HIGH"
        reasons.append("Not on main branch")
    
    if "breaking" in commit_msg.lower():
        risk = "HIGH"
        reasons.append("Breaking changes detected")
    
    if "hotfix" in commit_msg.lower():
        risk = "LOW"
        reasons.append("Hotfix - typically low risk")
    
    return f"Risk Level: {risk}. Reasons: {'; '.join(reasons)}"


# Create agent
tools = [analyze_test_results, analyze_build_errors, check_commit_message, assess_deployment_risk]
agent_executor = create_react_agent(llm, tools)


def get_deployment_decision(build_data):
    """
    Use LangChain agent to decide deployment.
    
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
    
    # Build prompt for agent
    prompt = f"""
You are a CI/CD deployment decision agent. Analyze this build and decide if we should deploy.

Build Information:
- Branch: {build_data.get('branch')}
- Commit: {build_data.get('commit_sha')}
- Message: {build_data.get('commit_message')}
- Build Number: {build_data.get('build_number')}

Build Log:
{build_data.get('build_log', '')[:1000]}

Test Log:
{build_data.get('test_log', '')[:1000]}

Task:
1. Use the tools to analyze test results, build errors, and commit message
2. Assess deployment risk
3. Decide: DEPLOY, HOLD, or CANARY
4. Provide confidence (0-1) and reasoning

Respond with ONLY a JSON object:
{{
  "decision": "DEPLOY" | "HOLD" | "CANARY",
  "confidence": 0.0-1.0,
  "reasoning": "Why this decision?",
  "risks": ["risk1", "risk2"],
  "actions": ["step1", "step2"]
}}
"""

    try:
        # Run agent
        result = agent_executor.invoke({"messages": [HumanMessage(content=prompt)]})
        
        # Extract final message
        final_message = result["messages"][-1].content
        
        # Try to parse JSON from response
        if "```json" in final_message:
            final_message = final_message.split("```json")[1].split("```")[0]
        elif "{" in final_message:
            final_message = final_message[final_message.find("{"):final_message.rfind("}")+1]
        
        decision = json.loads(final_message)
        
        return {
            "decision": decision.get("decision", "HOLD"),
            "confidence": decision.get("confidence", 0.5),
            "reasoning": decision.get("reasoning", "Agent analysis complete"),
            "risks": decision.get("risks", []),
            "actions": decision.get("actions", [])
        }
        
    except Exception as e:
        print(f"Agent error: {e}")
        return {
            "decision": "HOLD",
            "confidence": 0.0,
            "reasoning": f"Agent error: {str(e)}",
            "risks": ["Agent failed"],
            "actions": ["Review manually"]
        }


@app.route('/decide', methods=['POST'])
def decide():
    """Main endpoint for Jenkins to call"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            "decision": "HOLD",
            "confidence": 0.0,
            "reasoning": "No build data provided"
        }), 400
    
    decision = get_deployment_decision(data)
    
    print(f"Decision: {decision['decision']} (confidence: {decision['confidence']})")
    
    return jsonify(decision), 200


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    print("Starting LangChain Decision Agent on port 5002...")
    print("Jenkins will call: http://localhost:5002/decide")
    print("\nUsing Claude with tools:")
    print("  - analyze_test_results")
    print("  - analyze_build_errors")
    print("  - check_commit_message")
    print("  - assess_deployment_risk")
    app.run(host='0.0.0.0', port=5002, debug=True)
