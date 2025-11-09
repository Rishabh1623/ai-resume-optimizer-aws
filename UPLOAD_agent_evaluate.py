"""
AGENTIC AI - EVALUATE: Score versions and select best
Optimized for minimal code size
"""
import json
import boto3
import os
import re

events = boto3.client('events')
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME', 'resume-optimizer-events')


def publish_event(detail_type, detail):
    """Publish event to EventBridge"""
    try:
        events.put_events(
            Entries=[{
                'Source': 'resume.optimizer',
                'DetailType': detail_type,
                'Detail': json.dumps(detail),
                'EventBusName': EVENT_BUS_NAME
            }]
        )
    except Exception as e:
        print(f"Event publish error: {e}")


def lambda_handler(event, context):
    """Evaluate: Agent scores its work"""
    print(f"📊 EVALUATE: Scoring versions...")
    
    versions = event.get('versions', [])
    job_desc = event.get('jobDescription', '')
    
    # Score each version
    scored = []
    for v in versions:
        content = v.get('content', '')
        
        # ATS score (keyword matching)
        job_words = set(re.findall(r'\b\w{4,}\b', job_desc.lower()))
        resume_words = set(re.findall(r'\b\w{4,}\b', content.lower()))
        keyword_match = len(job_words & resume_words) / len(job_words) if job_words else 0
        ats = int(50 + (keyword_match * 50))
        
        # Action verbs
        verbs = ['led', 'managed', 'developed', 'created', 'implemented', 'designed', 
                 'built', 'launched', 'achieved', 'improved', 'increased', 'reduced']
        action_count = sum(1 for v in verbs if v in content.lower())
        
        # Quantified achievements (numbers/metrics)
        metrics = len(re.findall(r'\d+%|\$\d+|\d+x|\d+\s*(hours?|users?)', content, re.I))
        
        # Overall score
        overall = (ats * 0.5 + keyword_match * 100 * 0.3 + 
                   min(action_count * 5, 100) * 0.1 + min(metrics * 10, 100) * 0.1)
        
        scored.append({
            **v,
            'score': {
                'overall': round(overall, 2),
                'ats': ats,
                'keywords': keyword_match,
                'actionVerbs': action_count,
                'achievements': metrics
            }
        })
    
    # Select best
    best = max(scored, key=lambda x: x['score']['overall'])
    
    evaluation = {
        'versions': scored,
        'bestVersion': best,
        'bestScore': best['score']['overall'],
        'bestApproach': best['approach'],
        'atsScore': best['score']['ats'],
        'keywordMatch': best['score']['keywords'],
        'actionVerbs': best['score']['actionVerbs'],
        'achievements': best['score']['achievements']
    }
    
    publish_event('EvaluationComplete', {
        'jobId': event.get('jobId'),
        'score': best['score']['overall']
    })
    
    print(f"✓ Best: {best['approach']} ({best['score']['overall']}/100)")
    return evaluation
