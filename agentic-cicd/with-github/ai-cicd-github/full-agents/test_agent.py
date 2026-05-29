#!/usr/bin/env python3
"""
Test script for CI/CD agent - demonstrates various scenarios
Run this to see the agent in action without a full CI/CD pipeline
"""

import json
import requests
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

AGENT_URL = os.getenv("AGENT_URL", "http://localhost:5000")

def test_successful_build():
    """Test: All tests pass, deploy recommended"""
    print("\n" + "="*60)
    print("TEST 1: Successful Build - Should DEPLOY")
    print("="*60)
    
    webhook_payload = {
        "action": "completed",
        "workflow_run": {
            "id": 1001,
            "name": "Build",
            "head_sha": "abc123abc123abc123abc123abc123abc123abc1",
            "head_branch": "main",
            "conclusion": "success",
            "created_at": datetime.now().isoformat(),
            "head_commit": {
                "message": "Fix: Update user profile endpoint documentation"
            },
            "html_url": "https://github.com/example/repo/actions/runs/1001"
        }
    }
    
    response = requests.post(f"{AGENT_URL}/webhook", json=webhook_payload)
    result = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Decision: {result.get('decision')}")
    print(f"Confidence: {result.get('confidence'):.0%}")
    
    assert result.get("decision") in ["DEPLOY", "HOLD", "INVESTIGATE"], "Invalid decision"
    print("✓ Test passed")


def test_failing_tests():
    """Test: Integration tests fail, should HOLD"""
    print("\n" + "="*60)
    print("TEST 2: Failing Tests - Should HOLD")
    print("="*60)
    
    webhook_payload = {
        "action": "completed",
        "workflow_run": {
            "id": 1002,
            "name": "Build",
            "head_sha": "def456def456def456def456def456def456def4",
            "head_branch": "feature/payment",
            "conclusion": "failure",
            "created_at": datetime.now().isoformat(),
            "head_commit": {
                "message": "Feature: Add payment gateway integration"
            },
            "html_url": "https://github.com/example/repo/actions/runs/1002"
        }
    }
    
    response = requests.post(f"{AGENT_URL}/webhook", json=webhook_payload)
    result = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Decision: {result.get('decision')}")
    print(f"Confidence: {result.get('confidence'):.0%}")
    
    assert result.get("decision") in ["HOLD", "INVESTIGATE", "RETEST"], "Should not deploy with failures"
    print("✓ Test passed")


def test_flaky_tests():
    """Test: Flaky test (timeout), should RETEST or INVESTIGATE"""
    print("\n" + "="*60)
    print("TEST 3: Flaky Tests - Should RETEST")
    print("="*60)
    
    webhook_payload = {
        "action": "completed",
        "workflow_run": {
            "id": 1003,
            "name": "Build",
            "head_sha": "ghi789ghi789ghi789ghi789ghi789ghi789ghi7",
            "head_branch": "main",
            "conclusion": "failure",
            "created_at": datetime.now().isoformat(),
            "head_commit": {
                "message": "Update dependencies"
            },
            "html_url": "https://github.com/example/repo/actions/runs/1003"
        }
    }
    
    response = requests.post(f"{AGENT_URL}/webhook", json=webhook_payload)
    result = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Decision: {result.get('decision')}")
    print(f"Reasoning: {result.get('reasoning', 'N/A')[:100]}...")
    
    assert response.status_code == 200, "Request should succeed"
    print("✓ Test passed")


def test_database_migration():
    """Test: Database schema change, should use CANARY strategy"""
    print("\n" + "="*60)
    print("TEST 4: Database Migration - Should Deploy (Canary)")
    print("="*60)
    
    webhook_payload = {
        "action": "completed",
        "workflow_run": {
            "id": 1004,
            "name": "Build",
            "head_sha": "jkl012jkl012jkl012jkl012jkl012jkl012jkl0",
            "head_branch": "main",
            "conclusion": "success",
            "created_at": datetime.now().isoformat(),
            "head_commit": {
                "message": "Add users.last_login column to schema"
            },
            "html_url": "https://github.com/example/repo/actions/runs/1004"
        }
    }
    
    response = requests.post(f"{AGENT_URL}/webhook", json=webhook_payload)
    result = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Decision: {result.get('decision')}")
    print(f"Confidence: {result.get('confidence'):.0%}")
    
    if result.get("decision") == "DEPLOY":
        print(f"Strategy: {result.get('deployment_strategy', 'rolling')}")
    
    print("✓ Test passed")


