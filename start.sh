#!/bin/bash
# 启动脚本 - 同时运行FastAPI后端和Flask前端

echo "🚀 启动ASD检测系统..."

# 检查虚拟环境
if [ ! -d "myenv" ]; then
    echo "❌ 未找到虚拟环境myenv，请先创建: python3 -m venv myenv"
    exit 1
fi

# 激活虚拟环境
source myenv/bin/activate

# 安装依赖
echo "📦 检查依赖..."
pip install -q -r backend/requirements.txt

# 启动FastAPI后端 (端口8000)
echo "🔧 启动FastAPI后端 (http://localhost:8000)..."
python3 -m uvicorn backend.api:app --host 0.0.0.0 --port 8000 &
API_PID=$!

# 等待后端启动
sleep 3

# 启动Flask前端 (端口5000)
echo "🌐 启动Flask前端 (http://localhost:5000)..."
python3 backend/webapp.py &
WEBAPP_PID=$!

echo ""
echo "✅ 系统启动成功！"
echo ""
echo "📊 访问地址:"
echo "   - 前端界面: http://localhost:5000"
echo "   - API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo ""

# 等待用户中断
trap "kill $API_PID $WEBAPP_PID; echo ''; echo '🛑 服务已停止'; exit 0" INT
wait
