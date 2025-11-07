"""
AGENTIC AI - LEARN: Store successful strategies
Optimized for minimal code size
"""
import json
import boto3
import os
import time
from decimal import Decimal

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
events = boto3.client('events')


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
    """Learn: Store strategy in memory"""
    print(f"🧠 LEARN: Storing strategy...")
    
    # Support both jobId and execution_id
    job_id = event.get('jobId') or event.get('execution_id') or event.get('user_id', 'unknown')
    evaluation = event.get('evaluation', {})
    analysis = event.get('analysis', {})
    plan = event.get('plan', {})
    iteration = event.get('iteration', 1)
    
    best = evaluation.get('bestVersion', {})
    score = evaluation.get('bestScore', 0)
    
    # Store in memory if successful
    if score >= 85:
        memory_table = dynamodb.Table(os.environ['AGENT_MEMORY_TABLE'])
        try:
            memory_table.put_item(Item={
                'jobType': analysis.get('jobType', 'general'),
                'timestamp': int(time.time()),
                'strategy': plan.get('strategy', 'unknown'),
                'approach': best.get('approach', 'unknown'),
                'successScore': Decimal(str(score)),
                'context': {'gaps': len(analysis.get('skillsGap', [])), 'iterations': iteration},
                'ttl': int(time.time()) + (90 * 24 * 60 * 60)
            })
            print(f"✓ Stored in memory (score: {score})")
        except Exception as e:
            print(f"Memory error: {e}")
    
    # Save to S3
    output_key = f"optimized/{job_id}_optimized.txt"
    s3.put_object(
        Bucket=os.environ['OUTPUT_BUCKET'],
        Key=output_key,
        Body=best.get('content', '').encode('utf-8'),
        ContentType='text/plain'
    )
    
    # Update job status
    jobs_table = dynamodb.Table(os.environ['JOBS_TABLE'])
    jobs_table.update_item(
        Key={'jobId': job_id},
        UpdateExpression='SET #s = :s, #r = :r, #sc = :sc',
        ExpressionAttributeNames={'#s': 'status', '#r': 'result', '#sc': 'atsScore'},
        ExpressionAttributeValues={
            ':s': 'COMPLETED',
            ':r': output_key,
            ':sc': Decimal(str(score))
        }
    )
    
    # Send notification
    orig_score = analysis.get('originalScore', 65)
    sns.publish(
        TopicArn=os.environ['SNS_TOPIC_ARN'],
        Subject=f"Resume Optimized - Score: {score}/100",
        Message=f"""Resume Optimization Complete! 🎉

Job ID: {job_id}

Results:
Original Score: {orig_score}/100
Optimized Score: {score}/100
Improvement: +{score - orig_score} points

Keyword Match: {evaluation.get('keywordMatch', 0)*100:.1f}%
Action Verbs: {evaluation.get('actionVerbs', 0)}
Achievements: {evaluation.get('achievements', 0)}

Iterations: {iteration}
Approach: {best.get('approach', 'unknown')}
Job Type: {analysis.get('jobType', 'general')}

Download from S3: {output_key}

Powered by Agentic AI + AWS
"""
    )
    
    publish_event('OptimizationComplete', {
        'jobId': job_id,
        'score': score,
        'iterations': iteration
    })
    
    print(f"✓ Complete! Score: {score}, Iterations: {iteration}")
    return {'status': 'SUCCESS', 'jobId': job_id, 'score': score, 'outputKey': output_key}
