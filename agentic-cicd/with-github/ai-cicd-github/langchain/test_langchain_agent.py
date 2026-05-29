#!/usr/bin/env python3
"""
Test LangChain Decision Agent
Shows Claude making deployment decisions using LangChain tools
"""

import requests
import json
import time

AGENT_URL = "http://localhost:5002"

test_scenarios = [
    {
        "name": "Perfect build - all tests pass",
        "data": {
            "branch": "main",
            "commit_sha": "abc123",
            "commit_message": "Fix user authentication flow",
            "build_number": 101,
            "build_log": """
                npm install
                npm run build
                Build successful
                No errors or warnings
            """,
            "test_log": """
                PASS: 145 unit tests
                PASS: 32 integration tests
                Coverage: 89%
                All tests passed
            """
        }
    },
    {
        "name": "Some test failures - should HOLD",
        "data": {
            "branch": "develop",
            "commit_sha": "def456",
            "commit_message": "Add payment integration with Stripe",
            "build_number": 102,
            "build_log": """
                npm install
                npm run build
                Build successful
            """,
            "test_log": """
                PASS: 143 tests
                FAIL: 2 tests - payment webhook failed
                FAIL: 1 test - API timeout
                3 tests failed
            """
        }
    },
    {
        "name": "Breaking schema change - CANARY deployment",
        "data": {
            "branch": "main",
            "commit_sha": "ghi789",
            "commit_message": "Migration: Add users.phone_number column - BREAKING CHANGE",
            "build_number": 103,
            "build_log": """
                npm install
                npm run build
                Database migration prepared
                Build successful
            """,
            "test_log": """
                PASS: 145 tests
                All tests passed
                Migration tests: PASS
            """
        }
    },
    {
        "name": "Hotfix for security issue",
        "data": {
            "branch": "main",
            "commit_sha": "jkl012",
            "commit_message": "HOTFIX: Security patch for SQL injection vulnerability",
            "build_number": 104,
            "build_log": """
                npm install
                npm run build
                Security scanning: No vulnerabilities
            """,
            "test_log": """
                PASS: 50 smoke tests
                Critical path tests: PASS
            """
        }
    },
    {
        "name": "Build errors - compilation failed",
        "data": {
            "branch": "feature/new-ui",
            "commit_sha": "mno345",
            "commit_message": "Redesign dashboard UI",
            "build_number": 105,
            "build_log": """
                npm install
                npm run build
                ERROR in src/components/Dashboard.tsx line 45:
                Type 'string' is not assignable to type 'number'
                ERROR: Compilation failed
            """,
            "test_log": "Tests not run - build failed"
        }
    },
    {
        "name": "Documentation only - safe to deploy",
        "data": {
            "branch": "main",
            "commit_sha": "pqr678",
            "commit_message": "Update README and API documentation",
            "build_number": 106,
            "build_log": """
                npm install
                npm run build
                No source code changes detected
                Build successful
            """,
            "test_log": """
                PASS: 145 tests
                All tests passed
            """
        }
    }
]


def test_agent():
    """Run all test scenarios against LangChain agent"""
    
    print("=" * 80)
    print("LANGCHAIN DECISION AGENT TEST SUITE")
    print("=" * 80)
    
    # Check if agent is running
    try:
        response = requests.get(f"{AGENT_URL}/health", timeout=5)
        print(f"\n✓ Agent is running at {AGENT_URL}\n")
    except Exception as e:
        print(f"\n✗ Agent not running at {AGENT_URL}")
        print("Start it with: python langchain_agent.py\n")
        return
    
    results = []
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\nTest {i}: {scenario['name']}")
        print("-" * 80)
        print(f"Branch: {scenario['data']['branch']}")
        print(f"Commit: {scenario['data']['commit_message'][:60]}...")
        
        try:
            print("Calling LangChain agent...")
            
            response = requests.post(
                f"{AGENT_URL}/decide",
                json=scenario['data'],
                timeout=60  # LLM might take time
            )
            
            decision = response.json()
            
            print(f"\n  Decision: {decision.get('decision')}")
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
            
        except requests.Timeout:
            print("  TIMEOUT - Agent taking too long (LLM response delay)")
            results.append({
                'test': scenario['name'],
                'decision': 'TIMEOUT',
                'passed': False
            })
        except Exception as e:
            print(f"  ERROR: {str(e)[:100]}")
            results.append({
                'test': scenario['name'],
                'decision': 'ERROR',
                'passed': False
            })
        
        time.sleep(1)  # Rate limiting
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for r in results if r['passed'])
    total = len(results)
    
    for r in results:
        status = "✓" if r['passed'] else "✗"
        conf = f" ({r['confidence']:.0%})" if r['passed'] else ""
        print(f"{status} {r['test'][:50]:50} → {r['decision']}{conf}")
    
    print(f"\nTests passed: {passed}/{total}")
    
    # Decision breakdown
    if any(r['passed'] for r in results):
        print("\nDecision breakdown:")
        decisions = {}
        for r in results:
            if r['passed']:
                d = r['decision']
                decisions[d] = decisions.get(d, 0) + 1
        
        for decision, count in sorted(decisions.items()):
            print(f"  {decision}: {count}")


if __name__ == "__main__":
    test_agent()
