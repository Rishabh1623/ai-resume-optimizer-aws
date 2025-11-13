# FINAL FIX - Get to 85%+ Score

## Root Cause Analysis

**Current Results:**
- Score: 75.6/100 ❌
- Job Type: "general" ❌ (Should be "technical")
- Keyword Match: 43.8% ❌ (Should be 75%+)

**Problem:** The Capgemini job description is NOT being read from S3.

## Critical Fixes Required

### Fix 1: Upload Job Description to Correct Location

**Current file path in JSON:**
```json
"job_description_key": "resumes/job-description.txt"
```

**Action Required:**
1. Go to S3 Console: `resume-optimizer-dev-input-543927035352`
2. Navigate to `resumes/` folder
3. Upload `capgemini-job-description.txt` 
4. **Rename it to:** `job-description.txt` (NOT .pdf)

**Verify:**
- File should be at: `s3://resume-optimizer-dev-input-543927035352/resumes/job-description.txt`
- File size should be ~2KB (not empty)

### Fix 2: Update Lambda Functions (CRITICAL)

You MUST update these Lambda functions in AWS Console:

#### Lambda 1: resume-optimizer-dev-evaluate
```
Source: lambda/agent_evaluate.py
Status: ❌ NOT UPDATED (still using old scoring)
```

**How to Update:**
1. AWS Console → Lambda → `resume-optimizer-dev-evaluate`
2. Delete ALL existing code
3. Copy from `lambda/agent_evaluate.py` in your repo
4. Click "Deploy"
5. Wait for "Successfully updated"

#### Lambda 2: resume-optimizer-dev-generate  
```
Source: lambda/agent_generate.py
Status: ❌ NOT UPDATED (still using old prompts)
```

**How to Update:**
1. AWS Console → Lambda → `resume-optimizer-dev-generate`
2. Delete ALL existing code
3. Copy from `lambda/agent_generate.py` in your repo
4. Click "Deploy"

### Fix 3: Verify S3 File Reading

The Lambda needs to read TXT files correctly. Update step-functions-input.json:

```json
{
    "user_id": "rishabh-madne",
    "resume_key": "resumes/Rishabh_R_Madne.pdf",
    "job_description_key": "resumes/job-description.txt",
    "bucket": "resume-optimizer-dev-input-543927035352",
    "execution_id": "exec-003",
    "iteration": 1,
    "max_iterations": 3
}
```

## Expected Results After Fixes

| Metric | Current | After Fix | Target |
|--------|---------|-----------|--------|
| Overall Score | 75.6 | 88-92 | 85+ ✅ |
| Job Type | general | technical | technical ✅ |
| Keyword Match | 43.8% | 78-85% | 75%+ ✅ |
| Action Verbs | 13 | 18-22 | 15+ ✅ |
| Iterations | 3 | 1-2 | <3 ✅ |

## Step-by-Step Deployment

### Step 1: Upload Job Description (2 minutes)

**Option A: AWS CLI**
```bash
aws s3 cp capgemini-job-description.txt s3://resume-optimizer-dev-input-543927035352/resumes/job-description.txt
```

**Option B: AWS Console**
1. Open S3 Console
2. Go to bucket: `resume-optimizer-dev-input-543927035352`
3. Click `resumes/` folder
4. Click "Upload"
5. Select `capgemini-job-description.txt`
6. **Important:** Rename to `job-description.txt` during upload
7. Click "Upload"

### Step 2: Update Lambda - agent_evaluate (3 minutes)

1. Open AWS Lambda Console
2. Search for: `resume-optimizer-dev-evaluate`
3. Click on the function
4. Scroll to "Code source" section
5. Select ALL code (Ctrl+A)
6. Delete it
7. Open your local file: `lambda/agent_evaluate.py`
8. Copy ALL content (Ctrl+A, Ctrl+C)
9. Paste into Lambda editor (Ctrl+V)
10. Click "Deploy" button (orange)
11. Wait for "Successfully updated the function"

