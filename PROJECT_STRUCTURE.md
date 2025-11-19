# AI Resume Optimizer - Project Structure

Clean, production-ready repository structure following AWS and Terraform best practices.

## Directory Structure

```
resume-optimizer/
├── lambda/                          # Lambda function code
│   ├── agent_analyze.py            # Perceive: Analyze resume and job
│   ├── agent_plan.py               # Plan: Strategy selection
│   ├── agent_generate.py           # Act: Generate optimized versions
│   ├── agent_evaluate.py           # Evaluate: Score and rank versions
│   ├── agent_learn.py              # Learn: Store successful strategies
│   ├── api_handler.py              # API Gateway handler
│   ├── s3_trigger.py               # S3 event trigger handler
│   └── requirements.txt            # Python dependencies
│
├── terraform/                       # Infrastructure as Code
│   ├── main.tf                     # Main Terraform configuration
│   ├── variables.tf                # Variable definitions
│   ├── terraform.tfvars.example    # Example configuration
│   └── terraform.tfvars            # Your configuration (gitignored)
│
├── .gitignore                       # Git ignore patterns
├── ARCHITECTURE_DIAGRAM.md          # System architecture documentation
├── DEPLOYMENT.md                    # Deployment guide
├── LICENSE                          # MIT License
├── QUICK_SETUP.md                   # Quick start guide
├── README.md                        # Project overview
├── step-functions-input.json        # Test input for Step Functions
└── verify-deployment.sh             # Deployment verification script
```

## File Descriptions

### Lambda Functions (`lambda/`)

**agent_analyze.py** - Perceive Phase
- Extracts text from resume using Textract
- Analyzes job description
- Identifies skill gaps
- Determines job type and context

**agent_plan.py** - Plan Phase
- Queries agent memory for similar jobs
- Selects optimization strategy
- Sets quality targets (ATS ≥ 85)
- Defines approaches (keywords, achievements, structure)

**agent_generate.py** - Act Phase
- Generates 3 parallel resume versions
- Uses Bedrock Claude 3 for content generation
- Applies different optimization strategies
- Supports iterative improvement

**agent_evaluate.py** - Evaluate Phase
- Scores each version (ATS, keywords, achievements)
- Ranks versions by quality
- Determines if quality threshold met
- Decides whether to iterate

**agent_learn.py** - Learn Phase
- Stores successful strategies in DynamoDB
- Updates agent memory
- Tracks performance metrics
- Sends completion notifications

**api_handler.py** - API Gateway Handler
- Health check endpoint
- Manual optimization trigger
- Status query endpoint
- RESTful API interface

**s3_trigger.py** - S3 Event Handler
- Processes S3 upload events
- Validates file types
- Triggers Step Functions workflow
- Handles errors gracefully

**requirements.txt** - Python Dependencies
- boto3 (AWS SDK)
- Minimal dependencies for Lambda

### Terraform (`terraform/`)

**main.tf** - Infrastructure Definition
- Lambda functions and layers
- Step Functions state machine
- S3 buckets (input/output)
- DynamoDB tables (jobs, memory, analytics)
- EventBridge rules
- SNS notifications
- IAM roles and policies
- CloudWatch logs

**variables.tf** - Configuration Variables
- AWS region
- Project name
- Environment
- Bedrock model ID
- Email notifications
- Resource tags

**terraform.tfvars.example** - Example Configuration
- Template for your configuration
- Copy to `terraform.tfvars`
- Update with your values

**terraform.tfvars** - Your Configuration
- Gitignored for security
- Contains your AWS settings
- Email addresses
- Custom configurations

### Documentation

**README.md** - Project Overview
- What the project does
- Key features
- Quick start
- Architecture overview
- Cost estimates

**DEPLOYMENT.md** - Deployment Guide
- Prerequisites
- Step-by-step deployment
- Verification steps
- Troubleshooting
- Cost optimization

**QUICK_SETUP.md** - Quick Start
- Fastest way to get started
- Minimal configuration
- Basic testing
- Common commands

**ARCHITECTURE_DIAGRAM.md** - Architecture
- System design
- Component interactions
- Data flow
- AWS services used
- Agentic AI workflow

### Configuration Files

**.gitignore** - Git Ignore Patterns
- Terraform state files
- Python cache
- IDE files
- AWS credentials
- Personal notes
- Generated artifacts

**LICENSE** - MIT License
- Open source license
- Usage permissions
- Liability disclaimer

### Testing & Verification

**step-functions-input.json** - Test Input
- Sample input for Step Functions
- Test resume and job description
- Manual execution testing

**verify-deployment.sh** - Verification Script
- Checks all resources created
- Validates configuration
- Tests basic functionality
- Reports deployment status

## Best Practices Implemented

### Code Organization
- ✅ Separate Lambda functions by responsibility
- ✅ Single responsibility principle
- ✅ Clear naming conventions
- ✅ Minimal dependencies

### Infrastructure as Code
- ✅ All resources defined in Terraform
- ✅ Variables for configuration
- ✅ Example files for onboarding
- ✅ State management

### Security
- ✅ No hardcoded credentials
- ✅ IAM least privilege
- ✅ Secrets in gitignore
- ✅ Encryption at rest/transit

### Documentation
- ✅ Clear README
- ✅ Deployment guide
- ✅ Architecture diagrams
- ✅ Code comments

### Version Control
- ✅ Comprehensive gitignore
- ✅ No generated files
- ✅ No personal information
- ✅ Clean commit history

## What's NOT in the Repository

Following best practices, these are excluded:

### Generated Files
- ❌ Terraform state files (`.tfstate`)
- ❌ Lambda deployment packages (`.zip`)
- ❌ Python cache (`__pycache__`)
- ❌ Generated diagrams (`.png`)

### Configuration
- ❌ Personal `terraform.tfvars`
- ❌ AWS credentials
- ❌ Environment variables (`.env`)

### Personal Files
- ❌ Interview notes
- ❌ Job descriptions
- ❌ Demo scripts
- ❌ TODO lists

### Development Artifacts
- ❌ IDE settings (`.vscode`, `.idea`)
- ❌ OS files (`.DS_Store`)
- ❌ Backup files (`.bak`)
- ❌ Log files (`.log`)

## Adding New Features

### New Lambda Function
1. Create `lambda/new_function.py`
2. Add to `terraform/main.tf`
3. Update Step Functions workflow
4. Add IAM permissions
5. Update documentation

### New AWS Service
1. Add resource to `terraform/main.tf`
2. Add IAM permissions
3. Update Lambda code
4. Test thoroughly
5. Update cost estimates

### New Configuration
1. Add variable to `terraform/variables.tf`
2. Update `terraform.tfvars.example`
3. Document in DEPLOYMENT.md
4. Update README if user-facing

## Maintenance

### Regular Updates
- Review and update dependencies
- Check for AWS service updates
- Update Terraform provider versions
- Review and optimize costs
- Update documentation

### Security
- Rotate credentials regularly
- Review IAM policies
- Update Lambda runtimes
- Scan for vulnerabilities
- Monitor CloudWatch logs

### Performance
- Monitor Lambda execution times
- Optimize memory allocation
- Review Bedrock token usage
- Check DynamoDB capacity
- Analyze CloudWatch metrics

## Contributing

When contributing:
1. Follow existing code structure
2. Update documentation
3. Add tests if applicable
4. Keep commits clean
5. Update CHANGELOG (if exists)

## Questions?

Refer to:
- README.md for overview
- DEPLOYMENT.md for setup
- ARCHITECTURE_DIAGRAM.md for design
- Code comments for implementation details
