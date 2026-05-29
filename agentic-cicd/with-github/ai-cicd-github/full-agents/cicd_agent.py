"""
CI/CD Agent: LLM-powered deployment decision engine

This agent listens to build webhooks, analyzes logs and metrics,
and makes intelligent deployment decisions using Claude.

Features:
- Webhook integration (GitHub Actions, GitLab CI)
- Automated build/test log analysis
- Intelligent deployment risk assessment
- Automatic rollback on metric degradation
- Slack notifications for decisions
"""

import os
import json
import time
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

import anthropic
from flask import Flask, request, jsonify
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class DeploymentDecision(Enum):
    """Possible deployment decisions from the agent"""
    DEPLOY = "deploy"
    HOLD = "hold"  # Needs fixes first
    INVESTIGATE = "investigate"  # Unclear, needs human review
    ROLLBACK = "rollback"  # Post-deploy issue detected
    RETEST = "retest"  # Flaky test, retry


@dataclass
class PipelineContext:
    """Context about the current build/deployment"""
    branch: str
    commit_sha: str
    commit_message: str
    build_logs: str
    test_results: Dict[str, Any]
    current_metrics: Optional[Dict[str, float]] = None
    previous_version: Optional[str] = None
    
    def to_prompt(self) -> str:
        """Format context as a structured prompt for Claude"""
        prompt = f"""
Build Pipeline Analysis
=======================

Branch: {self.branch}
Commit: {self.commit_sha}
Message: {self.commit_message}

Test Results:
{json.dumps(self.test_results, indent=2)}

Build Logs (last 100 lines):
{self._get_log_tail()}

Current Production Metrics:
{json.dumps(self.current_metrics or {}, indent=2)}

Previous Version: {self.previous_version or "N/A"}
"""
        return prompt
    
    def _get_log_tail(self) -> str:
        """Get last 100 lines of logs"""
        lines = self.build_logs.split('\n')
        return '\n'.join(lines[-100:])


