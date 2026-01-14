"""
adapters.py - 模型加载和预测适配器

加载的模型:
  - 问卷模型: 3个pkl文件 (model, scaler, label_encoders)
  - 图片模型: 1个keras模型文件
"""
from pathlib import Path
import json
import traceback
from typing import Optional
import os
import warnings

# 抑制sklearn版本警告
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

# 强制使用CPU模式(避免GPU驱动问题)
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

# 尝试多种keras加载方式
load_model = None
try:
    from tensorflow.keras.models import load_model as _tf_load_model
    load_model = _tf_load_model
except Exception:
    try:
        from keras.models import load_model as _keras_load_model
        load_model = _keras_load_model
    except Exception:
        load_model = None

import joblib
import numpy as np

# 配置路径 - 使用 backend/models 目录
BACKEND_DIR = Path(__file__).resolve().parent
MODELS_DIR = BACKEND_DIR / "models"
CONFIG_DIR = BACKEND_DIR / "config"

# 模型文件路径
SURVEY_MODEL_PKL = MODELS_DIR / "autism_model.pkl"
SURVEY_SCALER_PKL = MODELS_DIR / "scaler.pkl"
SURVEY_ENCODERS_PKL = MODELS_DIR / "label_encoders.pkl"
IMAGE_MODEL_PATH = MODELS_DIR / "autism_behavior_mobilenet_v2.keras"
CLASS_NAMES_PATH = CONFIG_DIR / "class_names.json"

# 全局模型存储
_survey_artifacts = None
_image_model = None
_class_names = []


def load_adapters():
    """启动时加载所有模型和artifacts"""
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

    # 加载问卷模型artifacts (3个pkl文件)
    try:
        if SURVEY_MODEL_PKL.exists():
            model = joblib.load(str(SURVEY_MODEL_PKL))
            scaler = joblib.load(str(SURVEY_SCALER_PKL)) if SURVEY_SCALER_PKL.exists() else None
            label_encoders = joblib.load(str(SURVEY_ENCODERS_PKL)) if SURVEY_ENCODERS_PKL.exists() else {}
            
            # 期望的特征列表(来自AI ASD Detector/Code/app.py)
            expected_features = [
                'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
                'Age_Mons', 'Sex', 'Ethnicity', 'Jaundice', 'Family_mem_with_ASD', 'Who completed the test'
            ]
            
            _survey_artifacts = {
                "model": model,
                "scaler": scaler,
                "label_encoders": label_encoders,
                "expected_features": expected_features
            }
            print(f"[adapters] ✓ 问卷模型已加载 (3个pkl文件)")
        else:
            _survey_artifacts = None
            print(f"[adapters] 警告: 问卷模型pkl未找到于 {SURVEY_MODEL_PKL}")
    except Exception as e:
        _survey_artifacts = None
        print(f"[adapters] 错误: 加载问卷模型失败: {e}")
        traceback.print_exc()

    # 加载keras图片模型
    try:
        if load_model is None:
            raise ImportError("keras load_model不可用 (需安装keras或tensorflow)")
        
        if IMAGE_MODEL_PATH.exists():
            _image_model = load_model(str(IMAGE_MODEL_PATH), compile=False)
            print(f"[adapters] ✓ 图片模型已加载")
        else:
            _image_model = None
            print(f"[adapters] 警告: 图片模型未找到于 {IMAGE_MODEL_PATH}")
    except Exception as e:
        _image_model = None
        print(f"[adapters] 错误: 加载图片模型失败: {e}")
        traceback.print_exc()

    print(f"[adapters] 加载完成 - 问卷: {bool(_survey_artifacts)}, 图片: {bool(_image_model)}, 类别数: {len(_class_names)}")


def get_models_info():
    """返回已加载模型的状态"""
    return {
        "survey_model_loaded": bool(_survey_artifacts),
        "image_model_loaded": bool(_image_model),
        "class_names": _class_names,
        "class_names_count": len(_class_names),
    }


def predict_image(image_bytes: bytes) -> Optional[dict]:
    """
    从图片字节流预测自闭症行为
    返回: {"label": str, "score": float, "raw": list}
    """
    if _image_model is None:
        return {"error": "图片模型未加载"}
    
    try:
        from PIL import Image
        from io import BytesIO
        
        # 获取模型输入尺寸
        try:
            inp_shape = None
            if hasattr(_image_model, 'input_shape') and _image_model.input_shape is not None:
                inp_shape = _image_model.input_shape
            elif hasattr(_image_model, 'inputs') and _image_model.inputs:
                inp_shape = tuple(_image_model.inputs[0].shape.as_list())
            
            if inp_shape and len(inp_shape) >= 4:
                target_h = int(inp_shape[1]) if inp_shape[1] is not None else 128
                target_w = int(inp_shape[2]) if inp_shape[2] is not None else 128
            else:
                target_h = target_w = 128
        except Exception:
            target_h = target_w = 128

        # 预处理图片
        img = Image.open(BytesIO(image_bytes)).convert("RGB").resize((target_w, target_h))
        x = np.array(img).astype("float32") / 255.0
        x = np.expand_dims(x, axis=0)

        # 预测
        preds = _image_model.predict(x, verbose=0)
        
        # 提取预测结果
        if hasattr(preds, 'shape') and len(preds.shape) == 2:
            probs = preds[0]
        else:
            probs = np.array(preds).ravel()
        
        idx = int(np.argmax(probs))
        score = float(probs[idx])
        label = _class_names[idx] if idx < len(_class_names) else str(idx)
        
        return {
            "label": label,
            "score": score,
            "confidence": f"{score*100:.2f}%",
            "all_probabilities": {_class_names[i]: float(probs[i]) for i in range(len(_class_names))} if len(_class_names) == len(probs) else {}
        }
    except Exception as e:
        return {
            "error": "图片预测失败",
            "detail": str(e),
            "trace": traceback.format_exc()
        }


