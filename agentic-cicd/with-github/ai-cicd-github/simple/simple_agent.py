#!/usr/bin/env python3
"""
Simple Decision Agent for Jenkins
Lightweight agent that analyzes build logs and decides: DEPLOY or HOLD
"""

from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

def analyze_build(data):
    """
    Analyze build data and make a decision.
    Simple heuristics - no LLM needed for basic cases.
    """
    
    branch = data.get('branch', 'unknown')
    commit_msg = data.get('commit_message', '').lower()
    test_results = data.get('test_results', '')
    build_log = data.get('build_log', '')
    
    decision = {
        'decision': 'HOLD',
        'confidence': 0.5,
        'reasoning': 'Default hold',
        'deployment_strategy': 'rolling',
        'risks': [],
        'action': 'Review manually'
    }
    
    # Count test results
    passed = len(re.findall(r'✓|PASS|passed', test_results, re.IGNORECASE))
    failed = len(re.findall(r'✗|FAIL|failed', test_results, re.IGNORECASE))
    
    # Check for errors in build log
    errors = len(re.findall(r'error|fatal|exception', build_log, re.IGNORECASE))
    warnings = len(re.findall(r'warning|warn', build_log, re.IGNORECASE))
    
    # Signal: All tests pass, no errors
    if passed > 0 and failed == 0 and errors == 0:
        decision['decision'] = 'DEPLOY'
        decision['confidence'] = 0.95
        decision['reasoning'] = f'All {passed} tests passed, no build errors'
        decision['deployment_strategy'] = 'rolling'
        
        # Check for risky changes
        if any(risk in commit_msg for risk in ['schema', 'migration', 'breaking']):
            decision['deployment_strategy'] = 'canary'
            decision['risks'].append('Breaking change detected')
            decision['confidence'] = 0.85
            decision['reasoning'] = f'All tests pass but breaking change - use canary'
    
    # Signal: Some tests fail
    elif failed > 0:
        decision['decision'] = 'HOLD'
        decision['confidence'] = 0.9
        decision['reasoning'] = f'{failed} tests failed, {passed} passed. Developer needs to fix.'
        decision['risks'].append(f'{failed} test failures')
    
    # Signal: Build errors
    elif errors > 0:
        decision['decision'] = 'HOLD'
        decision['confidence'] = 0.95
        decision['reasoning'] = f'Build has {errors} errors. Check compilation/syntax.'
        decision['risks'].append(f'{errors} build errors')
    
    # Signal: Only warnings
    elif warnings > 0:
        decision['decision'] = 'DEPLOY'
        decision['confidence'] = 0.7
        decision['reasoning'] = f'{warnings} warnings but no errors - safe to deploy'
        decision['risks'].append(f'{warnings} build warnings')
    
    # Hotfix on main branch
    if branch == 'main' and 'hotfix' in commit_msg:
        decision['decision'] = 'DEPLOY'
        decision['confidence'] = 0.95
        decision['reasoning'] = 'Hotfix on main branch - expedited'
        decision['deployment_strategy'] = 'rolling'
    
    return decision


@app.route('/decide', methods=['POST'])
def get_decision():
    """
    Main endpoint: Jenkins calls this with build data.
    Returns deployment decision.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'decision': 'HOLD',
                'confidence': 0.0,
                'reasoning': 'No data provided'
            }), 400
        
        decision = analyze_build(data)
        
        # Log decision
        print(f"Decision for {data.get('commit_sha', 'unknown')}: {decision['decision']}")
        
        return jsonify(decision), 200
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'decision': 'HOLD',
            'confidence': 0.0,
            'reasoning': f'Agent error: {str(e)}'
        }), 500


@app.route('/deployment', methods=['POST'])
def record_deployment():
    """
    Jenkins calls this after successful deployment.
    For tracking and monitoring.
    """
    try:
        data = request.get_json()
        print(f"Deployment recorded: {data.get('commit_sha')} on {data.get('branch')}")
        return jsonify({'status': 'recorded'}), 200
    except:
        return jsonify({'status': 'error'}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    print("Starting Decision Agent on port 5001...")
    print("Jenkins will call: http://localhost:5001/decide")
    app.run(host='0.0.0.0', port=5001, debug=True)
