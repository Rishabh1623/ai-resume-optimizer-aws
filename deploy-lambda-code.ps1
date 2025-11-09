# Deploy updated Lambda code to AWS
Write-Host "Deploying Lambda function code..." -ForegroundColor Cyan

$functionName = "resume-optimizer-dev-analyze"
$region = "us-east-1"

# Create a temporary directory for the Lambda package
$tempDir = "temp_lambda"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

# Copy the Lambda file
Copy-Item "lambda\agent_analyze.py" -Destination "$tempDir\agent_analyze.py"

# Create zip file
$zipFile = "lambda_package.zip"
if (Test-Path $zipFile) { Remove-Item $zipFile }

Compress-Archive -Path "$tempDir\*" -DestinationPath $zipFile

Write-Host "Uploading to AWS Lambda..." -ForegroundColor Yellow

# Update Lambda function
aws lambda update-function-code `
    --function-name $functionName `
    --zip-file fileb://$zipFile `
    --region $region

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Lambda function updated successfully!" -ForegroundColor Green
    Write-Host "You can now run your Step Functions execution." -ForegroundColor Green
} else {
    Write-Host "`n✗ Failed to update Lambda function" -ForegroundColor Red
    Write-Host "Please update manually in AWS Console" -ForegroundColor Yellow
}

# Clean up
Remove-Item -Recurse -Force $tempDir
Remove-Item $zipFile

Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
