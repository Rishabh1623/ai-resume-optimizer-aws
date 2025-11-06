# Architecture Diagrams

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                     │
│                    (Upload Resume)                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      S3 INPUT BUCKET                             │
│                   (resume-optimizer-input)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ S3 Event
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      EVENTBRIDGE                                 │
│                   (Event-Driven Trigger)                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STEP FUNCTIONS                                 │
│              (Agentic AI Orchestration)                          │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  AGENTIC AI WORKFLOW                                   │    │
│  │                                                         │    │
│  │  1. Perceive (Analyze)                                 │    │
│  │     ├─ Extract text (Textract)                         │    │
│  │     ├─ Analyze sentiment (Comprehend)                  │    │
│  │     └─ Understand context (Bedrock)                    │    │
│  │                                                         │    │
│  │  2. Plan (Strategy)                                    │    │
│  │     ├─ Identify skill gaps                             │    │
│  │     ├─ Determine job type                              │    │
│  │     └─ Create optimization plan                        │    │
│  │                                                         │    │
│  │  3. Act (Generate) - PARALLEL                          │    │
│  │     ├─ Version A: Keyword-optimized                    │    │
│  │     ├─ Version B: Achievement-focused                  │    │
│  │     └─ Version C: Structure-improved                   │    │
│  │                                                         │    │
│  │  4. Evaluate (Score)                                   │    │
│  │     ├─ Calculate ATS scores                            │    │
│  │     ├─ Check keyword density                           │    │
│  │     └─ Count action verbs                              │    │
│  │                                                         │    │
│  │  5. Decide (Iterate?)                                  │    │
│  │     ├─ If score < 85: Improve and loop back           │    │
│  │     └─ If score >= 85: Success!                        │    │
│  │                                                         │    │
│  │  6. Select (Best Version)                              │    │
│  │     └─ Choose highest scoring version                  │    │
│  └────────────────────────────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RESULTS STORAGE                                │
│                                                                  │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │  S3 OUTPUT       │         │   DYNAMODB       │             │
│  │  (Optimized      │         │   (Job Tracking) │             │
│  │   Resume)        │         │                  │             │
│  └──────────────────┘         └──────────────────┘             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SNS NOTIFICATION                            │
│                   (Email to User)                                │
└─────────────────────────────────────────────────────────────────┘
```

## Agentic AI Loop

```
                    ┌─────────────────┐
                    │   START         │
                    │  (Resume + Job) │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PERCEIVE      │
                    │  (Analyze)      │
                    │                 │
                    │ • Extract text  │
                    │ • Find skills   │
                    │ • Understand    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     PLAN        │
                    │  (Strategy)     │
                    │                 │
                    │ • Skill gaps    │
                    │ • Job type      │
                    │ • Approach      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      ACT        │
                    │  (Generate)     │
                    │                 │
                    │ • 3 versions    │
                    │ • Parallel      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   EVALUATE      │
                    │   (Score)       │
                    │                 │
                    │ • ATS score     │
                    │ • Keywords      │
                    │ • Quality       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    DECIDE       │
                    │  Score >= 85?   │
                    └────┬───────┬────┘
                         │       │
                    YES  │       │  NO
                         │       │
                         │       └──────┐
                         │              │
                         ▼              ▼
                ┌─────────────┐  ┌─────────────┐
                │   SUCCESS   │  │   ITERATE   │
                │  (Return)   │  │  (Improve)  │
                └─────────────┘  └──────┬──────┘
                                        │
                                        │ Loop back
                                        └──────────┐
                                                   │
                                                   ▼
                                          ┌─────────────────┐
                                          │      ACT        │
                                          │  (Generate)     │
                                          └─────────────────┘
```

## AWS Services Integration

```
┌──────────────────────────────────────────────────────────────┐
│                    COMPUTE LAYER                              │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Lambda     │  │   Lambda     │  │   Lambda     │      │
│  │  API Handler │  │  Processor   │  │  Evaluator   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                  ORCHESTRATION LAYER                          │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │     SQS      │  │     Step     │  │  EventBridge │      │
│  │   Queues     │  │  Functions   │  │    Rules     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                      AI LAYER                                 │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Bedrock    │  │   Textract   │  │  Comprehend  │      │
│  │   (Claude)   │  │   (Extract)  │  │  (Sentiment) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                    STORAGE LAYER                              │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │      S3      │  │   DynamoDB   │  │  CloudWatch  │      │
│  │   Buckets    │  │    Tables    │  │     Logs     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow

