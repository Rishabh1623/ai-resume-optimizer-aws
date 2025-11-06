#!/bin/bash
# Deployment Verification Script
# Run this after terraform apply to verify agentic AI deployment

set -e

echo "=========================================="
echo "Verifying Agentic AI Deployment"
echo "=========================================="
echo ""

cd terraform

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_error() { echo -e "${RED}✗ $1${NC}"; }
print_info() { echo -e "${YELLOW}→ $1${NC}"; }

# Get outputs
print_info "Getting deployment outputs..."
STATE_MACHINE_ARN=$(terraform output -raw state_machine_arn 2>/dev/null)
EVENT_BUS_NAME=$(terraform output -raw event_bus_name 2>/dev/null)
AGENT_MEMORY_TABLE=$(terraform output -raw agent_memory_table 2>/dev/null)
INPUT_BUCKET=$(terraform output -raw input_bucket_name 2>/dev/null)
API_ENDPOINT=$(terraform output -raw api_endpoint 2>/dev/null)

if [ -z "$STATE_MACHINE_ARN" ]; then
    print_error "Terraform outputs not found. Did you run 'terraform apply'?"
    exit 1
fi

print_success "Outputs retrieved"
echo ""

# Check 1: Step Functions
print_info "Checking Step Functions (Agentic Workflow)..."
if aws stepfunctions describe-state-machine --state-machine-arn "$STATE_MACHINE_ARN" &>/dev/null; then
    print_success "Step Functions state machine exists"
else
    print_error "Step Functions state machine not found"
fi

# Check 2: Lambda Functions
print_info "Checking Lambda Functions (Agent Components)..."
LAMBDAS=("api" "analyze" "plan" "generate" "evaluate" "learn")
for lambda in "${LAMBDAS[@]}"; do
    if aws lambda get-function --function-name "resume-optimizer-dev-$lambda" &>/dev/null; then
        print_success "Lambda $lambda exists"
    else
        print_error "Lambda $lambda not found"
    fi
done

# Check 3: EventBridge Custom Bus
print_info "Checking EventBridge Custom Bus..."
if aws events describe-event-bus --name "$EVENT_BUS_NAME" &>/dev/null; then
    print_success "Custom event bus exists"
else
    print_error "Custom event bus not found"
fi

# Check 4: Agent Memory Table
print_info "Checking Agent Memory Table..."
if aws dynamodb describe-table --table-name "$AGENT_MEMORY_TABLE" &>/dev/null; then
    print_success "Agent memory table exists"
else
    print_error "Agent memory table not found"
fi

# Check 5: S3 Buckets
print_info "Checking S3 Buckets..."
if aws s3 ls "s3://$INPUT_BUCKET" &>/dev/null; then
    print_success "Input bucket exists"
else
    print_error "Input bucket not found"
fi

# Check 6: API Gateway
print_info "Checking API Gateway..."
if curl -s "$API_ENDPOINT/health" | grep -q "healthy"; then
    print_success "API Gateway is healthy"
else
    print_error "API Gateway health check failed"
fi

# Check 7: Bedrock Access
print_info "Checking Bedrock Model Access..."
if aws bedrock list-foundation-models --region us-east-1 2>/dev/null | grep -q "claude"; then
    print_success "Bedrock access configured"
else
    print_error "Bedrock access not enabled - Go to AWS Console → Bedrock → Model Access"
fi

echo ""
echo "=========================================="
echo "Verification Complete!"
echo "=========================================="
echo ""
echo "Deployment Summary:"
echo "  API Endpoint: $API_ENDPOINT"
echo "  Input Bucket: $INPUT_BUCKET"
echo "  State Machine: $STATE_MACHINE_ARN"
echo "  Event Bus: $EVENT_BUS_NAME"
echo ""
echo "Next Steps:"
echo "  1. Confirm email subscription (check inbox)"
echo "  2. Upload a resume to test: aws s3 cp resume.pdf s3://$INPUT_BUCKET/"
echo "  3. Watch execution: AWS Console → Step Functions"
echo "  4. View logs: aws logs tail /aws/lambda/resume-optimizer-dev-analyze --follow"
echo ""
