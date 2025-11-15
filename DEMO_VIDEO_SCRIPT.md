# Demo Video Script - AI Resume Optimizer

**Total Time: 2-3 minutes**

---

## 🎬 SCENE 1: Introduction (15 seconds)

**[Show GitHub repo page]**

"Hi, I'm Rishabh, and this is my AI Resume Optimizer - an intelligent system I built on AWS that uses agentic AI to automatically optimize resumes for job applications."

---

## 🏗️ SCENE 2: Architecture Overview (30 seconds)

**[Show architecture diagram]**

"The system uses 15+ AWS services in an event-driven architecture. At its core is an agentic AI workflow powered by AWS Step Functions.

Unlike traditional AI that just responds to prompts, this agent makes autonomous decisions - it perceives the problem, plans a strategy, takes action, evaluates its work, and learns from the results.

It uses AWS Bedrock with Claude 3 for AI, Textract for PDF extraction, and DynamoDB for storing what it learns."

---

## 🚀 SCENE 3: Live Demo - Upload (20 seconds)

**[Show S3 Console]**

"Let me show you how it works. I'll upload a resume and job description to S3."

**[Upload files to S3]**

"As soon as the files hit S3, an event triggers the workflow automatically."

---

## 🤖 SCENE 4: Agent in Action (45 seconds)

**[Show Step Functions visual execution]**

"Here's where it gets interesting. Watch the agent work through its phases:

**[Point to Analyze step]**
First, it analyzes the resume - extracting skills, identifying gaps, and understanding the job requirements.

**[Point to Plan step]**
Then it autonomously decides on an optimization strategy based on the job type and what's worked before.

**[Point to Generate parallel steps]**
Next, it generates three different optimized versions in parallel - one focused on keywords, one on achievements, and one on structure.

**[Point to Evaluate step]**
The agent then evaluates each version, scoring them on ATS compatibility, keyword matching, and achievement metrics.

**[Point to CheckQuality decision]**
Here's the key - if the score is below 85%, it automatically iterates and tries again. In this case, it achieved 91% on the first try, so it moves straight to learning."

---

## 📊 SCENE 5: Results (30 seconds)

**[Show email notification]**

"Within 90 seconds, I receive an email with the results.

The original resume scored 58 out of 100. The optimized version? 91.4 - that's a 33-point improvement!

**[Show S3 output bucket]**
The optimized resume is automatically saved to S3.

**[Show DynamoDB]**
And the agent stores this successful strategy in its memory, so it gets smarter with each optimization."

---

## 💡 SCENE 6: Technical Highlights (20 seconds)

**[Show code/Terraform]**

"The entire infrastructure is deployed with Terraform - about 35 AWS resources defined as code.

Key features include:
- Agentic AI with autonomous decision-making
- Event-driven architecture with custom EventBridge bus
- Production-ready with error handling and monitoring
- Costs less than a penny per resume"

---

## 🎯 SCENE 7: Closing (10 seconds)

**[Show GitHub repo]**

"This project demonstrates advanced AWS patterns, agentic AI principles, and production-ready architecture. All the code is on GitHub. Thanks for watching!"

---

## 📝 Alternative: SHORT VERSION (90 seconds)

**[Show GitHub]**
"Hi, I'm Rishabh. This is my AI Resume Optimizer built on AWS.

**[Show architecture]**
It uses agentic AI - meaning the system makes autonomous decisions, not just responds to prompts.

**[Upload to S3]**
I upload a resume and job description to S3.

**[Show Step Functions]**
The agent analyzes, plans a strategy, generates three versions, evaluates them, and learns from the results - all automatically.

**[Show results]**
In 90 seconds, my resume score improved from 58 to 91 out of 100.

**[Show code]**
Built with 15+ AWS services, deployed with Terraform, and production-ready. Check it out on GitHub!"

---

## 🎯 Key Points to Emphasize

1. **"Agentic AI"** - Say this multiple times, it's your differentiator
2. **"Autonomous decisions"** - Not just AI, but intelligent agent behavior
3. **"91% score in 1 iteration"** - Shows efficiency
4. **"15+ AWS services"** - Demonstrates breadth of knowledge
5. **"Production-ready"** - Not just a toy project
6. **"Event-driven architecture"** - Modern design pattern

---

## 🎬 Recording Tips

### Before Recording:
- [ ] Clean up browser tabs
- [ ] Close unnecessary applications
- [ ] Test audio (clear, no background noise)
- [ ] Prepare all screens in advance
- [ ] Do a practice run

### What to Show:
1. GitHub repo (5 sec)
2. Architecture diagram (10 sec)
3. S3 upload (10 sec)
4. Step Functions execution (30 sec)
5. Email results (10 sec)
6. S3 output (5 sec)
7. DynamoDB memory (5 sec)
8. Code/Terraform (10 sec)
9. GitHub repo again (5 sec)

### Recording Settings:
- **Resolution:** 1920x1080 (1080p)
- **Frame Rate:** 30 fps
- **Audio:** Clear voice, no music
- **Length:** 2-3 minutes max
- **Format:** MP4 (H.264)

---

## 🎤 Voice Tips

- **Pace:** Speak clearly, not too fast
- **Energy:** Enthusiastic but professional
- **Pauses:** Brief pause between sections
- **Emphasis:** Stress key technical terms
- **Confidence:** You built this, own it!

---

## 📱 Quick Mobile-Friendly Script (60 seconds)

"AI Resume Optimizer - built on AWS with agentic AI.

**[Architecture]** 15+ services, event-driven design.

**[Demo]** Upload resume to S3, agent analyzes, plans, generates three versions, evaluates, and learns.

**[Results]** 58 to 91 score in 90 seconds.

**[Tech]** Step Functions, Bedrock, Lambda, DynamoDB. Terraform IaC. Production-ready.

Check it out on GitHub!"

---

## 🎯 What NOT to Say

❌ "Um", "uh", "like", "you know"
❌ "This is just a simple project"
❌ "I'm not sure if this works"
❌ Apologizing for anything
❌ Reading code line by line

## ✅ What TO Say

✅ "I built", "I designed", "I implemented"
✅ "Production-ready", "Scalable", "Event-driven"
✅ "Agentic AI", "Autonomous", "Self-improving"
✅ Specific numbers (91%, 15+ services, 90 seconds)
✅ AWS service names confidently

---

## 🎬 Final Checklist

Before uploading:
- [ ] Video is 2-3 minutes
- [ ] Audio is clear
- [ ] Shows actual working system
- [ ] Mentions "agentic AI" multiple times
- [ ] Shows impressive results (91% score)
- [ ] Ends with GitHub link
- [ ] File size under 10MB (or upload to YouTube)

---

**Good luck with your recording! You've got this! 🚀**
