"""
API Handler - Triggers Agentic AI Workflow via Step Functions
"""
import json
import boto3
import os
import uuid
from datetime import datetime

stepfunctions = boto3.client('stepfunctions')
dynamodb = boto3.resource('dynamodb')
events = boto3.client('events')

STATE_MACHINE_ARN = os.environ['STATE_MACHINE_ARN']
JOBS_TABLE = os.environ['JOBS_TABLE']
EVENT_BUS_NAME = os.environ['EVENT_BUS_NAME']

jobs_table = dynamodb.Table(JOBS_TABLE)

def lambda_handler(event, context):
    """API Gateway handler"""
    
    http_method = event.get('httpMethod', '')
    path = event.get('path', '')
    
    if http_method == 'POST' and path == '/optimize':
        return handle_optimize(event)
    elif http_method == 'GET' and path == '/health':
        return handle_health()
    elif http_method == 'GET' and '/status/' in path:
        return handle_status(event)
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Not found'})
        }

def handle_optimize(event):
    """
    Handle resume optimization request
    Triggers Step Functions agentic workflow
    """
    try:
        body = json.loads(event.get('body', '{}'))
        
        job_id = str(uuid.uuid4())
        user_id = body.get('userId', 'anonymous')
        resume = body.get('resume', '')
        job_description = body.get('jobDescription', '')
        target_role = body.get('targetRole', 'Unknown')
        
        # Create job record
        jobs_table.put_item(
            Item={
                'jobId': job_id,
                'userId': user_id,
                'status': 'QUEUED',
                'targetRole': target_role,
                'createdAt': datetime.utcnow().isoformat(),
                'expiresAt': int(datetime.utcnow().timestamp()) + (30 * 24 * 60 * 60)
            }
        )
        
        # Start Step Functions execution (Agentic AI Workflow)
        stepfunctions.start_execution(
            stateMachineArn=STATE_MACHINE_ARN,
            name=f"job-{job_id}",
            input=json.dumps({
                'jobId': job_id,
                'userId': user_id,
                'resume': resume,
                'jobDescription': job_description,
                'targetRole': target_role
            })
        )
        
        # Publish event
        events.put_events(
            Entries=[{
                'Source': 'resume-optimizer.api',
                'DetailType': 'OptimizationRequested',
                'Detail': json.dumps({
                    'jobId': job_id,
                    'userId': user_id
                }),
                'EventBusName': EVENT_BUS_NAME
            }]
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'jobId': job_id,
                'status': 'QUEUED',
                'message': 'Agentic AI workflow started. The agent will autonomously optimize your resume.'
            })
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def handle_status(event):
    """Get job status"""
    try:
        path = event.get('path', '')
        job_id = path.split('/')[-1]
        
        response = jobs_table.get_item(Key={'jobId': job_id})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Job not found'})
            }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response['Item'], default=str)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def handle_health():
    """Health check endpoint"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'status': 'healthy',
            'service': 'resume-optimizer-agentic-ai',
            'features': [
                'Autonomous planning',
                'Iterative improvement',
                'Self-evaluation',
                'Learning from experience'
            ]
        })
    }