class DeploymentAgent:
    """AI agent for making deployment decisions"""
    
    def __init__(self, slack_webhook: Optional[str] = None):
        self.slack_webhook = slack_webhook or os.getenv("SLACK_WEBHOOK_URL")
        self.deployment_history = []
    
    def analyze_and_decide(self, context: PipelineContext) -> Dict[str, Any]:
        """
        Analyze pipeline context and make a deployment decision.
        Returns: {decision, reasoning, confidence, risks, action_plan}
        """
        logger.info(f"Analyzing build for commit {context.commit_sha[:8]}")
        
        # Build the analysis prompt
        analysis_prompt = f"""{context.to_prompt()}

TASK: You are a CI/CD deployment decision engine. Analyze this build carefully.

Respond with ONLY a JSON object (no markdown, no explanation):
{{
  "decision": "DEPLOY" | "HOLD" | "INVESTIGATE" | "ROLLBACK" | "RETEST",
  "confidence": 0.0-1.0,
  "reasoning": "Why did you make this decision?",
  "risks": ["risk1", "risk2", ...],
  "blockers": ["blocker1", "blocker2", ...],
  "action_plan": ["step1", "step2", ...],
  "deployment_strategy": "canary" | "rolling" | "full",
  "rollback_trigger": "error_rate > 1% OR latency_p99 > 500ms",
  "post_deploy_checks": ["check1", "check2", ...]
}}

Key decision criteria:
1. All unit & integration tests pass = good signal
2. Test flakiness or timeouts = investigate/retest
3. Build errors or warnings = hold
4. Production metrics degradation = consider rollback
5. High risk changes (schema, auth) = canary deployment
6. Low risk changes (docs, comments) = safe to deploy
"""
        
        try:
            # Call Claude to analyze
            message = client.messages.create(
                model="claude-opus-4-1",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": analysis_prompt}
                ]
            )
            
            response_text = message.content[0].text.strip()
            
            # Handle markdown code blocks
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            decision_data = json.loads(response_text)
            
            # Normalize decision value
            decision_data["decision"] = decision_data["decision"].upper()
            
            # Log the decision
            self._log_decision(context, decision_data)
            
            # Send notification
            self._notify_decision(context, decision_data)
            
            return decision_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response: {e}")
            return {
                "decision": "INVESTIGATE",
                "confidence": 0.5,
                "reasoning": "Failed to parse AI response, manual review needed",
                "risks": ["AI analysis failed"],
                "blockers": [],
                "action_plan": ["Review logs manually", "Check test results"],
            }
        except Exception as e:
            logger.error(f"Error calling Claude: {e}")
            return {
                "decision": "HOLD",
                "confidence": 0.3,
                "reasoning": f"API error: {str(e)}",
                "risks": ["API unavailable"],
                "blockers": [],
                "action_plan": ["Retry analysis", "Fallback to manual review"],
            }
    
    def post_deploy_monitor(self, 
                           commit_sha: str, 
                           deployment_id: str,
                           metrics: Dict[str, float],
                           baseline_metrics: Dict[str, float]) -> Optional[DeploymentDecision]:
        """
        Monitor post-deployment metrics and decide if rollback is needed.
        Returns: DeploymentDecision or None if all OK
        """
        logger.info(f"Monitoring deployment {deployment_id}")
        
        # Check for SLO breaches
        monitor_prompt = f"""
Post-Deployment Health Check
============================

Deployment ID: {deployment_id}
Commit: {commit_sha}

Current Metrics:
{json.dumps(metrics, indent=2)}

Baseline (pre-deployment):
{json.dumps(baseline_metrics, indent=2)}

Analyze the metrics. Respond with ONLY a JSON object:
{{
  "status": "HEALTHY" | "DEGRADED" | "CRITICAL",
  "issues": ["issue1", "issue2", ...],
  "slo_breaches": ["slo1", "slo2", ...],
  "rollback_recommended": true | false,
  "confidence": 0.0-1.0,
  "reasoning": "Why is the deployment healthy/degraded?"
}}

SLO Thresholds:
- Error rate: < 0.1%
- Latency p99: < 200ms
- Memory: < 80% utilization
"""
        
        try:
            message = client.messages.create(
                model="claude-opus-4-1",
                max_tokens=512,
                messages=[
                    {"role": "user", "content": monitor_prompt}
                ]
            )
            
            response_text = message.content[0].text.strip()
            
            # Clean up markdown if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            health_data = json.loads(response_text)
            
            if health_data.get("rollback_recommended"):
                logger.warning(f"ROLLBACK RECOMMENDED: {health_data['reasoning']}")
                self._notify_rollback(deployment_id, health_data)
                return DeploymentDecision.ROLLBACK
            
            return None
            
        except Exception as e:
            logger.error(f"Error monitoring deployment: {e}")
            return None
    
    def _log_decision(self, context: PipelineContext, decision: Dict[str, Any]):
        """Log decision to history"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "commit": context.commit_sha,
            "branch": context.branch,
            "decision": decision["decision"],
            "confidence": decision["confidence"],
            "reasoning": decision["reasoning"],
        }
        self.deployment_history.append(entry)
        logger.info(f"Decision: {decision['decision']} (confidence: {decision['confidence']})")
    
    def _notify_decision(self, context: PipelineContext, decision: Dict[str, Any]):
        """Send Slack notification of decision"""
        if not self.slack_webhook:
            return
        
        color_map = {
            "DEPLOY": "#36a64f",
            "HOLD": "#ff9900",
            "INVESTIGATE": "#0099ff",
            "ROLLBACK": "#ff0000",
            "RETEST": "#ffcc00",
        }
        
        payload = {
            "attachments": [
                {
                    "color": color_map.get(decision["decision"], "#cccccc"),
                    "title": f"CI/CD Decision: {decision['decision']}",
                    "fields": [
                        {
                            "title": "Branch",
                            "value": context.branch,
                            "short": True
                        },
                        {
                            "title": "Commit",
                            "value": context.commit_sha[:8],
                            "short": True
                        },
                        {
                            "title": "Confidence",
                            "value": f"{decision['confidence']:.0%}",
                            "short": True
                        },
                        {
                            "title": "Reasoning",
                            "value": decision["reasoning"],
                            "short": False
                        },
                        {
                            "title": "Risks",
                            "value": ", ".join(decision.get("risks", [])) or "None",
                            "short": False
                        },
                        {
                            "title": "Next Steps",
                            "value": "\n".join(decision.get("action_plan", [])),
                            "short": False
                        },
                    ]
                }
            ]
        }
        
        try:
            requests.post(self.slack_webhook, json=payload, timeout=5)
        except Exception as e:
            logger.error(f"Failed to send Slack notification: {e}")
    
    def _notify_rollback(self, deployment_id: str, health_data: Dict[str, Any]):
        """Send urgent rollback notification"""
        if not self.slack_webhook:
            return
        
        payload = {
            "attachments": [
                {
                    "color": "#ff0000",
                    "title": "🚨 AUTOMATIC ROLLBACK TRIGGERED",
                    "fields": [
                        {
                            "title": "Deployment ID",
                            "value": deployment_id,
                            "short": True
                        },
                        {
                            "title": "Status",
                            "value": health_data.get("status", "UNKNOWN"),
                            "short": True
                        },
                        {
                            "title": "Issues",
                            "value": "\n".join(health_data.get("issues", [])),
                            "short": False
                        },
                        {
                            "title": "SLO Breaches",
                            "value": "\n".join(health_data.get("slo_breaches", [])),
                            "short": False
                        },
                    ]
                }
            ]
        }
        
        try:
            requests.post(self.slack_webhook, json=payload, timeout=5)
        except Exception as e:
            logger.error(f"Failed to send rollback notification: {e}")


# Initialize agent
agent = DeploymentAgent()


@app.route("/webhook", methods=["POST"])
def github_webhook():
    """Handle GitHub Actions workflow completion webhook"""
    payload = request.json
    
    # Parse workflow conclusion
    if payload.get("action") != "completed":
        return jsonify({"status": "ignored"}), 200
    
    workflow_run = payload.get("workflow_run", {})
    if workflow_run.get("conclusion") not in ["success", "failure"]:
        return jsonify({"status": "skipped"}), 200
    
    # Extract context
    context = PipelineContext(
        branch=workflow_run.get("head_branch", "unknown"),
        commit_sha=workflow_run.get("head_sha", "unknown"),
        commit_message=workflow_run.get("head_commit", {}).get("message", ""),
        build_logs=_fetch_github_logs(payload),
        test_results={
            "status": workflow_run.get("conclusion", "unknown"),
            "run_id": workflow_run.get("id"),
            "url": workflow_run.get("html_url"),
            "timestamp": workflow_run.get("created_at"),
        },
        current_metrics=_fetch_production_metrics(),
    )
    
    # Analyze and decide
    decision = agent.analyze_and_decide(context)
    
    # Execute decision if DEPLOY
    if decision["decision"] == "DEPLOY":
        deployment_id = _trigger_deployment(context, decision)
        
        # Schedule post-deploy monitoring
        if deployment_id:
            _schedule_health_check(deployment_id, context.commit_sha)
    
    return jsonify({
        "status": "analyzed",
        "decision": decision["decision"],
        "confidence": decision["confidence"],
    }), 200


@app.route("/health-check/<deployment_id>", methods=["GET"])
def check_deployment_health(deployment_id: str):
    """Check health of a deployed version"""
    commit_sha = request.args.get("commit")
    
    current_metrics = _fetch_production_metrics()
    baseline_metrics = _fetch_baseline_metrics()
    
    result = agent.post_deploy_monitor(
        commit_sha or "unknown",
        deployment_id,
        current_metrics,
        baseline_metrics,
    )
    
    return jsonify({
        "deployment_id": deployment_id,
        "action": result.value if result else "CONTINUE_MONITORING",
        "metrics": current_metrics,
    }), 200


def _fetch_github_logs(payload: Dict[str, Any]) -> str:
    """Fetch GitHub Actions workflow logs"""
    # In production, use GitHub API with authentication
    # For demo, return simulated logs
    return """
