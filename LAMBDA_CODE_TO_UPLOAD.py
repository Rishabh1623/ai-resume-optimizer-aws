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
    print(f"Event received: {json.dumps(event)}")
    
    # Get resume and job description - they might be in different keys
    resume = event.get('resume', event.get('resumeText', ''))
    job_desc = event.get('jobDescription', event.get('jobDescriptionText', ''))
    
    # If still empty, try to read from S3
    if not resume and event.get('resume_key'):
        s3 = boto3.client('s3')
        textract = boto3.client('textract')
        bucket = event.get('bucket', os.environ.get('INPUT_BUCKET'))
        resume_key = event['resume_key']
        
        print(f"DEBUG: Attempting to read resume from S3")
        print(f"DEBUG: Bucket = {bucket}")
        print(f"DEBUG: Key = {resume_key}")
        
        try:
            # First check if file exists
            s3.head_object(Bucket=bucket, Key=resume_key)
            print(f"✓ Resume file exists in S3")
            
            # Check if PDF - use Textract
            if resume_key.lower().endswith('.pdf'):
                print(f"Extracting PDF with Textract: {resume_key}")
                response = textract.detect_document_text(
                    Document={'S3Object': {'Bucket': bucket, 'Name': resume_key}}
                )
                resume = '\n'.join([
                    block['Text'] for block in response.get('Blocks', [])
                    if block['BlockType'] == 'LINE'
                ])
            else:
                # Text file - read directly
                response = s3.get_object(Bucket=bucket, Key=resume_key)
                resume = response['Body'].read().decode('utf-8')
            
            print(f"✓ Loaded resume from S3: {len(resume)} chars")
        except Exception as e:
            print(f"❌ Error reading resume from S3: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
    
    if not job_desc and event.get('job_description_key'):
        s3 = boto3.client('s3')
        textract = boto3.client('textract')
        bucket = event.get('bucket', os.environ.get('INPUT_BUCKET'))
        jd_key = event['job_description_key']
        
        print(f"DEBUG: Attempting to read JD from S3")
        print(f"DEBUG: Bucket = {bucket}")
        print(f"DEBUG: Key = {jd_key}")
        
        try:
            # First check if file exists
            s3.head_object(Bucket=bucket, Key=jd_key)
            print(f"✓ JD file exists in S3")
            
            # Check if PDF - use Textract
            if jd_key.lower().endswith('.pdf'):
                print(f"Extracting PDF with Textract: {jd_key}")
                response = textract.detect_document_text(
                    Document={'S3Object': {'Bucket': bucket, 'Name': jd_key}}
                )
                job_desc = '\n'.join([
                    block['Text'] for block in response.get('Blocks', [])
                    if block['BlockType'] == 'LINE'
                ])
            else:
                # Text file - read directly
                response = s3.get_object(Bucket=bucket, Key=jd_key)
                job_desc = response['Body'].read().decode('utf-8')
            
            print(f"✓ Loaded job description from S3: {len(job_desc)} chars")
        except Exception as e:
            print(f"❌ Error reading job description from S3: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
    
    # Validate we have resume
    if not resume:
        raise ValueError(f"Missing resume - resume: {len(resume)} chars")
    
    # If no job description, use generic one
    if not job_desc:
        print("⚠️ No job description found, using generic optimization")
        job_desc = "Professional role requiring strong technical skills, communication abilities, and relevant experience. Seeking candidates with proven track record and ability to work in team environments."
    
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
    
    # Sentiment - only if resume has content
    sentiment_result = 'NEUTRAL'
    if resume and len(resume) > 0:
        try:
            sentiment = comprehend.detect_sentiment(Text=resume[:5000], LanguageCode='en')
            sentiment_result = sentiment['Sentiment']
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
    
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
        'sentiment': sentiment_result,
        'originalScore': max(50, score),
        'targetScore': 85,
        'resume': resume,  # Pass through for next steps
        'jobDescription': job_desc  # Pass through for next steps
    }
    
    publish_event('AnalysisComplete', {'jobId': event.get('jobId', 'unknown'), 'jobType': job_type})
    
    print(f"✓ {len(gaps)} gaps, {len(matched)} matched, type: {job_type}")
    return analysis
