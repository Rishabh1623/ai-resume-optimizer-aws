"""
AGENTIC AI - ACT: Generate optimized versions
Optimized for minimal code size
"""
import json
import boto3
import os

bedrock = boto3.client('bedrock-runtime', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
events = boto3.client('events')

BEDROCK_MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-haiku-20240307-v1:0')
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME', 'resume-optimizer-events')


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
            modelId=BEDROCK_MODEL_ID,
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
                'EventBusName': EVENT_BUS_NAME
            }]
        )
    except Exception as e:
        print(f"Event publish error: {e}")


def lambda_handler(event, context):
    """Act: Generate optimized version"""
    approach = event.get('approach', 'keywords')
    input_data = event.get('input', {})
    
    resume = input_data.get('resume', '')
    job_desc = input_data.get('jobDescription', '')
    iteration = input_data.get('iteration', 1)
    
    print(f"🎨 ACT: Generating {approach} version (iter {iteration})...")
    
    # Build prompt based on approach - CRITICAL: Must preserve original content
    if approach == 'keywords':
        prompt = f"""Optimize this resume by incorporating relevant keywords from the job description while keeping ALL original content, experience, and achievements.

JOB DESCRIPTION:
{job_desc[:1500]}

ORIGINAL RESUME:
{resume[:3000]}

INSTRUCTIONS:
- Keep ALL original work experience, projects, and achievements
- Add relevant keywords from job description naturally
- Maintain the candidate's actual name, contact info, and details
- Improve ATS compatibility
- Use action verbs
- Keep professional tone

Return ONLY the optimized resume with the candidate's actual information."""
    
    elif approach == 'achievements':
        prompt = f"""Enhance this resume by making achievements more quantifiable and impactful while keeping ALL original content.

JOB DESCRIPTION:
{job_desc[:1500]}

ORIGINAL RESUME:
{resume[:3000]}

INSTRUCTIONS:
- Keep ALL original work experience and projects
- Enhance existing achievements with stronger action verbs
- Maintain all actual metrics and numbers
- Add impact statements where appropriate
- Keep the candidate's actual name and details
- Align with job requirements

Return ONLY the enhanced resume with the candidate's actual information."""
    
    else:  # structure
        prompt = f"""Improve the structure and formatting of this resume while keeping ALL original content intact.

JOB DESCRIPTION:
{job_desc[:1500]}

ORIGINAL RESUME:
{resume[:3000]}

INSTRUCTIONS:
- Keep ALL original content, experience, and achievements
- Improve section organization and formatting
- Maintain the candidate's actual name, contact, and details
- Enhance readability and ATS compatibility
- Use clear section headers
- Keep professional formatting

Return ONLY the restructured resume with the candidate's actual information."""
    
    if iteration > 1:
        prompt += f"\n\nIteration {iteration}: Further refine based on previous optimization."
    
    optimized = invoke_bedrock(prompt, 4096, 0.7) or resume
    
    publish_event('VersionGenerated', {'jobId': input_data.get('jobId'), 'approach': approach})
    
    print(f"✓ Generated {len(optimized)} chars")
    return {'approach': approach, 'content': optimized, 'iteration': iteration}