def predict_survey(payload: dict) -> Optional[dict]:
    """
    从问卷响应预测自闭症风险
    
    期望的payload格式:
    {
      "data": {
        "age": int,
        "sex": str,
        "ethnicity": str,
        "jaundice": str,
        "asd_history": str,
        "respondent": str,
        "Q1": {"answer": "Yes"|"No"},
        ...
        "Q10": {"answer": "Yes"|"No"}
      }
    }
    
    返回: {
      "prediction": str,
      "risk_questions": list,
      "score": int,
      "risk_level": str
    }
    """
    if _survey_artifacts is None:
        return {"error": "问卷模型未加载"}
    
    try:
        model = _survey_artifacts["model"]
        scaler = _survey_artifacts["scaler"]
        label_encoders = _survey_artifacts["label_encoders"]
        expected_features = _survey_artifacts["expected_features"]
        
        # 提取数据(支持{"data": {...}}或直接dict)
        data = payload.get("data", payload)
        
        # 转换输入(遵循AI ASD Detector逻辑)
        transformed = {
            "Age_Mons": int(data.get("age", 0)),
            "Sex": data.get("sex", ""),
            "Ethnicity": data.get("ethnicity", ""),
            "Jaundice": data.get("jaundice", ""),
            "Family_mem_with_ASD": data.get("asd_history", ""),
            "Who completed the test": data.get("respondent", "")
        }
        
        # Q1-Q7, Q9: "No"=风险(值1), "Yes"=正常(值0)
        for i in [1, 2, 3, 4, 5, 6, 7, 9]:
            q_key = f"Q{i}"
            a_key = f"A{i}"
            answer = data.get(q_key, {}).get("answer", "No") if isinstance(data.get(q_key), dict) else "No"
            transformed[a_key] = 0 if answer == "Yes" else 1
        
        # Q8, Q10: "Yes"=风险(值1), "No"=正常(值0)
        for i in [8, 10]:
            q_key = f"Q{i}"
            a_key = f"A{i}"
            answer = data.get(q_key, {}).get("answer", "No") if isinstance(data.get(q_key), dict) else "No"
            transformed[a_key] = 1 if answer == "Yes" else 0
        
        # 编码分类特征
        for col in ['Sex', 'Ethnicity', 'Jaundice', 'Family_mem_with_ASD', 'Who completed the test']:
            if col in transformed and col in label_encoders:
                try:
                    if transformed[col] in label_encoders[col].classes_:
                        transformed[col] = label_encoders[col].transform([transformed[col]])[0]
                    else:
                        transformed[col] = 0
                except Exception:
                    transformed[col] = 0
            else:
                transformed[col] = 0
        
        # 构建特征向量
        input_data = np.array([transformed.get(col, 0) for col in expected_features]).reshape(1, -1)
        
        # 缩放
        if scaler is not None:
            input_data = scaler.transform(input_data)
        
        # 预测
        prediction = model.predict(input_data)
        
        # 计算风险分数
        score = sum(transformed.get(f'A{i}', 0) for i in range(1, 11))
        risk_threshold = 3
        if score <= risk_threshold:
            risk_level = "低风险"
        elif score <= 7:
            risk_level = "中风险"
        else:
            risk_level = "高风险"
        
        risk_questions = [f'Q{i}' for i in range(1, 11) if transformed.get(f'A{i}', 0) == 1]
        
        # 解码预测标签
        pred_label_encoder = label_encoders.get('Class/ASD Traits ', None)
        if pred_label_encoder is not None:
            try:
                pred_str = pred_label_encoder.inverse_transform(prediction)[0]
            except Exception:
                pred_str = str(prediction[0])
        else:
            pred_str = str(prediction[0])
        
        return {
            "prediction": pred_str,
            "risk_questions": risk_questions,
            "score": int(score),
            "risk_level": risk_level
        }
    except Exception as e:
        return {
            "error": "问卷预测失败",
            "detail": str(e),
            "trace": traceback.format_exc()
        }
