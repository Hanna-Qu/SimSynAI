# GitHub Repository Setup Script (Windows PowerShell)
# Initialize project and publish to GitHub

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername,
    
    [Parameter(Mandatory=$false)]
    [string]$RepoName = "SimSynAI",
    
    [Parameter(Mandatory=$false)]
    [switch]$CreateRepo = $false
)

Write-Host "GitHub Repository Setup Script" -ForegroundColor Green
Write-Host "Username: $GitHubUsername" -ForegroundColor Blue
Write-Host "Repository: $RepoName" -ForegroundColor Blue
Write-Host "=================================" -ForegroundColor Green

# Check if in project root directory
if (-not (Test-Path "VERSION")) {
    Write-Host "ERROR: Please run this script from project root directory" -ForegroundColor Red
    exit 1
}

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "OK: Git installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git not installed. Please install Git:" -ForegroundColor Red
    Write-Host "   Download: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Check if GitHub CLI is installed (optional)
$ghInstalled = $false
try {
    $ghVersion = gh --version
    Write-Host "OK: GitHub CLI installed: $ghVersion" -ForegroundColor Green
    $ghInstalled = $true
} catch {
    Write-Host "WARNING: GitHub CLI not installed, using manual mode" -ForegroundColor Yellow
    Write-Host "   Recommended: winget install GitHub.cli" -ForegroundColor Cyan
}

# 1. Initialize Git repository (if not exists)
if (-not (Test-Path ".git")) {
    Write-Host "SETUP: Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "OK: Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "OK: Git repository exists" -ForegroundColor Green
}

# 2. Update README with username
Write-Host "SETUP: Updating GitHub links in README..." -ForegroundColor Yellow
$readmeContent = Get-Content "README.md" -Raw
$readmeContent = $readmeContent -replace "your-username", $GitHubUsername
$readmeContent | Set-Content "README.md" -Encoding UTF8
Write-Host "OK: README updated" -ForegroundColor Green

# 3. Update development docs with links
Write-Host "SETUP: Updating GitHub links in development docs..." -ForegroundColor Yellow
$devDocsContent = Get-Content "docs/development-setup.md" -Raw
$devDocsContent = $devDocsContent -replace "your-username", $GitHubUsername
$devDocsContent | Set-Content "docs/development-setup.md" -Encoding UTF8
Write-Host "OK: Development docs updated" -ForegroundColor Green

# 4. Add all files to Git
Write-Host "SETUP: Adding files to Git..." -ForegroundColor Yellow
git add .
Write-Host "OK: Files added" -ForegroundColor Green

# 5. Create initial commit
$hasCommits = git log --oneline 2>$null
if (-not $hasCommits) {
    Write-Host "SETUP: Creating initial commit..." -ForegroundColor Yellow
    git commit -m "Initial commit: SimSynAI v1.0.0

- AI-powered simulation platform based on LLMs
- Support multiple LLMs: OpenAI, Anthropic, Google Gemini, Qwen, DeepSeek
- Docker containerization deployment
- Conda local development environment
- React + TypeScript frontend
- FastAPI + SQLAlchemy backend
- User authentication and authorization
- Intelligent chat system
- Simulation modeling features
- Data visualization
- Complete test coverage
- Detailed documentation
- CI/CD automation pipeline"
    Write-Host "OK: Initial commit created" -ForegroundColor Green
} else {
    Write-Host "INFO: Commits already exist, skipping initial commit" -ForegroundColor Cyan
}

# 6. Create or connect GitHub repository
if ($ghInstalled -and $CreateRepo) {
    Write-Host "SETUP: Creating repository using GitHub CLI..." -ForegroundColor Yellow
    try {
        gh repo create $RepoName --public --description "AI-powered simulation platform based on Large Language Models" --add-readme=false
        Write-Host "OK: GitHub repository created successfully" -ForegroundColor Green
        
        # Add remote repository
        git remote add origin "https://github.com/$GitHubUsername/$RepoName.git"
        Write-Host "OK: Remote repository connected" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to create GitHub repository" -ForegroundColor Red
        Write-Host "Please create repository manually: https://github.com/new" -ForegroundColor Yellow
    }
} else {
    Write-Host "INFO: Please complete the following steps manually:" -ForegroundColor Cyan
    Write-Host "1. Visit https://github.com/new to create a new repository" -ForegroundColor White
    Write-Host "2. Repository name: $RepoName" -ForegroundColor White
    Write-Host "3. Description: AI-powered simulation platform based on Large Language Models" -ForegroundColor White
    Write-Host "4. Set as Public" -ForegroundColor White
    Write-Host "5. Do not initialize README (we already have one)" -ForegroundColor White
    Write-Host ""
    Write-Host "After creating the repository, run the following command to connect remote:" -ForegroundColor Cyan
    Write-Host "git remote add origin https://github.com/$GitHubUsername/$RepoName.git" -ForegroundColor Yellow
}

# 7. Setup Git user info (if not configured)
$gitUser = git config --global user.name 2>$null
$gitEmail = git config --global user.email 2>$null

if (-not $gitUser) {
    Write-Host "WARNING: Please set Git username:" -ForegroundColor Yellow
    Write-Host "git config --global user.name `"Your Name`"" -ForegroundColor Cyan
}

if (-not $gitEmail) {
    Write-Host "WARNING: Please set Git email:" -ForegroundColor Yellow
    Write-Host "git config --global user.email `"your.email@example.com`"" -ForegroundColor Cyan
}

# 8. Check if remote repository is connected
$remoteOrigin = git remote get-url origin 2>$null
if ($remoteOrigin) {
    Write-Host "OK: Remote repository connected: $remoteOrigin" -ForegroundColor Green
    
    # Push to GitHub
    Write-Host "SETUP: Pushing code to GitHub..." -ForegroundColor Yellow
    try {
        git branch -M main
        git push -u origin main
        Write-Host "OK: Code pushed successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "SUCCESS: Project published to GitHub successfully!" -ForegroundColor Green
        Write-Host "Repository URL: https://github.com/$GitHubUsername/$RepoName" -ForegroundColor Cyan
    } catch {
        Write-Host "ERROR: Failed to push code, please check GitHub authentication" -ForegroundColor Red
        Write-Host "Tip: You may need to setup SSH keys or Personal Access Token" -ForegroundColor Yellow
    }
} else {
    Write-Host "WARNING: Remote repository not connected, please connect first" -ForegroundColor Yellow
}

# 9. Show next steps
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Setup GitHub Pages (if you need documentation site)" -ForegroundColor White
Write-Host "2. Configure GitHub Secrets (API keys and sensitive info)" -ForegroundColor White
Write-Host "3. Enable GitHub Actions (CI/CD already configured)" -ForegroundColor White
Write-Host "4. Add collaborators or setup team permissions" -ForegroundColor White
Write-Host "5. Create your first Release version" -ForegroundColor White
Write-Host ""
Write-Host "Version Release Commands:" -ForegroundColor Cyan
Write-Host ".\scripts\release.py patch   # Release patch version" -ForegroundColor Yellow
Write-Host ".\scripts\quick-publish.ps1  # Quick publish script" -ForegroundColor Yellow
Write-Host ""
Write-Host "Setup completed! Enjoy your development journey!" -ForegroundColor Green 