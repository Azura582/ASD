# 统一 ASD 检测后端

本后端提供一个基于 FastAPI 的轻量服务,整合了仓库中多个与自闭症谱系障碍(ASD)相关的模型与脚本,并对外暴露统一的接口。

## 支持的模型
- **问卷调查模型**: 使用 3 个 pkl 文件(model, scaler, label_encoders)进行 ASD 风险评估
- **图像分类模型**: 使用 MobileNetV2 Keras 模型识别自闭症行为(head_banging, spinning, hand_flapping)

## API 接口
- `GET /health` - 健康检查
- `GET /version` - 版本信息
- `GET /models` - 查看已加载的模型状态
- `POST /predict/image` - 图像行为检测(multipart 文件上传)
- `POST /predict/survey` - 问卷风险评估(JSON 格式)

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

## 模型文件位置
确保以下文件存在:
- `AI ASD Detector/Code/autism_model.pkl`
- `AI ASD Detector/Code/scaler.pkl`
- `AI ASD Detector/Code/label_encoders.pkl`
- `autism-spectrum-disorder-detection-main/models/autism_behavior_mobilenet_v2.keras`
- `autism-spectrum-disorder-detection-main/config/class_names.json`

## 注意事项
- 适配器加载器(`backend/adapters.py`)会在仓库根目录查找模型文件。如果移动或重命名,请更新 `adapters.py` 中的路径配置。
- 服务默认使用 CPU 模式运行(通过 CUDA_VISIBLE_DEVICES="" 设置),避免 GPU 驱动兼容性问题。
- 图像模型会自动检测输入尺寸要求,目前为 128x128 像素。

