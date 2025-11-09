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
    
    # Build prompt based on approach
    prompts = {
        'keywords': f"Optimize resume with job keywords. Job: {job_desc[:1500]} Resume: {resume[:2000]}",
        'achievements': f"Add quantified achievements. Job: {job_desc[:1500]} Resume: {resume[:2000]}",
        'structure': f"Improve structure and formatting. Job: {job_desc[:1500]} Resume: {resume[:2000]}"
    }
    
    base_prompt = prompts.get(approach, prompts['keywords'])
    prompt = f"{base_prompt}\n\nInstructions:\n- ATS-friendly\n- Professional tone\n- Clear sections\n- Action verbs\n- Metrics\n\nReturn ONLY optimized resume."
    
    if iteration > 1:
        prompt += f"\n\nIteration {iteration}: Improve previous attempt."
    
    optimized = invoke_bedrock(prompt, 4096, 0.7) or resume
    
    publish_event('VersionGenerated', {'jobId': input_data.get('jobId'), 'approach': approach})
    
    print(f"✓ Generated {len(optimized)} chars")
    return {'approach': approach, 'content': optimized, 'iteration': iteration}
