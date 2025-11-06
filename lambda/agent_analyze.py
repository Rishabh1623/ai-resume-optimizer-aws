"""
AGENTIC AI - PERCEIVE: Analyze resume and job description
Optimized for minimal code size
"""
import json
import boto3
import os
from agent_utils import invoke_bedrock, publish_event, extract_json

comprehend = boto3.client('comprehend')

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
    
    publish_event('AnalysisComplete', {'jobId': event.get('jobId'), 'jobType': job_type})
    
    print(f"✓ {len(gaps)} gaps, {len(matched)} matched, type: {job_type}")
    return analysis
