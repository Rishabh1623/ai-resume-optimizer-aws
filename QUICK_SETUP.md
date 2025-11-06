# Quick Setup Guide

## 🚀 3 Steps to Deploy

### Step 1: Edit Configuration (1 minute)

The file `terraform/terraform.tfvars` is already created. Just edit your email:

```bash
cd terraform
nano terraform.tfvars
```

**Change this line:**
```hcl
notification_email = "your-email@example.com"  # ⚠️ Put your real email here!
```

**Save:** `Ctrl+X`, `Y`, `Enter`

### Step 2: Deploy (3-5 minutes)

```bash
terraform init
terraform apply
```

Type `yes` when prompted.

### Step 3: Enable Bedrock (1 minute)

1. Go to AWS Console → Bedrock
2. Click "Model access"
3. Enable "Claude 3 Sonnet"
4. Wait 1-2 minutes

**Done!** 🎉

---

## 📝 Configuration File Explained

### Location
```
terraform/terraform.tfvars
```

### Required Values

```hcl
# ⚠️ MUST CHANGE
notification_email = "your-email@example.com"
```

### Optional Values (defaults are fine)

```hcl
# AWS region (Bedrock available in these regions)
aws_region = "us-east-1"  # or us-west-2, eu-west-1, ap-southeast-1

# Project name (prefix for all resources)
project_name = "resume-optimizer"

# Environment
environment = "dev"  # or staging, prod

# AI Model
bedrock_model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
# Options:
# - claude-3-haiku (faster, cheaper)
# - claude-3-sonnet (balanced) ← default
# - claude-3-opus (best quality, expensive)

# Lambda settings
lambda_timeout = 300  # seconds (5 minutes)
lambda_memory = 512   # MB
```

---

## 🔧 Different Ways to Edit

### Method 1: Nano (Easiest on Linux)
```bash
nano terraform/terraform.tfvars
# Edit, then Ctrl+X, Y, Enter
```

### Method 2: Vim
```bash
vim terraform/terraform.tfvars
# Press 'i' to edit
# Press 'Esc', type ':wq', Enter to save
```

### Method 3: VS Code (if installed)
```bash
code terraform/terraform.tfvars
```

### Method 4: Edit on Windows, then upload
```bash
# On Windows: Edit terraform/terraform.tfvars
# Then upload to EC2:
scp -i your-key.pem terraform/terraform.tfvars ubuntu@YOUR_EC2_IP:~/resume-optimizer/terraform/
```

### Method 5: Use sed (command line)
```bash
# Replace email in one command
sed -i 's/your-email@example.com/real-email@gmail.com/g' terraform/terraform.tfvars

# Replace region
sed -i 's/us-east-1/us-west-2/g' terraform/terraform.tfvars
```

---

## ✅ Verify Configuration

```bash
# Check your values
cat terraform/terraform.tfvars

# Should show your real email, not "your-email@example.com"
```

---

## 🎯 Minimal Configuration (Just Email)

If you only want to change the email:

```bash
cd terraform
echo 'notification_email = "your-real-email@gmail.com"' >> terraform.tfvars
```

All other values will use defaults.

---

## 🚨 Common Mistakes

### ❌ Forgot to change email
```hcl
notification_email = "your-email@example.com"  # ← Still example!
```

### ✅ Correct
```hcl
notification_email = "john.doe@gmail.com"  # ← Real email
```

### ❌ Wrong region (Bedrock not available)
```hcl
aws_region = "us-west-1"  # ← Bedrock not available here!
```

### ✅ Correct regions
```hcl
aws_region = "us-east-1"     # ✓ Virginia
aws_region = "us-west-2"     # ✓ Oregon
aws_region = "eu-west-1"     # ✓ Ireland
aws_region = "ap-southeast-1" # ✓ Singapore
```

---

## 📋 Pre-Deployment Checklist

Before running `terraform apply`:

- [ ] Edited `terraform/terraform.tfvars`
- [ ] Changed `notification_email` to your real email
- [ ] Verified `aws_region` supports Bedrock
- [ ] AWS credentials configured (`aws configure`)
- [ ] In the `terraform/` directory

---

## 🚀 Deploy Command

```bash
cd terraform
terraform init
terraform apply
```

**That's it!** 🎉
