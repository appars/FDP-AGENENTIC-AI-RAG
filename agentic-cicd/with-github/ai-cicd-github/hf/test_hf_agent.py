#!/usr/bin/env python3
"""
Test Hugging Face Decision Agent
Demonstrates the agent making decisions using free HF Inference API
"""

import json
import subprocess
import time
import os

test_scenarios = [
    {
        "name": "All tests pass - should DEPLOY",
        "data": {
            "branch": "main",
            "commit": "abc123",
            "message": "Fix user authentication flow",
            "build_log": """
                npm install
                npm run build
                Build successful - no errors or warnings detected
            """,
            "test_log": """
                Test Results:
                ✓ 145 unit tests PASS
                ✓ 32 integration tests PASS
                Coverage: 89%
                All tests completed successfully
            """
        }
    },
    {
        "name": "Test failures - should HOLD",
        "data": {
            "branch": "develop",
            "commit": "def456",
            "message": "Add payment gateway integration",
            "build_log": """
                npm install
                npm run build
                Build successful - no errors
            """,
            "test_log": """
                Test Results:
                ✓ 143 tests PASS
                ✗ FAIL: Payment webhook handler
                ✗ FAIL: API timeout in stripe integration
                2 tests failed
            """
        }
    },
    {
        "name": "Breaking schema change - CANARY",
        "data": {
            "branch": "main",
            "commit": "ghi789",
            "message": "Migration: Add users.phone_number column - BREAKING CHANGE",
            "build_log": """
                npm install
                npm run build
                Database migration prepared
                Build successful
            """,
            "test_log": """
                Test Results:
                ✓ 145 tests PASS
                ✓ Migration tests PASS
                Database schema validation: OK
            """
        }
    },
    {
        "name": "Hotfix for security",
        "data": {
            "branch": "main",
            "commit": "jkl012",
            "message": "HOTFIX: Security patch for SQL injection vulnerability in API",
            "build_log": """
                npm install
                npm run build
                Security scanning: No vulnerabilities detected
                Build successful
            """,
            "test_log": """
                Test Results:
                ✓ 50 smoke tests PASS
                Critical path tests: All pass
                Security tests: Pass
            """
        }
    },
    {
        "name": "Build compilation error",
        "data": {
            "branch": "feature/ui",
            "commit": "mno345",
            "message": "Redesign dashboard UI",
            "build_log": """
                npm install
                npm run build
                ERROR in src/components/Dashboard.tsx line 45:
                Type 'string' is not assignable to type 'number'
                ERROR: Compilation failed with 2 errors
            """,
            "test_log": "Tests not run - build failed"
        }
    }
]


def run_agent(scenario):
    """Run agent for a test scenario"""
    try:
        cmd = [
            "python3", "hf_agent.py",
            "--branch", scenario["data"]["branch"],
            "--commit", scenario["data"]["commit"],
            "--message", scenario["data"]["message"],
            "--build-log", scenario["data"]["build_log"],
            "--test-log", scenario["data"]["test_log"],
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            return {
                "error": f"Command failed: {result.stderr}",
                "passed": False
            }
        
        try:
            decision = json.loads(result.stdout)
            return {
                "decision": decision,
                "passed": True
            }
        except json.JSONDecodeError:
            return {
                "error": f"Invalid JSON response: {result.stdout}",
                "passed": False
            }
        
    except subprocess.TimeoutExpired:
        return {
            "error": "Timeout - HF API took too long",
            "passed": False
        }
    except Exception as e:
        return {
            "error": str(e),
            "passed": False
        }


def main():
    print("=" * 80)
    print("HUGGING FACE LANGCHAIN AGENT TEST SUITE")
    print("=" * 80)
    
    # Check HF token
    if not os.getenv("HF_TOKEN"):
        print("\n⚠️  HF_TOKEN not set!")
        print("\nTo use this agent:")
        print("1. Get free token from https://huggingface.co/settings/tokens")
        print("2. Export token: export HF_TOKEN=hf_...")
        print("3. Run tests: python3 test_hf_agent.py\n")
        return
    
    results = []
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\nTest {i}: {scenario['name']}")
        print("-" * 80)
        print(f"Branch: {scenario['data']['branch']}")
        print(f"Commit: {scenario['data']['message'][:60]}...")
        
        print("Calling Hugging Face agent...")
        
        result = run_agent(scenario)
        
        if not result["passed"]:
            print(f"❌ ERROR: {result['error']}")
            results.append({
                'test': scenario['name'],
                'decision': 'ERROR',
                'passed': False
            })
        else:
            decision = result["decision"]
            print(f"\n✓ Decision: {decision.get('decision')}")
            print(f"  Confidence: {decision.get('confidence', 0):.0%}")
            print(f"  Reasoning: {decision.get('reasoning', 'N/A')[:150]}...")
            
            if decision.get('risks'):
                print(f"  Risks: {', '.join(decision['risks'][:2])}")
            
            if decision.get('actions'):
                print(f"  Actions: {', '.join(decision['actions'][:2])}")
            
            results.append({
                'test': scenario['name'],
                'decision': decision.get('decision'),
                'confidence': decision.get('confidence', 0),
                'passed': True
            })
        
        time.sleep(2)  # Rate limit HF API
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for r in results if r['passed'])
    total = len(results)
    
    for r in results:
        status = "✓" if r['passed'] else "❌"
        conf = f" ({r['confidence']:.0%})" if r['passed'] else ""
        decision = r.get('decision', 'ERROR')
        print(f"{status} {r['test'][:50]:50} → {decision}{conf}")
    
    print(f"\nTests completed: {passed}/{total}")
    
    if passed > 0:
        print("\nDecision breakdown:")
        decisions = {}
        for r in results:
            if r['passed']:
                d = r['decision']
                decisions[d] = decisions.get(d, 0) + 1
        
        for decision, count in sorted(decisions.items()):
            print(f"  {decision}: {count}")


if __name__ == "__main__":
    main()
