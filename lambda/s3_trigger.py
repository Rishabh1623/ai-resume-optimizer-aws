"""
S3 Trigger Handler - Processes resume uploads and finds matching job descriptions
Supports two upload patterns:
1. user123/resume.pdf + user123/job-description.txt
2. resume.pdf (generic optimization without JD)
"""
import json
import boto3
import os
from urllib.parse import unquote_plus

s3 = boto3.client('s3')
stepfunctions = boto3.client('stepfunctions')
textract = boto3.client('textract')

STATE_MACHINE_ARN = os.environ['STATE_MACHINE_ARN']

def lambda_handler(event, context):
    """
    Triggered by S3 upload
    Looks for matching job description file
    Starts Step Functions workflow
    """
    print("📤 S3 Upload detected...")
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        
        print(f"File: s3://{bucket}/{key}")
        
        # Skip if this is a job description file (we only trigger on resume)
        if 'job-description' in key.lower() or key.endswith('.txt'):
            print("Skipping job description file")
            continue
        
        # Skip output folder
        if key.startswith('optimized/'):
            print("Skipping output folder")
            continue
        
        # Extract user folder if present
        # Pattern: user123/resume.pdf or just resume.pdf
        parts = key.split('/')
        if len(parts) == 2:
            user_folder = parts[0]
            filename = parts[1]
        else:
            user_folder = None
            filename = key
        
        print(f"User folder: {user_folder}")
        print(f"Filename: {filename}")
        
        # Look for matching job description
        job_description = find_job_description(bucket, user_folder, key)
        
        if job_description:
            print(f"✓ Found job description ({len(job_description)} chars)")
        else:
            print("⚠ No job description found - using generic optimization")
            job_description = "Generic resume optimization for professional roles"
        
        # Extract text from resume
        resume_text = extract_resume_text(bucket, key)
        
        if not resume_text:
            print("❌ Could not extract text from resume")
            continue
        
        print(f"✓ Extracted resume text ({len(resume_text)} chars)")
        
        # Generate job ID
        job_id = f"{user_folder or 'user'}-{filename.replace('.pdf', '')}-{context.request_id[:8]}"
        
        # Start Step Functions workflow
        try:
            stepfunctions.start_execution(
                stateMachineArn=STATE_MACHINE_ARN,
                name=f"job-{job_id}".replace('/', '-')[:80],  # Max 80 chars
                input=json.dumps({
                    'jobId': job_id,
                    'userId': user_folder or 'anonymous',
                    'resume': resume_text,
                    'jobDescription': job_description,
                    'targetRole': 'Professional Role',
                    'sourceFile': key
                })
            )
            print(f"✓ Started workflow: {job_id}")
            
        except Exception as e:
            print(f"❌ Error starting workflow: {e}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processing started')
    }

def find_job_description(bucket, user_folder, resume_key):
    """
    Look for job description file in same folder
    Supports both .txt and .pdf files
    Patterns:
    - user123/job-description.txt or .pdf
    - user123/jd.txt or .pdf
    - user123/job.txt or .pdf
    """
    if not user_folder:
        # No user folder, check for JD in root
        jd_patterns = [
            'job-description.txt', 'job-description.pdf',
            'jd.txt', 'jd.pdf',
            'job.txt', 'job.pdf',
            'job-desc.txt', 'job-desc.pdf'
        ]
    else:
        # Check in user folder
        jd_patterns = [
            f"{user_folder}/job-description.txt",
            f"{user_folder}/job-description.pdf",
            f"{user_folder}/jd.txt",
            f"{user_folder}/jd.pdf",
            f"{user_folder}/job.txt",
            f"{user_folder}/job.pdf",
            f"{user_folder}/job-desc.txt",
            f"{user_folder}/job-desc.pdf"
        ]
    
    for pattern in jd_patterns:
        try:
            # Check if file exists
            s3.head_object(Bucket=bucket, Key=pattern)
            
            # Extract text based on file type
            if pattern.endswith('.pdf'):
                jd_text = extract_text_from_pdf(bucket, pattern)
            else:
                response = s3.get_object(Bucket=bucket, Key=pattern)
                jd_text = response['Body'].read().decode('utf-8')
            
            if jd_text:
                print(f"✓ Found JD: {pattern}")
                return jd_text
                
        except s3.exceptions.NoSuchKey:
            continue
        except Exception as e:
            print(f"Error reading {pattern}: {e}")
            continue
    
    return None

def extract_text_from_pdf(bucket, key):
    """Extract text from PDF using Textract"""
    try:
        response = textract.detect_document_text(
            Document={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            }
        )
        
        # Extract text from all blocks
        text = ''
        for block in response.get('Blocks', []):
            if block['BlockType'] == 'LINE':
                text += block['Text'] + '\n'
        
        return text
        
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return None

def extract_resume_text(bucket, key):
    """Extract text from PDF using Textract"""
    try:
        # For PDF files, use Textract
        if key.lower().endswith('.pdf'):
            response = textract.detect_document_text(
                Document={
                    'S3Object': {
                        'Bucket': bucket,
                        'Name': key
                    }
                }
            )
            
            # Extract text from all blocks
            text = ''
            for block in response.get('Blocks', []):
                if block['BlockType'] == 'LINE':
                    text += block['Text'] + '\n'
            
            return text
        
        # For text files, read directly
        elif key.lower().endswith('.txt'):
            response = s3.get_object(Bucket=bucket, Key=key)
            return response['Body'].read().decode('utf-8')
        
        else:
            print(f"Unsupported file type: {key}")
            return None
            
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None