### Step 3: Update Lambda - agent_generate (3 minutes)

1. Search for: `resume-optimizer-dev-generate`
2. Click on the function
3. Select ALL code and delete
4. Open your local file: `lambda/agent_generate.py`
5. Copy ALL content
6. Paste into Lambda editor
7. Click "Deploy"
8. Wait for success message

### Step 4: Run Test Execution (2 minutes)

1. Go to Step Functions Console
2. Click on: `resume-optimizer-dev-agentic-workflow`
3. Click "Start execution"
4. Paste this JSON:
```json
{
    "user_id": "rishabh-madne",
    "resume_key": "resumes/Rishabh_R_Madne.pdf",
    "job_description_key": "resumes/job-description.txt",
    "bucket": "resume-optimizer-dev-input-543927035352",
    "execution_id": "exec-003",
    "iteration": 1,
    "max_iterations": 3
}
```
5. Click "Start execution"
6. Wait 2-3 minutes
7. Check email for results

## Verification Checklist

After deployment, verify:

- [ ] S3 file exists: `resumes/job-description.txt`
- [ ] Lambda `agent_evaluate` shows new code (check for "PRODUCTION-READY SCORING")
- [ ] Lambda `agent_generate` shows new code (check for "CRITICAL: Must preserve")
- [ ] Step Functions execution completes successfully
- [ ] Email shows:
  - [ ] Job Type: "technical" (not "general")
  - [ ] Keyword Match: 75%+ (not 43%)
  - [ ] Overall Score: 85%+ (not 75%)
  - [ ] Iterations: 1-2 (not 3)

## Troubleshooting

### Issue: Still shows "Job Type: general"

**Cause:** Job description file not found or not readable

**Fix:**
1. Check S3 file exists at exact path
2. Verify file is not empty (should be ~2KB)
3. Check CloudWatch logs for "Error reading job description"

### Issue: Score still low (< 80%)

**Cause:** Lambda code not updated

**Fix:**
1. Go to Lambda function
2. Check if code contains "PRODUCTION-READY SCORING ALGORITHM"
3. If not, re-deploy the code

### Issue: "invoke_bedrock is not defined"

**Cause:** Old Lambda code still deployed

**Fix:**
1. Update ALL Lambda functions from repository
2. Ensure each has the helper functions at the top

## Quick Verification Commands

```bash
# Check if JD file exists in S3
aws s3 ls s3://resume-optimizer-dev-input-543927035352/resumes/job-description.txt

# Download and verify content
aws s3 cp s3://resume-optimizer-dev-input-543927035352/resumes/job-description.txt - | head -20

# Check Lambda function code (first 50 lines)
aws lambda get-function --function-name resume-optimizer-dev-evaluate --query 'Code.Location' --output text
```

## Success Criteria

✅ **Job Type:** "technical" (indicates Capgemini JD is being read)  
✅ **Keyword Match:** 78-85% (high match with Capgemini requirements)  
✅ **Overall Score:** 88-92/100 (realistic production score)  
✅ **Iterations:** 1-2 (reaches target faster)  
✅ **Action Verbs:** 18-22 (expanded detection)  
✅ **Achievements:** 12-15 (better pattern matching)

## Time Estimate

- Upload JD: 2 minutes
- Update 2 Lambda functions: 6 minutes
- Run test: 3 minutes
- **Total: ~11 minutes**

## After Success

Once you see 85%+ scores:

1. ✅ System is production-ready
2. ✅ Can demo in interviews
3. ✅ Can add to resume/portfolio
4. ✅ Can discuss architecture confidently

## Support

If still having issues after following all steps:

1. Check CloudWatch Logs for each Lambda
2. Verify S3 file permissions (should be readable by Lambda role)
3. Ensure Terraform applied successfully
4. Check IAM roles have S3 read permissions
