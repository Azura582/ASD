# ASD检测系统 - 统一Web应用

完整的自闭症谱系障碍检测系统，整合问卷检测和图片行为识别。

## 功能特性

### 1. 问卷检测
- 10道标准化筛查问题
- 基于行为观察和发展特征评估
- 科学的风险评分系统
- 即时生成检测报告

### 2. 图片检测
- 上传儿童行为照片
- AI识别典型自闭症行为模式:
  - 头部撞击 (head_banging)
  - 原地旋转 (spinning)
  - 手部拍动 (hand_flapping)
- 深度学习MobileNetV2模型
- 提供置信度评分

## 系统架构

```
medicine/
├── backend/
│   ├── adapters.py      # 模型加载和预测适配器
│   ├── api.py           # FastAPI后端接口
│   ├── webapp.py        # Flask前端应用
│   ├── templates/       # HTML模板
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── survey.html
│   │   └── image.html
│   ├── static/          # 静态资源
│   ├── models/          # 模型文件
│   └── requirements.txt
├── AI ASD Detector/     # 问卷模型源码
│   └── Code/
│       ├── autism_model.pkl
│       ├── scaler.pkl
│       └── label_encoders.pkl
└── autism-spectrum-disorder-detection/  # 图片模型源码
    ├── models/
    │   └── autism_behavior_mobilenet_v2.keras
    └── config/
        └── class_names.json
```

## 快速开始

### 1. 一键启动（推荐）

```bash
chmod +x start.sh
./start.sh
```

启动后访问:
- 前端界面: http://localhost:5000
- API文档: http://localhost:8000/docs

### 2. 手动启动

```bash
# 激活虚拟环境
source myenv/bin/activate

# 安装依赖
pip install -r backend/requirements.txt

# 终端1: 启动FastAPI后端
python3 -m uvicorn backend.api:app --host 0.0.0.0 --port 8000

# 终端2: 启动Flask前端
python3 backend/webapp.py
```

## API接口文档

### FastAPI后端 (端口8000)

#### 健康检查
```http
GET /health
```

#### 查看模型状态
```http
GET /models
```

响应示例:
```json
{
  "survey_model_loaded": true,
  "image_model_loaded": true,
  "class_names": ["head_banging", "spinning", "hand_flapping"],
  "class_names_count": 3
}
```

#### 问卷预测
```http
POST /predict/survey
Content-Type: application/json

{
  "age": 36,
  "sex": "Male",
  "ethnicity": "Others",
  "jaundice": "no",
  "asd_history": "no",
  "respondent": "Parent",
  "Q1": {"answer": "Yes"},
  "Q2": {"answer": "No"},
  ...
  "Q10": {"answer": "Yes"}
}
```

响应示例:
```json
{
  "prediction": "Yes",
  "risk_questions": ["Q2", "Q3", "Q5"],
  "score": 6,
  "risk_level": "中风险"
}
```

#### 图片预测
```http
POST /predict/image
Content-Type: multipart/form-data

file: <image_file>
```

响应示例:
```json
{
  "label": "hand_flapping",
  "score": 0.92,
  "confidence": "92.00%",
  "all_probabilities": {
    "head_banging": 0.03,
    "spinning": 0.05,
    "hand_flapping": 0.92
  }
}
```

## 模型文件要求

确保以下文件存在:

### 问卷模型 (3个pkl文件)
- `AI ASD Detector/Code/autism_model.pkl`
- `AI ASD Detector/Code/scaler.pkl`
- `AI ASD Detector/Code/label_encoders.pkl`

### 图片模型 (1个keras文件)
- `autism-spectrum-disorder-detection/models/autism_behavior_mobilenet_v2.keras`
- `autism-spectrum-disorder-detection/config/class_names.json`

## 技术栈

- **后端API**: FastAPI 0.104.1
- **前端**: Flask 3.0.0 + Bootstrap 5.3
- **ML框架**: TensorFlow-CPU 2.15.0, scikit-learn 1.3.2, XGBoost 2.0.2
- **深度学习**: Keras 2.15.0 (MobileNetV2模型)

## 模块化设计

系统采用模块化设计，方便后续扩展:

1. **adapters.py**: 统一的模型适配器接口
   - `load_adapters()`: 启动时加载所有模型
   - `predict_survey()`: 问卷预测接口
   - `predict_image()`: 图片预测接口
   - `get_models_info()`: 模型状态查询

2. **api.py**: RESTful API层
   - 独立的FastAPI服务
   - 自动生成OpenAPI文档
   - CORS支持

3. **webapp.py**: Web前端层
   - Flask应用
   - Bootstrap响应式界面
   - Ajax异步通信

### 添加新模型示例

在`adapters.py`中添加:

```python
def predict_video(video_bytes: bytes) -> dict:
    """视频预测接口"""
    # 实现视频模型加载和预测逻辑
    pass
```

在`api.py`中添加路由:

```python
@app.post("/predict/video")
async def predict_video(file: UploadFile = File(...)):
    content = await file.read()
    res = adapters.predict_video(content)
    return JSONResponse(res)
```

## 注意事项

1. **CPU模式**: 系统默认使用CPU模式运行(CUDA_VISIBLE_DEVICES=""),避免GPU驱动问题
2. **内存占用**: 图片模型约100MB,问卷模型约10MB
3. **推理速度**: 
   - 问卷预测: < 100ms
   - 图片预测: 1-3秒(CPU模式)
4. **免责声明**: 本系统仅供筛查参考,不能替代专业医疗诊断

## 故障排查

### 模型加载失败
```bash
# 检查模型文件是否存在
ls -lh "AI ASD Detector/Code/"*.pkl
ls -lh "autism-spectrum-disorder-detection/models/"*.keras

# 查看启动日志
# 应看到: [adapters] ✓ 问卷模型已加载 (3个pkl文件)
#         [adapters] ✓ 图片模型已加载
```

### 前端连接后端失败
```bash
# 确认后端正在运行
curl http://localhost:8000/health

# 检查环境变量
export API_BASE="http://localhost:8000"
```

### 依赖安装问题
```bash
# 升级pip
pip install --upgrade pip

# 清理缓存重装
pip cache purge
pip install -r backend/requirements.txt --no-cache-dir
```

## 开发团队

如有问题或建议,请提交Issue或联系开发团队。

---

**重要提示**: 本系统用于研究和辅助筛查目的,不应作为临床诊断的唯一依据。如怀疑儿童有ASD症状,请及时就医并咨询专业医生。
