# ============================================================================
# AI RESUME OPTIMIZER - AGENTIC AI + EVENT-DRIVEN ARCHITECTURE
# ============================================================================
# This implements:
# 1. Step Functions - Agentic AI workflow with autonomous decision-making
# 2. EventBridge Custom Bus - True event-driven architecture
# 3. Agent Memory - Learning from past optimizations
#
# WHAT TO CHANGE:
# 1. Copy terraform.tfvars.example to terraform.tfvars
# 2. Edit terraform.tfvars with your email and region
# 3. Run: terraform init && terraform apply
# ============================================================================

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

locals {
  name_prefix = "${var.project_name}-${var.environment}"
}

data "aws_caller_identity" "current" {}

# ============================================================================
# EVENTBRIDGE CUSTOM EVENT BUS - Event-Driven Architecture
# ============================================================================
# Custom event bus for resume optimization events
resource "aws_cloudwatch_event_bus" "resume_events" {
  name = "${local.name_prefix}-events"
}

# Event Archive for replay capability
resource "aws_cloudwatch_event_archive" "resume_events" {
  name             = "${local.name_prefix}-archive"
  event_source_arn = aws_cloudwatch_event_bus.resume_events.arn
  retention_days   = 30
}

# ============================================================================
# S3 BUCKETS - File Storage
# ============================================================================
resource "aws_s3_bucket" "input" {
  bucket = "${local.name_prefix}-input-${data.aws_caller_identity.current.account_id}"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "input" {
  bucket = aws_s3_bucket.input.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket" "output" {
  bucket = "${local.name_prefix}-output-${data.aws_caller_identity.current.account_id}"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "output" {
  bucket = aws_s3_bucket.output.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "output" {
  bucket = aws_s3_bucket.output.id
  
  rule {
    id     = "delete-old-files"
    status = "Enabled"
    
    filter {
      prefix = ""
    }
    
    expiration {
      days = 30
    }
  }
}

# S3 notification triggers Lambda (which then starts Step Functions)
# This allows us to check for matching job description files
resource "aws_s3_bucket_notification" "input" {
  bucket = aws_s3_bucket.input.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.s3_trigger.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.s3_trigger]
}

# ============================================================================
# DYNAMODB TABLES - Database
# ============================================================================
# Jobs table
resource "aws_dynamodb_table" "jobs" {
  name         = "${local.name_prefix}-jobs"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "jobId"

  attribute {
    name = "jobId"
    type = "S"
  }

  attribute {
    name = "userId"
    type = "S"
  }

  global_secondary_index {
    name            = "userId-index"
    hash_key        = "userId"
    projection_type = "ALL"
  }

  ttl {
    attribute_name = "expiresAt"
    enabled        = true
  }

  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"
}

# Agent Memory table - Stores learning from past optimizations
resource "aws_dynamodb_table" "agent_memory" {
  name         = "${local.name_prefix}-agent-memory"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "jobType"
  range_key    = "timestamp"

  attribute {
    name = "jobType"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }

  attribute {
    name = "successScore"
    type = "N"
  }

  global_secondary_index {
    name            = "score-index"
    hash_key        = "jobType"
    range_key       = "successScore"
    projection_type = "ALL"
  }
}

# Analytics table
resource "aws_dynamodb_table" "analytics" {
  name         = "${local.name_prefix}-analytics"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "date"
  range_key    = "metric"

  attribute {
    name = "date"
    type = "S"
  }

  attribute {
    name = "metric"
    type = "S"
  }
}

# ============================================================================
# SQS QUEUES - Message Queuing
# ============================================================================
resource "aws_sqs_queue" "processing" {
  name                       = "${local.name_prefix}-processing"
  visibility_timeout_seconds = var.lambda_timeout + 30
  message_retention_seconds  = 86400
  receive_wait_time_seconds  = 20

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_sqs_queue" "dlq" {
  name                      = "${local.name_prefix}-dlq"
  message_retention_seconds = 1209600
}

# ============================================================================
# SNS TOPIC - Notifications with Fan-Out
# ============================================================================
resource "aws_sns_topic" "notifications" {
  name = "${local.name_prefix}-notifications"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.notifications.arn
  protocol  = "email"
  endpoint  = var.notification_email
}

# ============================================================================
# IAM ROLES - Permissions
# ============================================================================
# Lambda execution role
resource "aws_iam_role" "lambda" {
  name = "${local.name_prefix}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "lambda" {
  name = "${local.name_prefix}-lambda-policy"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = [
          "${aws_s3_bucket.input.arn}/*",
          "${aws_s3_bucket.output.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          aws_dynamodb_table.jobs.arn,
          "${aws_dynamodb_table.jobs.arn}/index/*",
          aws_dynamodb_table.agent_memory.arn,
          "${aws_dynamodb_table.agent_memory.arn}/index/*",
          aws_dynamodb_table.analytics.arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = [
          aws_sqs_queue.processing.arn,
          aws_sqs_queue.dlq.arn
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["sns:Publish"]
        Resource = aws_sns_topic.notifications.arn
      },
      {
        Effect   = "Allow"
        Action   = ["bedrock:InvokeModel"]
        Resource = "arn:aws:bedrock:*::foundation-model/*"
      },
      {
        Effect = "Allow"
        Action = [
          "textract:AnalyzeDocument",
          "textract:DetectDocumentText"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "comprehend:DetectSentiment",
          "comprehend:DetectEntities"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "events:PutEvents"
        ]
        Resource = aws_cloudwatch_event_bus.resume_events.arn
      },
      {
        Effect = "Allow"
        Action = [
          "states:StartExecution"
        ]
        Resource = aws_sfn_state_machine.agentic_workflow.arn
      }
    ]
  })
}