2024-01-15 10:22:01 Starting build...
2024-01-15 10:22:15 Checked out commit abc123
2024-01-15 10:22:30 Installing dependencies...
2024-01-15 10:23:45 Dependencies installed successfully
2024-01-15 10:23:46 Running unit tests...
2024-01-15 10:24:12 ✓ 145 tests passed
2024-01-15 10:24:12 Running integration tests...
2024-01-15 10:26:30 ✓ 32 integration tests passed
2024-01-15 10:26:31 Building Docker image...
2024-01-15 10:27:45 Image built: myapp:abc123
2024-01-15 10:27:46 Scanning for vulnerabilities...
2024-01-15 10:28:00 ✓ No critical vulnerabilities
2024-01-15 10:28:01 Build successful!
"""


def _fetch_production_metrics() -> Dict[str, float]:
    """Fetch current production metrics"""
    # In production, query Prometheus, Datadog, or similar
    return {
        "error_rate_percent": 0.02,
        "latency_p99_ms": 145,
        "cpu_usage_percent": 62,
        "memory_usage_percent": 58,
        "requests_per_second": 1250,
        "deployment_version": "v1.2.3",
    }


def _fetch_baseline_metrics() -> Dict[str, float]:
    """Fetch baseline metrics from before deployment"""
    return {
        "error_rate_percent": 0.015,
        "latency_p99_ms": 138,
        "cpu_usage_percent": 60,
        "memory_usage_percent": 55,
        "requests_per_second": 1200,
    }


def _trigger_deployment(context: PipelineContext, decision: Dict[str, Any]) -> str:
    """Trigger actual deployment"""
    # In production, call your CD system (Argo CD, Spinnaker, etc.)
    deployment_id = f"deploy-{context.commit_sha[:8]}-{int(time.time())}"
    
    logger.info(f"Deployment triggered: {deployment_id}")
    logger.info(f"Strategy: {decision.get('deployment_strategy', 'rolling')}")
    
    # Simulate deployment
    return deployment_id


def _schedule_health_check(deployment_id: str, commit_sha: str):
    """Schedule periodic health checks"""
    # In production, use APScheduler or similar
    logger.info(f"Scheduled health checks for {deployment_id}")


if __name__ == "__main__":
    logger.info("Starting CI/CD Agent...")
    app.run(host="0.0.0.0", port=5000, debug=False)
