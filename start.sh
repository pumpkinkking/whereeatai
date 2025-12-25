#!/bin/bash

# WhereEatAI 启动脚本 (Linux/macOS)

set -e

echo "======================================"
echo "  WhereEatAI 智能旅游推荐系统"
echo "======================================"
echo ""

# 检查Python版本
echo "检查Python版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python版本: $python_version"

# 检查是否存在虚拟环境
if [ ! -d "venv" ]; then
    echo ""
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo ""
echo "检查并安装依赖..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# 检查.env文件
if [ ! -f ".env" ]; then
    echo ""
    echo "警告: .env文件不存在"
    echo "正在复制.env.example到.env..."
    cp .env.example .env
    echo ""
    echo "请编辑.env文件并填入你的API_KEY"
    echo "编辑完成后重新运行此脚本"
    exit 1
fi

# 检查API_KEY
if ! grep -q "your_siliconflow_api_key" .env; then
    echo ""
    echo "✓ API配置已完成"
else
    echo ""
    echo "警告: 请在.env文件中配置API_KEY"
    echo "编辑.env文件并将your_siliconflow_api_key替换为实际的API密钥"
    exit 1
fi

# 创建日志目录
mkdir -p logs

echo ""
echo "======================================"
echo "  启动服务..."
echo "======================================"
echo ""

# 启动应用
python main.py
