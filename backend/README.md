# 统一 ASD 检测后端

本后端提供一个基于 FastAPI 的轻量服务，整合了仓库中多个与自闭症谱系障碍（ASD）相关的模型与脚本，并对外暴露统一的接口。

接口（Endpoints）
- GET /health
- GET /version
- POST /predict/image  （multipart 文件）
- POST /predict/video  （multipart 文件）
- POST /predict/survey （JSON，格式：{ "data": {...} }）
- GET /models

快速开始（本地，Python）

1. 创建并激活虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

2. 在仓库根目录运行服务：

```bash
python -m backend.main
```

3. 打开交互式文档：

访问 http://localhost:8000/docs 查看并测试 API。

Docker（可选）

在 `backend` 文件夹的上级目录（仓库根）使用 docker-compose 构建并运行：

```bash
docker compose -f backend/docker-compose.yml up --build
```

注意事项
- 适配器加载器（`backend/adapters.py`）会尝试在仓库中查找现有脚本和模型文件。如果你移动或重命名了这些文件，请相应更新适配器中的路径。
- 对于大型视频文件或生产级负载，建议使用任务队列（例如 Celery 或 RQ）并配合持久化的上传存储，以避免阻塞请求和占用大量内存/CPU。

