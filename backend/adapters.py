"""
adapters.py - 模型加载和预测适配器

纯 PyTorch/Ultralytics YOLO 实现，不依赖 Keras/TensorFlow
"""
from pathlib import Path
import json
import traceback
from typing import Optional
import os
import warnings

warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')
warnings.filterwarnings('ignore', category=FutureWarning)

# 强制使用 CPU
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

# PyTorch 和 Ultralytics
try:
    import torch
    from ultralytics import YOLO
    TORCH_AVAILABLE = True
except ImportError as e:
    torch = None
    YOLO = None
    TORCH_AVAILABLE = False
    print(f"[adapters] 警告: PyTorch/Ultralytics 不可用: {e}")

import joblib
import numpy as np
from PIL import Image
from io import BytesIO

BACKEND_DIR = Path(__file__).resolve().parent
MODELS_DIR = BACKEND_DIR / "models"
CONFIG_DIR = BACKEND_DIR / "config"

# 模型文件路径
SURVEY_MODEL_PKL = MODELS_DIR / "autism_model.pkl"
SURVEY_SCALER_PKL = MODELS_DIR / "scaler.pkl"
SURVEY_ENCODERS_PKL = MODELS_DIR / "label_encoders.pkl"
IMAGE_MODEL_PATH = MODELS_DIR / "best.pt"
CLASS_NAMES_PATH = CONFIG_DIR / "class_names.json"

# 全局模型存储
_survey_artifacts = None
_image_model = None
_class_names = []


def load_adapters():
    """加载所有模型适配器"""
    global _survey_artifacts, _image_model, _class_names
    
    # 加载图片分类标签
    try:
        if CLASS_NAMES_PATH.exists():
            _class_names = json.loads(CLASS_NAMES_PATH.read_text())
        else:
            _class_names = []
            print(f"[adapters] 警告: class_names.json未找到于 {CLASS_NAMES_PATH}")
    except Exception as e:
        _class_names = []
        print(f"[adapters] 警告: 加载class_names失败: {e}")

    # 加载问卷模型artifacts
    try:
        if not all([SURVEY_MODEL_PKL.exists(), SURVEY_SCALER_PKL.exists(), SURVEY_ENCODERS_PKL.exists()]):
            _survey_artifacts = None
            print(f"[adapters] 警告: 问卷模型文件不完整")
        else:
            _survey_artifacts = {
                "model": joblib.load(str(SURVEY_MODEL_PKL)),
                "scaler": joblib.load(str(SURVEY_SCALER_PKL)),
                "label_encoders": joblib.load(str(SURVEY_ENCODERS_PKL))
            }
            print(f"[adapters] ✓ 问卷模型已加载 (3个pkl文件)")
    except Exception as e:
        _survey_artifacts = None
        print(f"[adapters] 错误: 加载问卷模型失败: {e}")
        traceback.print_exc()

    # 加载 YOLO 图片模型 (PyTorch)
    try:
        if not TORCH_AVAILABLE:
            _image_model = None
            print(f"[adapters] 错误: PyTorch 或 Ultralytics 未安装，请运行: pip install torch ultralytics")
        elif not IMAGE_MODEL_PATH.exists():
            _image_model = None
            print(f"[adapters] 警告: 图片模型未找到于 {IMAGE_MODEL_PATH}")
        else:
            # 使用 Ultralytics YOLO 加载模型
            _image_model = YOLO(str(IMAGE_MODEL_PATH))
            # 设置为 CPU 模式
            _image_model.to('cpu')
            print(f"[adapters] ✓ 图片模型已用 Ultralytics YOLO 加载 ({IMAGE_MODEL_PATH.name})")
    except Exception as e:
        _image_model = None
        print(f"[adapters] 错误: 加载图片模型失败: {e}")
        traceback.print_exc()

    print(f"[adapters] 加载完成 - 问卷: {bool(_survey_artifacts)}, 图片: {bool(_image_model)}, 类别数: {len(_class_names)}")


def get_models_info():
    """返回模型加载状态信息"""
    return {
        "survey_model_loaded": bool(_survey_artifacts),
        "image_model_loaded": bool(_image_model),
        "class_names": _class_names,
        "class_names_count": len(_class_names)
    }


