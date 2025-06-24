#!/bin/bash
# SimSynAI 开发环境启动脚本 (Linux/macOS)
# 使用conda虚拟环境启动开发服务

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# 默认模式
MODE=${1:-full}

echo -e "${GREEN}🚀 SimSynAI 开发环境启动脚本${NC}"
echo -e "${BLUE}模式: ${MODE}${NC}"
echo -e "${GREEN}=================================${NC}"

# 检查conda是否安装
if ! command -v conda &> /dev/null; then
    echo -e "${RED}❌ Conda未安装，请先安装Anaconda或Miniconda:${NC}"
    echo -e "${YELLOW}   macOS: brew install --cask miniconda${NC}"
    echo -e "${YELLOW}   Linux: wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh${NC}"
    exit 1
fi

CONDA_VERSION=$(conda --version)
echo -e "${GREEN}✅ Conda已安装: ${CONDA_VERSION}${NC}"

# 检查是否在项目根目录
if [ ! -f "environment.yml" ]; then
    echo -e "${RED}❌ 请在项目根目录运行此脚本${NC}"
    exit 1
fi

# 检查conda环境是否存在
if ! conda env list | grep -q "simsynai"; then
    echo -e "${YELLOW}🔧 创建conda环境...${NC}"
    if conda env create -f environment.yml; then
        echo -e "${GREEN}✅ Conda环境创建成功${NC}"
    else
        echo -e "${RED}❌ Conda环境创建失败${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Conda环境已存在${NC}"
fi

# 初始化conda（如果需要）
eval "$(conda shell.bash hook)" 2>/dev/null || true

# 根据模式执行不同操作
case $MODE in
    "init")
        echo -e "${YELLOW}🔧 初始化开发环境...${NC}"
        
        # 创建初始化脚本
        cat > temp_init.py << 'EOF'
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
EOF
        
        # 运行初始化
        conda run -n simsynai python temp_init.py
        rm temp_init.py
        
        echo -e "${GREEN}✅ 环境初始化完成！${NC}"
        echo -e "${CYAN}💡 使用以下命令启动开发服务:${NC}"
        echo -e "${WHITE}   ./scripts/dev-start.sh backend   # 启动后端${NC}"
        echo -e "${WHITE}   ./scripts/dev-start.sh frontend  # 启动前端${NC}"
        echo -e "${WHITE}   ./scripts/dev-start.sh full      # 启动全部服务${NC}"
        ;;
        
    "backend")
        echo -e "${YELLOW}🐍 启动后端服务...${NC}"
        echo -e "${CYAN}📍 后端服务地址: http://localhost:8000${NC}"
        echo -e "${CYAN}📚 API文档地址: http://localhost:8000/docs${NC}"
        echo -e "${YELLOW}按 Ctrl+C 停止服务${NC}"
        echo ""
        
        cd backend
        conda run -n simsynai uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
        ;;
        
    "frontend")
        echo -e "${YELLOW}⚛️  启动前端服务...${NC}"
        echo -e "${CYAN}📍 前端服务地址: http://localhost:3000${NC}"
        echo -e "${YELLOW}按 Ctrl+C 停止服务${NC}"
        echo ""
        
        if [ ! -d "frontend/node_modules" ]; then
            echo -e "${YELLOW}📦 安装前端依赖...${NC}"
            cd frontend
            pnpm install
            cd ..
        fi
        
        cd frontend
        pnpm start
        ;;
        
    "full")
        echo -e "${YELLOW}🚀 启动完整开发环境...${NC}"
        echo -e "${CYAN}将在后台启动前后端服务${NC}"
        echo ""
        
        # 检查终端是否支持job control
        if [[ $- == *i* ]]; then
            # 交互式shell，支持后台任务
            echo -e "${YELLOW}📦 启动后端服务...${NC}"
            cd backend
            conda run -n simsynai uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
            BACKEND_PID=$!
            cd ..
            
            # 等待后端启动
            sleep 3
            
            echo -e "${YELLOW}📦 启动前端服务...${NC}"
            if [ ! -d "frontend/node_modules" ]; then
                echo -e "${YELLOW}📦 安装前端依赖...${NC}"
                cd frontend
                pnpm install
                cd ..
            fi
            
            cd frontend
            pnpm start &
            FRONTEND_PID=$!
            cd ..
            
            echo -e "${GREEN}✅ 服务启动完成！${NC}"
            echo -e "${CYAN}📍 前端地址: http://localhost:3000${NC}"
            echo -e "${CYAN}📍 后端地址: http://localhost:8000${NC}"
            echo -e "${CYAN}📚 API文档: http://localhost:8000/docs${NC}"
            echo -e "${YELLOW}按 Ctrl+C 停止所有服务${NC}"
            
            # 等待用户中断
            trap "echo -e '\n${YELLOW}正在停止服务...${NC}'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true; exit" INT
            wait
        else
            # 非交互式shell，使用tmux或screen
            if command -v tmux &> /dev/null; then
                echo -e "${YELLOW}使用tmux启动服务...${NC}"
                
                # 创建新的tmux会话
                tmux new-session -d -s simsynai
                
                # 在第一个窗口启动后端
                tmux send-keys -t simsynai "cd $(pwd)/backend && conda activate simsynai && uvicorn app.main:app --reload" Enter
                
                # 创建新窗口并启动前端
                tmux new-window -t simsynai
                tmux send-keys -t simsynai "cd $(pwd)/frontend && pnpm start" Enter
                
                echo -e "${GREEN}✅ 服务已在tmux中启动！${NC}"
                echo -e "${CYAN}使用 'tmux attach -t simsynai' 查看服务状态${NC}"
                echo -e "${CYAN}使用 'tmux kill-session -t simsynai' 停止所有服务${NC}"
            else
                echo -e "${YELLOW}⚠️  建议安装tmux以便更好地管理多个服务${NC}"
                echo -e "${YELLOW}请在不同终端窗口中分别运行:${NC}"
                echo -e "${WHITE}   ./scripts/dev-start.sh backend${NC}"
                echo -e "${WHITE}   ./scripts/dev-start.sh frontend${NC}"
            fi
        fi
        ;;
        
    *)
        echo -e "${RED}❌ 无效的模式: ${MODE}${NC}"
        echo -e "${YELLOW}可用模式: init, backend, frontend, full${NC}"
        echo -e "${YELLOW}用法: $0 [模式]${NC}"
        echo -e "${YELLOW}示例: $0 backend${NC}"
        exit 1
        ;;
esac 