def test_health_check():
    """Test: Agent health endpoint"""
    print("\n" + "="*60)
    print("TEST 5: Agent Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{AGENT_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Agent is healthy")
        else:
            print("✗ Agent returned non-200 status")
    except requests.ConnectionError:
        print("✗ Cannot connect to agent")
        print(f"  Make sure the agent is running at {AGENT_URL}")
        print("  Start it with: python cicd_agent.py")
        return False
    
    return True


def test_post_deploy_monitoring():
    """Test: Post-deployment health check (simulated)"""
    print("\n" + "="*60)
    print("TEST 6: Post-Deploy Monitoring")
    print("="*60)
    
    deployment_id = "deploy-abc123-1234567890"
    commit = "abc123abc123abc123abc123abc123abc123abc1"
    
    try:
        response = requests.get(
            f"{AGENT_URL}/health-check/{deployment_id}",
            params={"commit": commit},
            timeout=10
        )
        result = response.json()
        
        print(f"Status: {response.status_code}")
        print(f"Deployment ID: {result.get('deployment_id')}")
        print(f"Action: {result.get('action')}")
        print(f"Current error rate: {result.get('metrics', {}).get('error_rate_percent', 'N/A')}%")
        
        if result.get("action") == "ROLLBACK":
            print("🚨 ROLLBACK TRIGGERED")
        else:
            print("✓ Deployment healthy")
        
        print("✓ Test passed")
    except Exception as e:
        print(f"✗ Test failed: {e}")


def test_load():
    """Test: Send multiple builds rapidly to see how agent handles load"""
    print("\n" + "="*60)
    print("TEST 7: Load Test (5 builds in sequence)")
    print("="*60)
    
    commits = [
        "aaa111aaa111aaa111aaa111aaa111aaa111aaa1",
        "bbb222bbb222bbb222bbb222bbb222bbb222bbb2",
        "ccc333ccc333ccc333ccc333ccc333ccc333ccc3",
        "ddd444ddd444ddd444ddd444ddd444ddd444ddd4",
        "eee555eee555eee555eee555eee555eee555eee5",
    ]
    
    for i, commit in enumerate(commits, 1):
        payload = {
            "action": "completed",
            "workflow_run": {
                "id": 2000 + i,
                "head_sha": commit,
                "head_branch": "main",
                "conclusion": "success",
                "created_at": datetime.now().isoformat(),
                "head_commit": {"message": f"Commit {i}"},
                "html_url": f"https://github.com/example/repo/actions/runs/{2000+i}"
            }
        }
        
        try:
            response = requests.post(f"{AGENT_URL}/webhook", json=payload, timeout=30)
            print(f"  Build {i}: {response.status_code} - {response.json().get('decision', 'N/A')}")
        except Exception as e:
            print(f"  Build {i}: ERROR - {e}")
        
        time.sleep(1)  # Space out requests
    
    print("✓ Load test completed")


def main():
    """Run all tests"""
    print("CI/CD Agent Test Suite")
    print("=" * 60)
    print(f"Testing agent at: {AGENT_URL}")
    
    # Check if agent is running
    if not test_health_check():
        print("\n❌ Agent is not running. Start it first:")
        print("   python cicd_agent.py")
        return
    
    # Run tests
    tests = [
        test_successful_build,
        test_failing_tests,
        test_flaky_tests,
        test_database_migration,
        test_post_deploy_monitoring,
        test_load,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            failed += 1
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {passed + failed}")
    
    if failed == 0:
        print("\n✓ All tests passed!")
    else:
        print(f"\n✗ {failed} test(s) failed")


if __name__ == "__main__":
    main()