# Step Functions execution role
resource "aws_iam_role" "step_functions" {
  name = "${local.name_prefix}-stepfunctions-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "states.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "step_functions" {
  name = "${local.name_prefix}-stepfunctions-policy"
  role = aws_iam_role.step_functions.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:InvokeFunction"
        ]
        Resource = [
          aws_lambda_function.analyze.arn,
          aws_lambda_function.plan.arn,
          aws_lambda_function.generate.arn,
          aws_lambda_function.evaluate.arn,
          aws_lambda_function.learn.arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "events:PutEvents"
        ]
        Resource = aws_cloudwatch_event_bus.resume_events.arn
      }
    ]
  })
}

# ============================================================================
# LAMBDA FUNCTIONS - Agentic AI Components   Rishabhmadne
# ============================================================================
data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda"
  output_path = "${path.module}/lambda.zip"
}

# API Handler
resource "aws_lambda_function" "api" {
  filename         = data.archive_file.lambda.output_path
  function_name    = "${local.name_prefix}-api"
  role             = aws_iam_role.lambda.arn
  handler          = "api_handler.lambda_handler"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  runtime          = "python3.11"
  timeout          = 30
  memory_size      = 256

  environment {
    variables = {
      STATE_MACHINE_ARN = aws_sfn_state_machine.agentic_workflow.arn
      JOBS_TABLE        = aws_dynamodb_table.jobs.name
      EVENT_BUS_NAME    = aws_cloudwatch_event_bus.resume_events.name
    }
  }
}

# Analyze Lambda - Perceive phase of agent
resource "aws_lambda_function" "analyze" {
  filename         = data.archive_file.lambda.output_path
  function_name    = "${local.name_prefix}-analyze"
  role             = aws_iam_role.lambda.arn
  handler          = "agent_analyze.lambda_handler"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  runtime          = "python3.11"
  timeout          = var.lambda_timeout
  memory_size      = var.lambda_memory

  environment {
    variables = {
      BEDROCK_MODEL_ID = var.bedrock_model_id
      JOBS_TABLE       = aws_dynamodb_table.jobs.name
      EVENT_BUS_NAME   = aws_cloudwatch_event_bus.resume_events.name
      INPUT_BUCKET     = aws_s3_bucket.input.id
    }
  }
}

# Plan Lambda - Planning phase of agent
resource "aws_lambda_function" "plan" {
  filename         = data.archive_file.lambda.output_path
  function_name    = "${local.name_prefix}-plan"
  role             = aws_iam_role.lambda.arn
  handler          = "agent_plan.lambda_handler"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  runtime          = "python3.11"
  timeout          = var.lambda_timeout
  memory_size      = var.lambda_memory

  environment {
    variables = {
      BEDROCK_MODEL_ID   = var.bedrock_model_id
      AGENT_MEMORY_TABLE = aws_dynamodb_table.agent_memory.name
      EVENT_BUS_NAME     = aws_cloudwatch_event_bus.resume_events.name
    }
  }
}

# Generate Lambda - Action phase of agent
resource "aws_lambda_function" "generate" {
  filename         = data.archive_file.lambda.output_path
  function_name    = "${local.name_prefix}-generate"
  role             = aws_iam_role.lambda.arn
  handler          = "agent_generate.lambda_handler"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  runtime          = "python3.11"
  timeout          = var.lambda_timeout
  memory_size      = var.lambda_memory

  environment {
    variables = {
      BEDROCK_MODEL_ID = var.bedrock_model_id
      EVENT_BUS_NAME   = aws_cloudwatch_event_bus.resume_events.name
    }
  }
}