```
Resume PDF
    │
    ├─> S3 Upload
    │       │
    │       ├─> EventBridge Event
    │       │       │
    │       │       ├─> Step Functions Start
    │       │       │       │
    │       │       │       ├─> Lambda: Extract Text (Textract)
    │       │       │       │       │
    │       │       │       │       └─> Text Data
    │       │       │       │
    │       │       │       ├─> Lambda: Analyze (Comprehend)
    │       │       │       │       │
    │       │       │       │       └─> Sentiment Score
    │       │       │       │
    │       │       │       ├─> Lambda: Plan Strategy (Bedrock)
    │       │       │       │       │
    │       │       │       │       └─> Optimization Plan
    │       │       │       │
    │       │       │       ├─> Lambda: Generate Versions (Bedrock)
    │       │       │       │       │
    │       │       │       │       ├─> Version A
    │       │       │       │       ├─> Version B
    │       │       │       │       └─> Version C
    │       │       │       │
    │       │       │       ├─> Lambda: Evaluate (Custom Logic)
    │       │       │       │       │
    │       │       │       │       └─> Scores
    │       │       │       │
    │       │       │       ├─> Decision: Score >= 85?
    │       │       │       │       │
    │       │       │       │       ├─> YES: Continue
    │       │       │       │       └─> NO: Loop back to Generate
    │       │       │       │
    │       │       │       └─> Lambda: Select Best
    │       │       │               │
    │       │       │               └─> Best Version
    │       │       │
    │       │       └─> Save Results
    │       │               │
    │       │               ├─> S3 Output Bucket
    │       │               └─> DynamoDB Job Record
    │       │
    │       └─> SNS Notification
    │               │
    │               └─> Email to User
    │
    └─> Complete!
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      SECURITY LAYERS                         │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  IAM LAYER                                         │    │
│  │  • Least privilege roles                           │    │
│  │  • Service-specific policies                       │    │
│  │  • No hardcoded credentials                        │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │  ENCRYPTION LAYER                                  │    │
│  │  • S3: AES-256 at rest                            │    │
│  │  • DynamoDB: Encryption at rest                   │    │
│  │  • TLS 1.2+ in transit                            │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │  NETWORK LAYER                                     │    │
│  │  • VPC endpoints (optional)                        │    │
│  │  • Private subnets                                 │    │
│  │  • Security groups                                 │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │  MONITORING LAYER                                  │    │
│  │  • CloudWatch logs                                 │    │
│  │  • X-Ray tracing                                   │    │
│  │  • CloudTrail audit                                │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Cost Breakdown

```
Per Resume Processing:

┌─────────────────────────────────────────┐
│  Lambda Execution        $0.0001        │
│  Bedrock (3 iterations)  $0.0040        │
│  Textract                $0.0015        │
│  Comprehend              $0.0001        │
│  S3 Storage/Transfer     $0.0001        │
│  DynamoDB                $0.0001        │
│  SQS Messages            $0.0001        │
│  ─────────────────────────────────      │
│  TOTAL                   $0.0060        │
└─────────────────────────────────────────┘

Monthly (1000 resumes):
  Total: ~$6.00
```

## Scalability

```
Current Capacity:
┌──────────────────────────────────┐
│  Concurrent Executions: 1000     │
│  Resumes/Day: 10,000             │
│  Resumes/Month: 300,000          │
└──────────────────────────────────┘

Scale to 1M/month:
┌──────────────────────────────────┐
│  1. Increase Lambda concurrency  │
│  2. Add SQS FIFO queues          │
│  3. Use DynamoDB auto-scaling    │
│  4. Add CloudFront caching       │
│  5. Multi-region deployment      │
└──────────────────────────────────┘
```
