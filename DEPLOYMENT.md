# AI Resume Optimizer - Deployment Guide

Complete guide for deploying the AI Resume Optimizer to AWS.

## Prerequisites

### Required Tools
- AWS CLI v2+ configured with credentials
- Terraform v1.0+
- Python 3.9+
- Git

### AWS Account Requirements
- Active AWS account with billing enabled
- IAM permissions for:
  - Lambda, Step Functions, S3, DynamoDB
  - EventBridge, SNS, CloudWatch
  - Bedrock (Claude 3 model access)
  - Textract, Comprehend
  - IAM role creation

### Bedrock Model Access
1. Navigate to AWS Bedrock console
2. Request access to Claude 3 models (Haiku/Sonnet)
3. Wait for approval (usually instant)

## Pre-Deployment Checklist

- [ ] AWS CLI configured (`aws configure`)
- [ ] Terraform installed (`terraform --version`)
- [ ] Bedrock model access granted
- [ ] Email verified for SNS notifications
- [ ] S3 bucket names available (globally unique)
- [ ] Review and update `terraform.tfvars`

## Deployment Steps

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd resume-optimizer
```

### 2. Configure Variables
```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:
```hcl
aws_region          = "us-east-1"
project_name        = "resume-optimizer"
environment         = "prod"
notification_email  = "your-email@example.com"
bedrock_model_id    = "anthropic.claude-3-haiku-20240307-v1:0"
```

### 3. Initialize Terraform
```bash
terraform init
```

### 4. Review Deployment Plan
```bash
terraform plan
```

Review the resources to be created:
- 6 Lambda functions
- 1 Step Functions state machine
- 2 S3 buckets
- 3 DynamoDB tables
- EventBridge rules
- SNS topic
- IAM roles and policies

### 5. Deploy Infrastructure
```bash
terraform apply
```

Type `yes` when prompted. Deployment takes ~5-10 minutes.

### 6. Verify Deployment
```bash
# Check Lambda functions
aws lambda list-functions --query 'Functions[?contains(FunctionName, `resume-optimizer`)].FunctionName'

# Check Step Functions
aws stepfunctions list-state-machines --query 'stateMachines[?contains(name, `resume-optimizer`)].name'

# Check S3 buckets
aws s3 ls | grep resume-optimizer

# Check DynamoDB tables
aws dynamodb list-tables --query 'TableNames[?contains(@, `resume-optimizer`)]'
```

### 7. Confirm SNS Subscription
Check your email for SNS subscription confirmation and click the link.

### 8. Test Deployment
```bash
# Run verification script
bash verify-deployment.sh
```

Or test manually:
```bash
# Upload test resume
aws s3 cp test-resume.pdf s3://resume-optimizer-input-<account-id>/test-resume.pdf
aws s3 cp test-job-description.txt s3://resume-optimizer-input-<account-id>/test-job-description.txt

# Monitor execution
aws stepfunctions list-executions \
  --state-machine-arn <state-machine-arn> \
  --max-results 1
```

## Post-Deployment

### Monitor Logs
```bash
# View Lambda logs
aws logs tail /aws/lambda/resume-optimizer-analyze --follow

# View Step Functions execution
aws stepfunctions describe-execution --execution-arn <execution-arn>
```

### Check Costs
```bash
# View cost explorer (requires Cost Explorer enabled)
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost
```

### Set Up Alarms (Optional)
```bash
# Create CloudWatch alarm for Lambda errors
aws cloudwatch put-metric-alarm \
  --alarm-name resume-optimizer-errors \
  --alarm-description "Alert on Lambda errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold
```

## Updating the System

### Update Lambda Code
```bash
# Make changes to lambda/*.py files
cd terraform
terraform apply
```

### Update Configuration
```bash
# Edit terraform.tfvars
terraform plan
terraform apply
```

### Update Step Functions Workflow
```bash
# Edit terraform/main.tf (step_functions_definition)
terraform apply
```

## Troubleshooting

### Lambda Timeout
- Increase timeout in `terraform/main.tf`
- Default: 300 seconds (5 minutes)

### Bedrock Access Denied
- Verify model access in Bedrock console
- Check IAM role permissions
- Confirm correct model ID in variables

### S3 Upload Fails
- Check bucket permissions
- Verify EventBridge rule is enabled
- Check CloudWatch logs for errors

### Step Functions Fails
- View execution history in console
- Check individual Lambda logs
- Verify IAM role permissions

### High Costs
- Review CloudWatch metrics
- Check Bedrock token usage
- Optimize Lambda memory/timeout
- Consider using Claude Haiku instead of Sonnet

## Cleanup

### Destroy All Resources
```bash
cd terraform
terraform destroy
```

Type `yes` when prompted.

### Manual Cleanup (if needed)
```bash
# Empty S3 buckets first
aws s3 rm s3://resume-optimizer-input-<account-id> --recursive
aws s3 rm s3://resume-optimizer-output-<account-id> --recursive

# Then destroy
terraform destroy
```

## Security Best Practices

1. **Never commit secrets**
   - Use AWS Secrets Manager for sensitive data
   - Keep `terraform.tfvars` in `.gitignore`

2. **Enable encryption**
   - S3: Server-side encryption (enabled by default)
   - DynamoDB: Encryption at rest (enabled by default)

3. **Restrict IAM permissions**
   - Use least privilege principle
   - Review IAM policies regularly

4. **Enable logging**
   - CloudWatch Logs for all Lambda functions
   - CloudTrail for API calls
   - X-Ray for distributed tracing

5. **Monitor costs**
   - Set up billing alarms
   - Review Cost Explorer monthly
   - Use AWS Budgets

## Cost Optimization

- Use Claude Haiku for lower costs (~$0.004/resume)
- Adjust Lambda memory based on actual usage
- Enable S3 lifecycle policies for old files
- Use DynamoDB on-demand pricing for variable workloads
- Set up CloudWatch log retention policies

## Support

For issues or questions:
1. Check CloudWatch logs
2. Review Step Functions execution history
3. Verify IAM permissions
4. Check AWS service quotas
5. Review Terraform state

## Architecture Overview

```
User → S3 → EventBridge → Step Functions → Lambda Agents → Bedrock/Textract/Comprehend
                                              ↓
                                         DynamoDB + S3 Output → SNS → Email
```

## Next Steps

1. Set up CI/CD pipeline (GitHub Actions)
2. Add monitoring dashboard
3. Implement API Gateway for web interface
4. Add authentication (Cognito)
5. Scale to multi-region deployment
