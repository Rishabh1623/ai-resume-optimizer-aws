"""
AGENTIC AI - PERCEIVE: Analyze resume and job description
Optimized for minimal code size
"""
import json
import boto3
import os
import re

comprehend = boto3.client('comprehend')
events = boto3.client('events')
bedrock = boto3.client('bedrock-runtime', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

def invoke_bedrock(prompt, max_tokens=500):
    """Invoke Bedrock Claude model"""
    try:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
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

def extract_json(text):
    """Extract JSON array from text"""
    if not text:
        return []
    try:
        # Try direct parse
        return json.loads(text)
    except:
        # Extract JSON array from text
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
        return []

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
    """Perceive: Agent analyzes inputs"""
    print(f"🤖 PERCEIVE: Analyzing...")
    
    resume = event.get('resume', '')
    job_desc = event.get('jobDescription', '')
    
    # Extract skills using Bedrock
    skills_prompt = f"Extract skills from resume as JSON array: {resume[:2000]}"
    resume_skills = extract_json(invoke_bedrock(skills_prompt, 300) or '[]')
    
    # Extract requirements
    req_prompt = f"Extract requirements from job as JSON array: {job_desc[:2000]}"
    job_reqs = extract_json(invoke_bedrock(req_prompt, 300) or '[]')
    
    # Calculate gaps
    skills_set = set(str(s).lower() for s in resume_skills)
    reqs_set = set(str(r).lower() for r in job_reqs)
    gaps = list(reqs_set - skills_set)
    matched = list(skills_set & reqs_set)
    
    # Job type classification
    job_lower = job_desc.lower()
    job_type = ('technical' if any(w in job_lower for w in ['engineer', 'developer']) else
                'management' if any(w in job_lower for w in ['manager', 'director']) else
                'creative' if any(w in job_lower for w in ['design', 'ux']) else 'general')
    
    # Sentiment
    sentiment = comprehend.detect_sentiment(Text=resume[:5000], LanguageCode='en')
    
    # Initial score (simple keyword matching)
    keywords = job_lower.split()
    matches = sum(1 for w in keywords if w in resume.lower())
    score = min(100, int((matches / len(keywords)) * 100)) if keywords else 50
    
    analysis = {
        'resumeSkills': resume_skills[:20],  # Limit size
        'jobRequirements': job_reqs[:20],
        'skillsGap': gaps[:15],
        'matchedSkills': matched[:15],
        'jobType': job_type,
        'sentiment': sentiment['Sentiment'],
        'originalScore': max(50, score),
        'targetScore': 85
    }
    
    publish_event('AnalysisComplete', {'jobId': event.get('jobId', 'unknown'), 'jobType': job_type})
    
    print(f"✓ {len(gaps)} gaps, {len(matched)} matched, type: {job_type}")
    return analysis
