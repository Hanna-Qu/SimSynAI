#!/bin/bash
# SimSynAI 快速发布到GitHub脚本 (Bash)
# 此脚本将帮助您快速将项目发布到GitHub

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# 参数检查
if [ -z "$1" ]; then
    echo -e "${RED}❌ 请提供GitHub仓库URL${NC}"
    echo -e "${YELLOW}用法: $0 <仓库URL> [提交信息]${NC}"
    echo -e "${YELLOW}示例: $0 https://github.com/your-username/SimSynAI.git${NC}"
    exit 1
fi

REPO_URL="$1"
COMMIT_MESSAGE="${2:-feat: 初始项目提交 - SimSynAI v1.0.0}"

echo -e "${GREEN}🚀 SimSynAI GitHub 发布脚本${NC}"
echo -e "${GREEN}=================================${NC}"

# 检查Git是否安装
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git未安装，请先安装Git:${NC}"
    echo -e "${YELLOW}   macOS: brew install git${NC}"
    echo -e "${YELLOW}   Ubuntu: sudo apt install git${NC}"
    echo -e "${YELLOW}   CentOS: sudo yum install git${NC}"
    exit 1
fi

GIT_VERSION=$(git --version)
echo -e "${GREEN}✅ Git已安装: ${GIT_VERSION}${NC}"

# 检查是否在项目根目录
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ 请在项目根目录运行此脚本${NC}"
    exit 1
fi

echo -e "${BLUE}📁 当前目录: $(pwd)${NC}"

# 初始化Git仓库
echo -e "${YELLOW}🔧 初始化Git仓库...${NC}"
if git init > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Git仓库初始化成功${NC}"
else
    echo -e "${RED}❌ Git仓库初始化失败${NC}"
    exit 1
fi

# 添加所有文件
echo -e "${YELLOW}📝 添加文件到Git...${NC}"
if git add .; then
    echo -e "${GREEN}✅ 文件添加成功${NC}"
else
    echo -e "${RED}❌ 文件添加失败${NC}"
    exit 1
fi

# 创建初始提交
echo -e "${YELLOW}💾 创建初始提交...${NC}"
if git commit -m "$COMMIT_MESSAGE"; then
    echo -e "${GREEN}✅ 初始提交创建成功${NC}"
else
    echo -e "${RED}❌ 提交创建失败${NC}"
    exit 1
fi

# 添加远程仓库
echo -e "${YELLOW}🌐 添加远程仓库...${NC}"
if git remote add origin "$REPO_URL" 2>/dev/null; then
    echo -e "${GREEN}✅ 远程仓库添加成功: ${REPO_URL}${NC}"
else
    echo -e "${YELLOW}⚠️  远程仓库可能已存在${NC}"
fi

# 设置主分支
echo -e "${YELLOW}🌿 设置主分支...${NC}"
if git branch -M main; then
    echo -e "${GREEN}✅ 主分支设置成功${NC}"
else
    echo -e "${RED}❌ 主分支设置失败${NC}"
    exit 1
fi

# 推送到GitHub
echo -e "${YELLOW}🚀 推送到GitHub...${NC}"
echo -e "${CYAN}   如果提示输入用户名和密码，建议使用Personal Access Token${NC}"
if git push -u origin main; then
    echo -e "${GREEN}✅ 推送成功!${NC}"
else
    echo -e "${RED}❌ 推送失败，可能需要验证身份${NC}"
    echo -e "${YELLOW}   请检查:${NC}"
    echo -e "${YELLOW}   1. GitHub仓库是否存在${NC}"
    echo -e "${YELLOW}   2. 用户名和密码/Token是否正确${NC}"
    echo -e "${YELLOW}   3. 网络连接是否正常${NC}"
    exit 1
fi

# 创建版本标签
echo -e "${YELLOW}🏷️  创建版本标签...${NC}"
if git tag -a v1.0.0 -m "发布版本 1.0.0" && git push origin v1.0.0; then
    echo -e "${GREEN}✅ 版本标签 v1.0.0 创建并推送成功${NC}"
else
    echo -e "${YELLOW}⚠️  版本标签创建失败，但项目已成功推送${NC}"
fi

echo ""
echo -e "${GREEN}🎉 恭喜！SimSynAI项目已成功发布到GitHub!${NC}"
echo -e "${GREEN}=================================${NC}"
echo -e "${BLUE}📋 下一步操作建议:${NC}"
echo -e "${WHITE}   1. 访问您的GitHub仓库查看项目${NC}"
echo -e "${WHITE}   2. 在仓库设置中配置分支保护规则${NC}"
echo -e "${WHITE}   3. 启用GitHub Actions自动化流程${NC}"
echo -e "${WHITE}   4. 添加项目描述和主题标签${NC}"
echo -e "${WHITE}   5. 创建第一个Release版本${NC}"
echo ""
echo -e "${CYAN}📚 详细指南请参考: docs/github-setup.md${NC}"
echo -e "${CYAN}🔧 版本管理脚本: scripts/release.py${NC}" 