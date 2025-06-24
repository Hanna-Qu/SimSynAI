# SimSynAI 开发环境启动脚本 (Windows PowerShell)
# 使用conda虚拟环境启动开发服务

param(
    [Parameter(Mandatory=$false)]
    [string]$Mode = "full"  # full, backend, frontend, init
)

Write-Host "🚀 SimSynAI 开发环境启动脚本" -ForegroundColor Green
Write-Host "模式: $Mode" -ForegroundColor Blue
Write-Host "=================================" -ForegroundColor Green

# 检查conda是否安装
try {
    $condaVersion = conda --version
    Write-Host "✅ Conda已安装: $condaVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Conda未安装，请先安装Anaconda或Miniconda:" -ForegroundColor Red
    Write-Host "   下载地址: https://www.anaconda.com/products/distribution" -ForegroundColor Yellow
    exit 1
}

# 检查是否在项目根目录
if (-not (Test-Path "environment.yml")) {
    Write-Host "❌ 请在项目根目录运行此脚本" -ForegroundColor Red
    exit 1
}

# 检查conda环境是否存在
$envExists = conda env list | Select-String "simsynai"
if (-not $envExists) {
    Write-Host "🔧 创建conda环境..." -ForegroundColor Yellow
    try {
        conda env create -f environment.yml
        Write-Host "✅ Conda环境创建成功" -ForegroundColor Green
    } catch {
        Write-Host "❌ Conda环境创建失败" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ Conda环境已存在" -ForegroundColor Green
}

# 根据模式执行不同操作
switch ($Mode) {
    "init" {
        Write-Host "🔧 初始化开发环境..." -ForegroundColor Yellow
        
        # 激活环境并初始化数据库
        Write-Host "📦 初始化数据库..." -ForegroundColor Yellow
        $initScript = @"
import os
import sys
sys.path.append('backend')

from app.db.session import create_db_and_tables
from app.db.init_db import init_db
from app.db.session import SessionLocal

# 创建表
create_db_and_tables()
print('✅ 数据库表创建完成')

# 初始化默认用户
db = SessionLocal()
try:
    init_db(db)
    print('✅ 默认用户创建完成')
finally:
    db.close()
"@
        
        # 保存初始化脚本到临时文件
        $tempScript = "temp_init.py"
        $initScript | Out-File -FilePath $tempScript -Encoding UTF8
        
        # 运行初始化
        conda run -n simsynai python $tempScript
        Remove-Item $tempScript
        
        Write-Host "✅ 环境初始化完成！" -ForegroundColor Green
        Write-Host "💡 使用以下命令启动开发服务:" -ForegroundColor Cyan
        Write-Host "   .\scripts\dev-start.ps1 backend   # 启动后端" -ForegroundColor White
        Write-Host "   .\scripts\dev-start.ps1 frontend  # 启动前端" -ForegroundColor White
        Write-Host "   .\scripts\dev-start.ps1 full      # 启动全部服务" -ForegroundColor White
    }
    
    "backend" {
        Write-Host "🐍 启动后端服务..." -ForegroundColor Yellow
        Write-Host "📍 后端服务地址: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "📚 API文档地址: http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
        Write-Host ""
        
        Set-Location backend
        conda run -n simsynai uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    }
    
    "frontend" {
        Write-Host "⚛️  启动前端服务..." -ForegroundColor Yellow
        Write-Host "📍 前端服务地址: http://localhost:3000" -ForegroundColor Cyan
        Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
        Write-Host ""
        
        if (-not (Test-Path "frontend\node_modules")) {
            Write-Host "📦 安装前端依赖..." -ForegroundColor Yellow
            Set-Location frontend
            pnpm install
            Set-Location ..
        }
        
        Set-Location frontend
        pnpm start
    }
    
    "full" {
        Write-Host "🚀 启动完整开发环境..." -ForegroundColor Yellow
        Write-Host "将在新窗口中启动前后端服务" -ForegroundColor Cyan
        Write-Host ""
        
        # 在新窗口启动后端
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\scripts\dev-start.ps1 backend"
        
        # 等待2秒后启动前端
        Start-Sleep -Seconds 2
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\scripts\dev-start.ps1 frontend"
        
        Write-Host "✅ 服务启动完成！" -ForegroundColor Green
        Write-Host "📍 前端地址: http://localhost:3000" -ForegroundColor Cyan
        Write-Host "📍 后端地址: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "📚 API文档: http://localhost:8000/docs" -ForegroundColor Cyan
    }
    
    default {
        Write-Host "❌ 无效的模式: $Mode" -ForegroundColor Red
        Write-Host "可用模式: init, backend, frontend, full" -ForegroundColor Yellow
        exit 1
    }
} 