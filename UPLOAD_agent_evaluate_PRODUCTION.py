"""
AGENTIC AI - EVALUATE: Score versions and select best
PRODUCTION-READY VERSION with realistic scoring
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
        
        # PRODUCTION-READY SCORING ALGORITHM
        
        # 1. ATS Score - Keyword Matching (40% weight)
        # Filter out common words for better matching
        common_words = {'with', 'from', 'that', 'this', 'have', 'will', 'your', 'their', 
                       'about', 'which', 'when', 'where', 'what', 'been', 'were', 'said',
                       'each', 'them', 'than', 'some', 'into', 'only', 'over', 'such',
                       'just', 'also', 'very', 'well', 'back', 'good', 'much', 'work',
                       'year', 'make', 'most', 'many', 'more', 'time', 'role', 'team',
                       'using', 'based', 'across', 'within', 'through', 'under'}
        
        job_words = set(w for w in re.findall(r'\b\w{4,}\b', job_desc.lower()) 
                       if w not in common_words)
        resume_words = set(w for w in re.findall(r'\b\w{4,}\b', content.lower()) 
                          if w not in common_words)
        
        if job_words:
            keyword_match = len(job_words & resume_words) / len(job_words)
            # More realistic ATS scoring: 70-100 range
            ats = int(70 + (keyword_match * 30))
        else:
            keyword_match = 0.7
            ats = 85  # Default good score
        
        # 2. Action Verbs (20% weight) - Expanded list
        verbs = ['led', 'managed', 'developed', 'created', 'implemented', 'designed', 
                 'built', 'launched', 'achieved', 'improved', 'increased', 'reduced',
                 'architected', 'engineered', 'automated', 'optimized', 'delivered',
                 'established', 'spearheaded', 'drove', 'executed', 'collaborated',
                 'partnered', 'conducted', 'introduced', 'migrated', 'deployed',
                 're-architected', 'standardized', 'accelerated', 'enhanced']
        action_count = sum(1 for v in verbs if v in content.lower())
        action_score = min(action_count * 4, 100)  # Cap at 100
        
        # 3. Quantified Achievements (20% weight) - Enhanced detection
        metrics_patterns = [
            r'\d+[%x×]',  # 75%, 10x, 5×
            r'\$\d+[KMB]?',  # $100K, $5M
            r'\d+\+?\s*(?:years?|months?|weeks?)',  # 4+ years, 8 months
            r'\d+\+?\s*(?:users?|clients?|customers?)',  # 20+ clients
            r'\d+\s*(?:hours?|days?)',  # 30 hours
            r'(?:increased|reduced|improved|achieved|generated).*?\d+%',  # improved by 30%
        ]
        metrics = sum(len(re.findall(pattern, content, re.I)) for pattern in metrics_patterns)
        metrics_score = min(metrics * 6, 100)  # Cap at 100
        
        # 4. Professional Formatting (20% weight)
        format_score = 0
        # Check for key sections
        if re.search(r'(?:SUMMARY|PROFESSIONAL SUMMARY|PROFILE)', content, re.I):
            format_score += 25
        if re.search(r'(?:EXPERIENCE|PROFESSIONAL EXPERIENCE)', content, re.I):
            format_score += 25
        if re.search(r'(?:EDUCATION|CERTIFICATIONS)', content, re.I):
            format_score += 25
        if re.search(r'(?:SKILLS|TECHNICAL SKILLS)', content, re.I):
            format_score += 25
        
        # Calculate weighted overall score
        overall = (
            ats * 0.40 +           # ATS/Keywords: 40%
            action_score * 0.20 +  # Action Verbs: 20%
            metrics_score * 0.20 + # Achievements: 20%
            format_score * 0.20    # Formatting: 20%
        )
        
        scored.append({
            **v,
            'score': {
                'overall': round(overall, 2),
                'ats': ats,
                'keywords': round(keyword_match, 3),
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
