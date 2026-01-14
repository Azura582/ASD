# ASD 检测统一后端系统


## 📁 项目结构

```
backend/
├── main.py              # FastAPI 主应用
├── adapters.py          # 模型加载和预测适配器
├── test_api.py          # API 完整测试脚本
├── requirements.txt     # Python 依赖
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
# 激活虚拟环境
source myenv/bin/activate

# 启动 FastAPI 服务器
cd /home/azura/code/medicine
uvicorn backend.main:app 
```

服务器启动后访问：
- **API 文档**: http://localhost:8000/docs (Swagger UI)
- **API 根路径**: http://localhost:8000/


## 📡 API 端点

### 1. 健康检查
```bash
GET /health
```
返回: `{"status": "ok"}`

### 2. 模型状态
```bash
GET /models
```
返回当前加载的模型信息。

### 3. 问卷评估
```bash
POST /predict/survey
Content-Type: application/json

{
  "age": 36,
  "sex": "Male",
  "ethnicity": "Other",
  "jaundice": "no",
  "asd_history": "no",
  "respondent": "parent",
  "Q1": {"answer": "Yes"},
  "Q2": {"answer": "No"},
  ...
  "Q10": {"answer": "Yes"}
}
```

返回示例:
```json
{
  "prediction": "Yes",
  "risk_questions": ["Q2", "Q3", "Q5", "Q6", "Q9", "Q10"],
  "score": 6,
  "risk_level": "中风险"
}
```

### 4. 图片分类
```bash
POST /predict/image
Content-Type: multipart/form-data
```

上传图片文件，返回行为分类结果：

```json
{
  "label": "spinning",
  "score": 0.9272,
  "confidence": "92.72%",
  "all_probabilities": {
    "head_banging": 0.0724,
    "spinning": 0.9272,
    "hand_flapping": 0.0004
  }
}
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
- 输入: 年龄、性别、种族等基本信息 + 10个ASD筛查问题
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
