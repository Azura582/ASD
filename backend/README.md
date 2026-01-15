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
- **图片模型**: MobileNetV2 (Keras/TensorFlow)
- **图片处理**: Pillow
- **数据处理**: NumPy, Pandas

## 模型说明

### 问卷模型
- 输入: 年龄、性别、种族等基本信息 + ASD筛查问题
- 输出: ASD风险预测 (Yes/No)、风险分数 (0-10)、风险等级 (低/中/高)
- 文件: 3个pkl文件 (模型、缩放器、编码器)

### 图片模型
- 输入: RGB图片 (自动调整为128x128)
- 输出: 3种自闭症行为分类
  - head_banging (头部撞击)
  - spinning (旋转)
  - hand_flapping (手部拍打)
- 架构: MobileNetV2
- 文件: autism_behavior_mobilenet_v2.keras


## 使用 Swagger UI

1. 启动服务器后访问 http://localhost:8000/docs
2. 点击任意端点的 "Try it out" 按钮
3. 填写请求参数或上传文件
4. 点击 "Execute" 查看结果
  
**后端地址**: http://localhost:8000
