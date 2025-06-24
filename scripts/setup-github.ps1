# GitHub仓库快速设置脚本 (Windows PowerShell)
# 用于初始化项目并发布到GitHub

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername,
    
    [Parameter(Mandatory=$false)]
    [string]$RepoName = "SimSynAI",
    
    [Parameter(Mandatory=$false)]
    [switch]$CreateRepo = $false
)

Write-Host "GitHub仓库设置脚本" -ForegroundColor Green
Write-Host "用户名: $GitHubUsername" -ForegroundColor Blue
Write-Host "仓库名: $RepoName" -ForegroundColor Blue
Write-Host "=================================" -ForegroundColor Green

# 检查是否在项目根目录
if (-not (Test-Path "VERSION")) {
    Write-Host "ERROR: 请在项目根目录运行此脚本" -ForegroundColor Red
    exit 1
}

# 检查git是否安装
try {
    $gitVersion = git --version
    Write-Host "OK: Git已安装: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git未安装，请先安装Git:" -ForegroundColor Red
    Write-Host "   下载地址: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# 检查GitHub CLI是否安装（可选）
$ghInstalled = $false
try {
    $ghVersion = gh --version
    Write-Host "OK: GitHub CLI已安装: $ghVersion" -ForegroundColor Green
    $ghInstalled = $true
} catch {
    Write-Host "WARNING: GitHub CLI未安装，将使用手动方式" -ForegroundColor Yellow
    Write-Host "   推荐安装: winget install GitHub.cli" -ForegroundColor Cyan
}

# 1. 初始化Git仓库（如果还没有的话）
if (-not (Test-Path ".git")) {
    Write-Host "SETUP: 初始化Git仓库..." -ForegroundColor Yellow
    git init
    Write-Host "OK: Git仓库初始化完成" -ForegroundColor Green
} else {
    Write-Host "OK: Git仓库已存在" -ForegroundColor Green
}

# 2. 更新README中的用户名
Write-Host "SETUP: 更新README中的GitHub链接..." -ForegroundColor Yellow
$readmeContent = Get-Content "README.md" -Raw
$readmeContent = $readmeContent -replace "your-username", $GitHubUsername
$readmeContent | Set-Content "README.md"
Write-Host "OK: README更新完成" -ForegroundColor Green

# 3. 更新开发文档中的链接
Write-Host "SETUP: 更新开发文档中的GitHub链接..." -ForegroundColor Yellow
$devDocsContent = Get-Content "docs/development-setup.md" -Raw
$devDocsContent = $devDocsContent -replace "your-username", $GitHubUsername
$devDocsContent | Set-Content "docs/development-setup.md"
Write-Host "OK: 开发文档更新完成" -ForegroundColor Green

# 4. 添加所有文件到Git
Write-Host "SETUP: 添加文件到Git..." -ForegroundColor Yellow
git add .
Write-Host "OK: 文件添加完成" -ForegroundColor Green

# 5. 创建初始提交
$hasCommits = git log --oneline 2>$null
if (-not $hasCommits) {
    Write-Host "SETUP: 创建初始提交..." -ForegroundColor Yellow
    git commit -m "Initial commit: SimSynAI v1.0.0

- 基于大语言模型的智能化仿真平台
- 支持多种LLM：OpenAI、Anthropic、Google Gemini、千问、DeepSeek
- Docker容器化部署
- Conda本地开发环境
- React + TypeScript前端
- FastAPI + SQLAlchemy后端
- 用户认证和权限管理
- 智能对话系统
- 仿真建模功能
- 数据可视化
- 完整的测试覆盖
- 详细的文档说明
- CI/CD自动化流程"
    Write-Host "OK: 初始提交完成" -ForegroundColor Green
} else {
    Write-Host "INFO: 已存在提交记录，跳过初始提交" -ForegroundColor Cyan
}

# 6. 创建或连接GitHub仓库
if ($ghInstalled -and $CreateRepo) {
    Write-Host "SETUP: 使用GitHub CLI创建仓库..." -ForegroundColor Yellow
    try {
        gh repo create $RepoName --public --description "基于大语言模型的智能化仿真平台" --add-readme=false
        Write-Host "OK: GitHub仓库创建成功" -ForegroundColor Green
        
        # 添加远程仓库
        git remote add origin "https://github.com/$GitHubUsername/$RepoName.git"
        Write-Host "OK: 远程仓库连接成功" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: GitHub仓库创建失败" -ForegroundColor Red
        Write-Host "请手动在GitHub上创建仓库：https://github.com/new" -ForegroundColor Yellow
    }
} else {
    Write-Host "INFO: 请手动完成以下步骤:" -ForegroundColor Cyan
    Write-Host "1. 访问 https://github.com/new 创建新仓库" -ForegroundColor White
    Write-Host "2. 仓库名: $RepoName" -ForegroundColor White
    Write-Host "3. 描述: 基于大语言模型的智能化仿真平台" -ForegroundColor White
    Write-Host "4. 设置为Public" -ForegroundColor White
    Write-Host "5. 不要初始化README（我们已经有了）" -ForegroundColor White
    Write-Host ""
    Write-Host "仓库创建后，运行以下命令连接远程仓库:" -ForegroundColor Cyan
    Write-Host "git remote add origin https://github.com/$GitHubUsername/$RepoName.git" -ForegroundColor Yellow
}

# 7. 设置Git用户信息（如果没有的话）
$gitUser = git config --global user.name 2>$null
$gitEmail = git config --global user.email 2>$null

if (-not $gitUser) {
    Write-Host "WARNING: 请设置Git用户名:" -ForegroundColor Yellow
    Write-Host "git config --global user.name `"Your Name`"" -ForegroundColor Cyan
}

if (-not $gitEmail) {
    Write-Host "WARNING: 请设置Git邮箱:" -ForegroundColor Yellow
    Write-Host "git config --global user.email `"your.email@example.com`"" -ForegroundColor Cyan
}

# 8. 检查是否有远程仓库连接
$remoteOrigin = git remote get-url origin 2>$null
if ($remoteOrigin) {
    Write-Host "OK: 远程仓库已连接: $remoteOrigin" -ForegroundColor Green
    
    # 推送到GitHub
    Write-Host "SETUP: 推送代码到GitHub..." -ForegroundColor Yellow
    try {
        git branch -M main
        git push -u origin main
        Write-Host "OK: 代码推送成功！" -ForegroundColor Green
        Write-Host ""
        Write-Host "SUCCESS: 项目已成功发布到GitHub！" -ForegroundColor Green
        Write-Host "仓库地址: https://github.com/$GitHubUsername/$RepoName" -ForegroundColor Cyan
    } catch {
        Write-Host "ERROR: 代码推送失败，请检查GitHub认证" -ForegroundColor Red
        Write-Host "提示: 可能需要设置SSH密钥或Personal Access Token" -ForegroundColor Yellow
    }
} else {
    Write-Host "WARNING: 远程仓库未连接，请先连接远程仓库" -ForegroundColor Yellow
}

# 9. 显示后续步骤
Write-Host ""
Write-Host "后续步骤建议:" -ForegroundColor Cyan
Write-Host "1. 设置GitHub Pages（如果需要文档站点）" -ForegroundColor White
Write-Host "2. 配置GitHub Secrets（API密钥等敏感信息）" -ForegroundColor White
Write-Host "3. 启用GitHub Actions（CI/CD已配置）" -ForegroundColor White
Write-Host "4. 添加协作者或设置团队权限" -ForegroundColor White
Write-Host "5. 创建第一个Release版本" -ForegroundColor White
Write-Host ""
Write-Host "版本发布命令:" -ForegroundColor Cyan
Write-Host ".\scripts\release.py patch   # 发布补丁版本" -ForegroundColor Yellow
Write-Host ".\scripts\quick-publish.ps1  # 快速发布脚本" -ForegroundColor Yellow
Write-Host ""
Write-Host "设置完成！享受您的开发之旅！" -ForegroundColor Green 