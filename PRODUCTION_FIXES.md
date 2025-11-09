# Production Fixes Required

## Issue 1: Job Description Not Being Read
The system shows "Job Type: general" which means it's still using the fallback generic JD.

**Fix**: Verify the file path in S3 matches exactly what's in step-functions-input.json

## Issue 2: Scoring Algorithm Too Conservative
Current scores are artificially low (58 → 67.5) even with good optimization.

**Fix**: Update evaluation algorithm to be more realistic and production-ready.
