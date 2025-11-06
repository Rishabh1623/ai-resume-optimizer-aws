# ============================================================================
# TERRAFORM VARIABLES - CUSTOMIZE THESE VALUES
# ============================================================================
# This file defines all configurable values for the project.
# Copy terraform.tfvars.example to terraform.tfvars and edit your values.

# ----------------------------------------------------------------------------
# REQUIRED: AWS Region
# ----------------------------------------------------------------------------
# CHANGE THIS: Set your preferred AWS region
# Bedrock is available in: us-east-1, us-west-2, eu-west-1, ap-southeast-1
variable "aws_region" {
  description = "AWS region where all resources will be created"
  type        = string
  default     = "us-east-1" # CHANGE: Your region
}

# ----------------------------------------------------------------------------
# REQUIRED: Email for Notifications
# ----------------------------------------------------------------------------
# CHANGE THIS: Your email address to receive notifications
# You'll get an email when resume optimization completes
variable "notification_email" {
  description = "Email address to receive SNS notifications"
  type        = string
  # NO DEFAULT - You must provide this in terraform.tfvars
}

# ----------------------------------------------------------------------------
# OPTIONAL: Project Configuration
# ----------------------------------------------------------------------------
# CHANGE THIS: If you want a different project name
# This is used as prefix for all resource names
variable "project_name" {
  description = "Project name (used as prefix for all resources)"
  type        = string
  default     = "resume-optimizer" # OPTIONAL: Change if needed
}

# CHANGE THIS: Environment name (dev, staging, prod)
variable "environment" {
  description = "Environment name (dev/staging/prod)"
  type        = string
  default     = "dev" # OPTIONAL: Change for different environments
}

# ----------------------------------------------------------------------------
# OPTIONAL: AI Model Configuration
# ----------------------------------------------------------------------------
# CHANGE THIS: If you want to use a different Claude model
# Available models: claude-3-sonnet, claude-3-haiku, claude-3-opus
variable "bedrock_model_id" {
  description = "Amazon Bedrock Claude model ID"
  type        = string
  default     = "anthropic.claude-3-sonnet-20240229-v1:0" # OPTIONAL: Change model
}

# ----------------------------------------------------------------------------
# OPTIONAL: Lambda Performance Settings
# ----------------------------------------------------------------------------
# CHANGE THIS: If you need longer processing time
# Default: 300 seconds (5 minutes)
# Increase if processing large resumes or complex jobs
variable "lambda_timeout" {
  description = "Lambda function timeout in seconds (max: 900)"
  type        = number
  default     = 300 # OPTIONAL: Increase if timeouts occur
}

# CHANGE THIS: If you need more memory for Lambda
# Default: 512 MB
# More memory = faster processing but higher cost
variable "lambda_memory" {
  description = "Lambda function memory in MB (128-10240)"
  type        = number
  default     = 512 # OPTIONAL: Increase for better performance
}

# ----------------------------------------------------------------------------
# OPTIONAL: Cost and Resource Tags
# ----------------------------------------------------------------------------
# CHANGE THIS: Add your own tags for cost tracking
variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    Project     = "resume-optimizer"
    ManagedBy   = "terraform"
    Environment = "dev"
  }
  # OPTIONAL: Add more tags like:
  # CostCenter = "engineering"
  # Owner      = "your-name"
}
