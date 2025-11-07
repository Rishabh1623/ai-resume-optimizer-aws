# Update Lambda function code
$functionName = "resume-optimizer-dev-analyze"
$region = "us-east-1"

# Create zip file
Compress-Archive -Path "lambda\agent_analyze.py" -DestinationPath "agent_analyze.zip" -Force

# Update Lambda
aws lambda update-function-code `
    --function-name $functionName `
    --zip-file fileb://agent_analyze.zip `
    --region $region

Write-Host "Lambda function updated successfully!"

# Clean up
Remove-Item "agent_analyze.zip"
