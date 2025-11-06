"""
AGENTIC AI - PLAN: Create optimization strategy
Optimized for minimal code size
"""
import boto3
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
events = boto3.client('events')

def lambda_handler(event, context):
    """Plan: Agent creates strategy"""
    print(f"🎯 PLAN: Creating strategy...")
    
    analysis = event.get('analysis', {})
    job_type = analysis.get('jobType', 'general')
    gaps = len(analysis.get('skillsGap', []))
    
    # Query memory for past successes
    table = dynamodb.Table(os.environ['AGENT_MEMORY_TABLE'])
    try:
        resp = table.query(
            IndexName='score-index',
            KeyConditionExpression='jobType = :jt AND successScore >= :s',
            ExpressionAttributeValues={':jt': job_type, ':s': Decimal('85')},
            Limit=5
        )
        past = [i['strategy'] for i in resp.get('Items', [])]
    except:
        past = []
    
    # AI decides strategy
    prompt = f"""Job: {job_type}, Gaps: {gaps}, Past: {','.join(past) or 'none'}
Choose ONE: keyword_optimization, achievement_focus, skills_emphasis, structure_improvement, balanced_approach
Return only the strategy name."""
    
    strategy = invoke_bedrock(prompt, 50, 0.3) or 'balanced_approach'
    strategy = strategy.strip().lower().replace(' ', '_')
    
    # Fallback logic
    if 'keyword' not in strategy and 'achievement' not in strategy and 'skills' not in strategy:
        strategy = 'skills_emphasis' if gaps > 10 else 'balanced_approach'
    
    plan = {
        'strategy': strategy,
        'jobType': job_type,
        'approaches': ['keywords', 'achievements', 'structure'],
        'successCriteria': {'atsScore': 85, 'keywordMatch': 0.8},
        'maxIterations': 3
    }
    
    publish_event('PlanCreated', {'jobId': event.get('jobId'), 'strategy': strategy})
    
    print(f"✓ Strategy: {strategy}")
    return plan