def predict_image(image_bytes: bytes) -> Optional[dict]:
    """使用 YOLO 模型对图片进行分类预测"""
    if _image_model is None:
        return {"error": "图片模型未加载"}
    
    try:
        # 从字节流加载图片
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        
        # YOLO 预测 (verbose=False 禁止打印)
        results = _image_model(img, verbose=False)
        
        # 获取第一个结果
        result = results[0]
        
        # 获取预测类别和概率
        if hasattr(result, 'probs') and result.probs is not None:
            # 分类任务
            probs = result.probs.data.cpu().numpy()
            top_idx = int(result.probs.top1)
            top_conf = float(result.probs.top1conf)
            
            # 获取标签
            label = _class_names[top_idx] if top_idx < len(_class_names) else str(top_idx)
            
            # 构建所有类别概率字典
            all_probs = {}
            for i, prob in enumerate(probs):
                class_name = _class_names[i] if i < len(_class_names) else f"class_{i}"
                all_probs[class_name] = float(prob)
            
            return {
                "label": label,
                "score": top_conf,
                "confidence": f"{top_conf*100:.2f}%",
                "all_probabilities": all_probs
            }
        else:
            # 如果不是分类模型，返回检测结果
            return {
                "error": "模型类型不匹配",
                "detail": "当前模型不是分类模型，请使用正确的 YOLO 分类模型"
            }
            
    except Exception as e:
        return {
            "error": "图片预测失败",
            "detail": str(e),
            "trace": traceback.format_exc()
        }


def predict_survey(payload: dict) -> Optional[dict]:
    """问卷预测 (保持原有逻辑不变)"""
    if _survey_artifacts is None:
        return {"error": "问卷模型未加载"}
    
    try:
        model = _survey_artifacts["model"]
        scaler = _survey_artifacts["scaler"]
        label_encoders = _survey_artifacts["label_encoders"]
        
        # 提取基本信息
        age = int(payload.get("age", 36))
        sex = str(payload.get("sex", "Male"))
        ethnicity = str(payload.get("ethnicity", "Others"))
        jaundice = str(payload.get("jaundice", "no"))
        asd_history = str(payload.get("asd_history", "no"))
        respondent = str(payload.get("respondent", "Parent"))
        
        # 提取10个问题答案
        answers = []
        for i in range(1, 11):
            q_key = f"Q{i}"
            if q_key in payload:
                ans = payload[q_key]
                if isinstance(ans, dict):
                    ans_val = ans.get("answer", "No")
                else:
                    ans_val = str(ans)
                answers.append(1 if ans_val.lower() in ["yes", "1", "true"] else 0)
            else:
                answers.append(0)
        
        score = sum(answers)
        
        # 编码分类特征
        sex_enc = label_encoders.get("sex", {}).get(sex, 0) if isinstance(label_encoders.get("sex"), dict) else 0
        ethnicity_enc = label_encoders.get("ethnicity", {}).get(ethnicity, 0) if isinstance(label_encoders.get("ethnicity"), dict) else 0
        jaundice_enc = 1 if jaundice.lower() == "yes" else 0
        asd_history_enc = 1 if asd_history.lower() == "yes" else 0
        respondent_enc = label_encoders.get("respondent", {}).get(respondent, 0) if isinstance(label_encoders.get("respondent"), dict) else 0
        
        # 构建特征向量
        features = [age, sex_enc, ethnicity_enc, jaundice_enc, asd_history_enc] + answers + [respondent_enc, score]
        features_array = np.array(features).reshape(1, -1)
        
        # 标准化
        features_scaled = scaler.transform(features_array)
        
        # 预测
        prediction = model.predict(features_scaled)[0]
        
        # 风险等级
        if score >= 7:
            risk_level = "高风险"
        elif score >= 4:
            risk_level = "中风险"
        else:
            risk_level = "低风险"
        
        # 风险问题
        risk_questions = [f"Q{i+1}" for i, ans in enumerate(answers) if ans == 1]
        
        return {
            "prediction": "ASD" if prediction == 1 else "非ASD",
            "score": score,
            "risk_level": risk_level,
            "risk_questions": risk_questions,
            "features": features
        }
    except Exception as e:
        return {
            "error": "问卷预测失败",
            "detail": str(e),
            "trace": traceback.format_exc()
        }