# Evaluate Lambda - Evaluation phase of agent
resource "aws_lambda_function" "evaluate" {
  filename         = data.archive_file.lambda.output_path
  function_name    = "${local.name_prefix}-evaluate"
  role             = aws_iam_role.lambda.arn
  handler          = "agent_evaluate.lambda_handler"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  runtime          = "python3.11"
  timeout          = var.lambda_timeout
  memory_size      = var.lambda_memory

  environment {
    variables = {
      EVENT_BUS_NAME = aws_cloudwatch_event_bus.resume_events.name
    }
  }
}

# Learn Lambda - Learning phase of agent
resource "aws_lambda_function" "learn" {
  filename         = data.archive_file.lambda.output_path
  function_name    = "${local.name_prefix}-learn"
  role             = aws_iam_role.lambda.arn
  handler          = "agent_learn.lambda_handler"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  runtime          = "python3.11"
  timeout          = 60
  memory_size      = 256

  environment {
    variables = {
      AGENT_MEMORY_TABLE = aws_dynamodb_table.agent_memory.name
      OUTPUT_BUCKET      = aws_s3_bucket.output.id
      SNS_TOPIC_ARN      = aws_sns_topic.notifications.arn
      JOBS_TABLE         = aws_dynamodb_table.jobs.name
      EVENT_BUS_NAME     = aws_cloudwatch_event_bus.resume_events.name
    }
  }
}

# S3 Trigger Lambda - Handles resume uploads and finds matching JD
resource "aws_lambda_function" "s3_trigger" {
  filename         = data.archive_file.lambda.output_path
  function_name    = "${local.name_prefix}-s3-trigger"
  role             = aws_iam_role.lambda.arn
  handler          = "s3_trigger.lambda_handler"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  runtime          = "python3.11"
  timeout          = 60
  memory_size      = 512

  environment {
    variables = {
      STATE_MACHINE_ARN = aws_sfn_state_machine.agentic_workflow.arn
    }
  }
}

# Lambda permission for S3 to invoke trigger
resource "aws_lambda_permission" "s3_trigger" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.s3_trigger.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.input.arn
}

# ============================================================================
# STEP FUNCTIONS - Agentic AI Workflow
# ============================================================================
resource "aws_sfn_state_machine" "agentic_workflow" {
  name     = "${local.name_prefix}-agentic-workflow"
  role_arn = aws_iam_role.step_functions.arn

  definition = jsonencode({
    Comment = "Agentic AI Resume Optimization Workflow"
    StartAt = "Analyze"
    States = {
      # PERCEIVE: Analyze resume and job description
      Analyze = {
        Type       = "Task"
        Resource   = aws_lambda_function.analyze.arn
        ResultPath = "$.analysis"
        Next       = "Plan"
        Catch = [{
          ErrorEquals = ["States.ALL"]
          ResultPath  = "$.error"
          Next        = "HandleError"
        }]
      }

      # PLAN: Create optimization strategy
      Plan = {
        Type       = "Task"
        Resource   = aws_lambda_function.plan.arn
        ResultPath = "$.plan"
        Next       = "InitializeIteration"
      }

      # Initialize iteration counter
      InitializeIteration = {
        Type       = "Pass"
        Result     = 1
        ResultPath = "$.iteration"
        Next       = "GenerateVersions"
      }

      # ACT: Generate optimized versions (parallel)
      GenerateVersions = {
        Type       = "Parallel"
        ResultPath = "$.versions"
        Next       = "Evaluate"
        Branches = [
          {
            StartAt = "GenerateKeywordVersion"
            States = {
              GenerateKeywordVersion = {
                Type     = "Task"
                Resource = aws_lambda_function.generate.arn
                Parameters = {
                  "approach" : "keywords"
                  "input.$" : "$"
                }
                End = true
              }
            }
          },
          {
            StartAt = "GenerateAchievementVersion"
            States = {
              GenerateAchievementVersion = {
                Type     = "Task"
                Resource = aws_lambda_function.generate.arn
                Parameters = {
                  "approach" : "achievements"
                  "input.$" : "$"
                }
                End = true
              }
            }
          },
          {
            StartAt = "GenerateStructureVersion"
            States = {
              GenerateStructureVersion = {
                Type     = "Task"
                Resource = aws_lambda_function.generate.arn
                Parameters = {
                  "approach" : "structure"
                  "input.$" : "$"
                }
                End = true
              }
            }
          }
        ]
      }

      # EVALUATE: Score all versions
      Evaluate = {
        Type       = "Task"
        Resource   = aws_lambda_function.evaluate.arn
        ResultPath = "$.evaluation"
        Next       = "CheckQuality"
      }

      # DECIDE: Is quality good enough?
      CheckQuality = {
        Type = "Choice"
        Choices = [
          {
            Variable                 = "$.evaluation.bestScore"
            NumericGreaterThanEquals = 85
            Next                     = "Learn"
          },
          {
            Variable                 = "$.iteration"
            NumericGreaterThanEquals = 3
            Next                     = "Learn"
          }
        ]
        Default = "IncrementIteration"
      }

      # ITERATE: Improve and try again
      IncrementIteration = {
        Type = "Pass"
        Parameters = {
          "iteration.$"      = "States.MathAdd($.iteration, 1)"
          "analysis.$"       = "$.analysis"
          "plan.$"           = "$.plan"
          "evaluation.$"     = "$.evaluation"
          "jobId.$"          = "$.jobId"
          "resume.$"         = "$.analysis.resume"
          "jobDescription.$" = "$.analysis.jobDescription"
        }
        Next = "GenerateVersions"
      }

      # LEARN: Store successful strategy
      Learn = {
        Type       = "Task"
        Resource   = aws_lambda_function.learn.arn
        ResultPath = "$.result"
        Next       = "Success"
      }

      Success = {
        Type = "Succeed"
      }

      HandleError = {
        Type  = "Fail"
        Error = "WorkflowFailed"
        Cause = "Agentic workflow encountered an error"
      }
    }
  })
}

