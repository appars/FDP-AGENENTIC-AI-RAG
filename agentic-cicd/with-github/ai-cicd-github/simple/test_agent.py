#!/usr/bin/env python3
"""
Test the decision agent - shows what decisions it makes
Run WITHOUT Jenkins - just test the agent logic
"""

import json
import requests
import time

AGENT_URL = "http://localhost:5001"

test_cases = [
    {
        "name": "All tests pass - Should DEPLOY",
        "data": {
            "branch": "main",
            "commit_sha": "abc123abc123",
            "commit_message": "Fix user profile endpoint",
            "build_number": 101,
            "test_results": """
                ✓ Test 1: Login works
                ✓ Test 2: Signup works
                ✓ Test 3: API endpoints
                PASS: 145 tests
                FAIL: 0 tests
            """,
            "build_log": "Build successful, no errors"
        }
    },
    {
        "name": "Tests fail - Should HOLD",
        "data": {
            "branch": "feature/payment",
            "commit_sha": "def456def456",
            "commit_message": "Add Stripe payment gateway",
            "build_number": 102,
            "test_results": """
                ✓ Test 1: Login works
                ✗ Test 2: Payment flow broken
                ✗ Test 3: Webhook integration
                PASS: 143 tests
                FAIL: 2 tests
            """,
            "build_log": "Build successful, 2 test failures"
        }
    },
    {
        "name": "Compilation error - Should HOLD",
        "data": {
            "branch": "develop",
            "commit_sha": "ghi789ghi789",
            "commit_message": "Refactor database layer",
            "build_number": 103,
            "test_results": "Tests not run",
            "build_log": """
                Compiling...
                ERROR: SyntaxError in models.py line 45
                ERROR: Type mismatch in database.py
                Build FAILED
            """
        }
    },
    {
        "name": "Schema change - Should DEPLOY with CANARY",
        "data": {
            "branch": "main",
            "commit_sha": "jkl012jkl012",
            "commit_message": "Migration: Add users.phone_number column",
            "build_number": 104,
            "test_results": """
                ✓ Test 1: Old schema works
                ✓ Test 2: New schema works
                ✓ Test 3: Migration succeeds
                PASS: 145 tests
                FAIL: 0 tests
            """,
            "build_log": "Build successful, database schema change"
        }
    },
    {
        "name": "Hotfix on main - Should DEPLOY immediately",
        "data": {
            "branch": "main",
            "commit_sha": "mno345mno345",
            "commit_message": "Hotfix: Security patch for API",
            "build_number": 105,
            "test_results": """
                ✓ Test 1: Security check passed
                ✓ Test 2: API responds
                PASS: 50 tests (smoke tests only)
                FAIL: 0 tests
            """,
            "build_log": "Quick build for hotfix"
        }
    },
    {
        "name": "Warnings but passing - Should DEPLOY with caution",
        "data": {
            "branch": "main",
            "commit_sha": "pqr678pqr678",
            "commit_message": "Update dependencies",
            "build_number": 106,
            "test_results": """
                ✓ Test 1: All endpoints
                PASS: 145 tests
                FAIL: 0 tests
            """,
            "build_log": """
                Building...
                WARNING: Deprecated function used in auth.js
                WARNING: Unused variable in utils.js
                Build successful with warnings
            """
        }
    }
]


def test_agent():
    """Run all test cases against the agent"""
    
    print("=" * 80)
    print("DECISION AGENT TEST SUITE")
    print("=" * 80)
    
    # Check if agent is running
    try:
        response = requests.get(f"{AGENT_URL}/health", timeout=5)
        print(f"\n✓ Agent is running at {AGENT_URL}\n")
    except:
        print(f"\n✗ Agent not running at {AGENT_URL}")
        print("Start it with: python simple_agent.py\n")
        return
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['name']}")
        print("-" * 80)
        
        try:
            response = requests.post(
                f"{AGENT_URL}/decide",
                json=test['data'],
                timeout=10
            )
            
            decision = response.json()
            
            print(f"  Decision: {decision.get('decision')}")
            print(f"  Confidence: {decision.get('confidence', 0):.0%}")
            print(f"  Strategy: {decision.get('deployment_strategy', 'N/A')}")
            print(f"  Reason: {decision.get('reasoning', 'N/A')}")
            
            if decision.get('risks'):
                print(f"  Risks: {', '.join(decision['risks'])}")
            
            print()
            results.append({
                'test': test['name'],
                'decision': decision.get('decision'),
                'passed': True
            })
            
        except Exception as e:
            print(f"  ERROR: {e}\n")
            results.append({
                'test': test['name'],
                'decision': 'ERROR',
                'passed': False
            })
        
        time.sleep(0.5)
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for r in results if r['passed'])
    total = len(results)
    
    for r in results:
        status = "✓" if r['passed'] else "✗"
        print(f"{status} {r['test']}: {r['decision']}")
    
    print(f"\nPassed: {passed}/{total}")
    
    # Decision breakdown
    print("\nDecision breakdown:")
    decisions = {}
    for r in results:
        d = r['decision']
        decisions[d] = decisions.get(d, 0) + 1
    
    for decision, count in sorted(decisions.items()):
        print(f"  {decision}: {count}")


if __name__ == "__main__":
    test_agent()
