#!/bin/bash

echo "启动鹿鸣..."

cd "$(dirname "$0")"

cd backend
if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt -q

echo "启动后端服务..."
uvicorn main:app --reload --port 8000 &

cd ../frontend
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi

echo "启动前端服务..."
npm run dev

wait