# ============================================================================
# API GATEWAY - REST API
# ============================================================================
resource "aws_api_gateway_rest_api" "main" {
  name = "${local.name_prefix}-api"
}

resource "aws_api_gateway_resource" "optimize" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "optimize"
}

resource "aws_api_gateway_method" "optimize_post" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.optimize.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "optimize" {
  rest_api_id             = aws_api_gateway_rest_api.main.id
  resource_id             = aws_api_gateway_resource.optimize.id
  http_method             = aws_api_gateway_method.optimize_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.api.invoke_arn
}

resource "aws_api_gateway_resource" "health" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "health"
}

resource "aws_api_gateway_method" "health_get" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.health.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "health" {
  rest_api_id             = aws_api_gateway_rest_api.main.id
  resource_id             = aws_api_gateway_resource.health.id
  http_method             = aws_api_gateway_method.health_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.api.invoke_arn
}

resource "aws_api_gateway_deployment" "main" {
  rest_api_id = aws_api_gateway_rest_api.main.id

  depends_on = [
    aws_api_gateway_integration.optimize,
    aws_api_gateway_integration.health
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "main" {
  deployment_id = aws_api_gateway_deployment.main.id
  rest_api_id   = aws_api_gateway_rest_api.main.id
  stage_name    = var.environment
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.main.execution_arn}/*/*"
}

# ============================================================================
# OUTPUTS
# ============================================================================
output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = aws_api_gateway_stage.main.invoke_url
}

output "input_bucket_name" {
  description = "S3 input bucket name"
  value       = aws_s3_bucket.input.id
}

output "output_bucket_name" {
  description = "S3 output bucket name"
  value       = aws_s3_bucket.output.id
}

output "state_machine_arn" {
  description = "Step Functions state machine ARN"
  value       = aws_sfn_state_machine.agentic_workflow.arn
}

output "event_bus_name" {
  description = "EventBridge custom event bus name"
  value       = aws_cloudwatch_event_bus.resume_events.name
}

output "agent_memory_table" {
  description = "Agent memory DynamoDB table name"
  value       = aws_dynamodb_table.agent_memory.name
}

output "jobs_table_name" {
  description = "Jobs DynamoDB table name"
  value       = aws_dynamodb_table.jobs.name
}

output "upload_instructions" {
  description = "How to upload resume and job description"
  value       = <<-EOT
    Upload Pattern:
    1. Create folder: s3://${aws_s3_bucket.input.id}/your-name/
    2. Upload resume: s3://${aws_s3_bucket.input.id}/your-name/resume.pdf
    3. Upload JD: s3://${aws_s3_bucket.input.id}/your-name/job-description.txt
    
    Example:
    aws s3 cp resume.pdf s3://${aws_s3_bucket.input.id}/john-doe/resume.pdf
    aws s3 cp job-description.txt s3://${aws_s3_bucket.input.id}/john-doe/job-description.txt
  EOT
}
