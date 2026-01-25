# ASD 检测统一后端系统


## 📁 项目结构

```
backend/
├── main.py              # FastAPI 后端界面
├── adapters.py          # 模型加载和预测适配器
├── requirements.txt     # Python 依赖
|—— webapp.py            # 前端
├── models/              # 模型文件目录
│   ├── autism_model.pkl           # 问卷预测模型
│   ├── scaler.pkl                 # 特征缩放器
│   ├── label_encoders.pkl         # 标签编码器
│   └── autism_behavior_mobilenet_v2.keras  # 图片分类模型
└── config/
    └── class_names.json # 图片分类标签
```

## 快速开始

###  启动后端服务

```bash
# 启动虚拟环境


# 启动 FastAPI 服务器
uvicorn backend.main:app 
```

服务器启动后访问：
- **API 文档**: http://localhost:8000/docs (Swagger UI)
- **API 根路径**: http://localhost:8000/

### 前端启动
```bash
python backend/webapp.py
```


## 技术栈

- **后端框架**: FastAPI 0.95.2
- **Web服务器**: Uvicorn
- **问卷模型**: XGBoost + scikit-learn (pkl格式)
- **图片模型**: best(pytorch)
- **图片处理**: Pillow
- **数据处理**: NumPy, Pandas



## 使用 Swagger UI

1. 启动服务器后访问 http://localhost:8000/docs
2. 点击任意端点的 "Try it out" 按钮
3. 填写请求参数或上传文件
4. 点击 "Execute" 查看结果
  
**后端地址**: http://localhost:8000
