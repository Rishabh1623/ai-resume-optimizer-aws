"""
AGENTIC AI - PLAN: Create optimization strategy
Optimized for minimal code size
"""
import json
import boto3
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
events = boto3.client('events')
bedrock = boto3.client('bedrock-runtime', region_name=os.environ.get('AWS_REGION', 'us-east-1'))


def invoke_bedrock(prompt, max_tokens=500, temperature=0.7):
    """Invoke Bedrock Claude model"""
    try:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}]
        })
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=body
        )
        result = json.loads(response['body'].read())
        return result['content'][0]['text']
    except Exception as e:
        print(f"Bedrock error: {e}")
        return None


def publish_event(detail_type, detail):
    """Publish event to EventBridge"""
    try:
        events.put_events(
            Entries=[{
                'Source': 'resume.optimizer',
                'DetailType': detail_type,
                'Detail': json.dumps(detail),
                'EventBusName': os.environ.get('EVENT_BUS_NAME', 'resume-optimizer-events')
            }]
        )
    except Exception as e:
        print(f"Event publish error: {e}")

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
