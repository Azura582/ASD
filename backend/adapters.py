"""
adapters.py

Purpose: Load and expose unified prediction functions for ASD detection models:
  - load_adapters()
  - predict_image(bytes) -> dict
  - predict_survey(dict) -> dict
  - get_models_info() -> dict

Models loaded:
  - Survey model: 3 pkl files (model, scaler, label_encoders) from AI ASD Detector
  - Image model: 1 keras model file from autism-spectrum-disorder-detection-main
"""
from pathlib import Path
import json
import traceback
from typing import Optional
import os
import warnings

# Suppress sklearn version warnings
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

# Try multiple keras loaders (TF bundled or standalone)
load_model = None
from keras.models import load_model as _keras_load_model
load_model = _keras_load_model

import joblib
import numpy as np


ROOT = Path(__file__).resolve().parent  # backend directory
SURVEY_MODEL_PKL = ROOT / "models" / "autism_model.pkl"
SURVEY_SCALER_PKL = ROOT / "models" / "scaler.pkl"
SURVEY_ENCODERS_PKL = ROOT / "models" / "label_encoders.pkl"
IMAGE_MODEL_PATH = ROOT / "models" / "autism_behavior_mobilenet_v2.keras"
CLASS_NAMES_PATH = ROOT / "config" / "class_names.json"

# Global model storage
_survey_artifacts = None
_image_model = None
_class_names = []


def load_adapters():
    """Load all models and artifacts at startup"""
    global _survey_artifacts, _image_model, _class_names
    
    # Load class names for image model
    try:
        if CLASS_NAMES_PATH.exists():
            _class_names = json.loads(CLASS_NAMES_PATH.read_text())
        else:
            _class_names = []
            print("[adapters] warn: class_names.json not found")
    except Exception as e:
        _class_names = []
        print("[adapters] warn: failed to load class_names:", e)

    # Load survey artifacts (3 pkl files)
    try:
        if SURVEY_MODEL_PKL.exists():
            model = joblib.load(str(SURVEY_MODEL_PKL))
            scaler = joblib.load(str(SURVEY_SCALER_PKL)) if SURVEY_SCALER_PKL.exists() else None
            label_encoders = joblib.load(str(SURVEY_ENCODERS_PKL)) if SURVEY_ENCODERS_PKL.exists() else {}
            
            # Expected features from AI ASD Detector/Code/app.py
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
            print("[adapters] ✓ survey model loaded (3 pkl files)")
        else:
            _survey_artifacts = None
            print("[adapters] warn: survey model pkl not found at", SURVEY_MODEL_PKL)
    except Exception as e:
        _survey_artifacts = None
        print("[adapters] ERROR loading survey model:", e)
        traceback.print_exc()

    # Load keras image model
    try:
        if load_model is None:
            raise ImportError("keras load_model not available (install keras or tensorflow)")
        
        if IMAGE_MODEL_PATH.exists():
            _image_model = load_model(str(IMAGE_MODEL_PATH), compile=False)
            print("[adapters] ✓ image model loaded")
        else:
            _image_model = None
            print("[adapters] warn: image model not found at", IMAGE_MODEL_PATH)
    except Exception as e:
        _image_model = None
        print("[adapters] ERROR loading image model:", e)
        traceback.print_exc()

    print(f"[adapters] load complete - survey: {bool(_survey_artifacts)}, image: {bool(_image_model)}, classes: {len(_class_names)}")


def get_models_info():
    """Return status of loaded models"""
    return {
        "survey_model_loaded": bool(_survey_artifacts),
        "image_model_loaded": bool(_image_model),
        "class_names": _class_names,
        "class_names_count": len(_class_names),
    }


def predict_image(image_bytes: bytes) -> Optional[dict]:
    """
    Predict autism behavior from image bytes.
    Returns: {"label": str, "score": float, "raw": list}
    """
    if _image_model is None:
        return {"error": "image model not loaded"}
    
    try:
        from PIL import Image
        from io import BytesIO
        
        # Get model input shape
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

        # Preprocess image
        img = Image.open(BytesIO(image_bytes)).convert("RGB").resize((target_w, target_h))
        x = np.array(img).astype("float32") / 255.0
        x = np.expand_dims(x, axis=0)

        # Predict
        preds = _image_model.predict(x)
        
        # Extract prediction
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
            "raw": preds.tolist()
        }
    except Exception as e:
        return {
            "error": "image prediction failed",
            "detail": str(e),
            "trace": traceback.format_exc()
        }


def predict_survey(payload: dict) -> Optional[dict]:
    """
    Predict autism risk from survey responses.
    
    Expected payload format:
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
    
    Returns: {
      "prediction": str,
      "risk_questions": list,
      "score": int,
      "risk_level": str
    }
    """
    if _survey_artifacts is None:
        return {"error": "survey model not loaded"}
    
    try:
        model = _survey_artifacts["model"]
        scaler = _survey_artifacts["scaler"]
        label_encoders = _survey_artifacts["label_encoders"]
        expected_features = _survey_artifacts["expected_features"]
        
        # Extract data (support both {"data": {...}} and direct dict)
        data = payload.get("data", payload)
        
        # Transform input following AI ASD Detector logic
        transformed = {
            "Age_Mons": int(data.get("age", 0)),
            "Sex": data.get("sex", ""),
            "Ethnicity": data.get("ethnicity", ""),
            "Jaundice": data.get("jaundice", ""),
            "Family_mem_with_ASD": data.get("asd_history", ""),
            "Who completed the test": data.get("respondent", "")
        }
        
        # Questions where "No" is concerning (value 1), "Yes" is not concerning (value 0)
        for i in [1, 2, 3, 4, 5, 6, 7, 9]:
            q_key = f"Q{i}"
            a_key = f"A{i}"
            answer = data.get(q_key, {}).get("answer", "No") if isinstance(data.get(q_key), dict) else "No"
            transformed[a_key] = 0 if answer == "Yes" else 1
        
        # Questions where "Yes" is concerning (value 1), "No" is not concerning (value 0)
        for i in [8, 10]:
            q_key = f"Q{i}"
            a_key = f"A{i}"
            answer = data.get(q_key, {}).get("answer", "No") if isinstance(data.get(q_key), dict) else "No"
            transformed[a_key] = 1 if answer == "Yes" else 0
        
        # Encode categorical features
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
        
        # Build feature vector
        input_data = np.array([transformed.get(col, 0) for col in expected_features]).reshape(1, -1)
        
        # Scale
        if scaler is not None:
            input_data = scaler.transform(input_data)
        
        # Predict
        prediction = model.predict(input_data)
        
        # Calculate risk score
        score = sum(transformed.get(f'A{i}', 0) for i in range(1, 11))
        risk_threshold = 3
        if score <= risk_threshold:
            risk_level = "Low"
        elif score <= 7:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        risk_questions = [f'A{i}' for i in range(1, 11) if transformed.get(f'A{i}', 0) == 1]
        
        # Decode prediction label
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
            "error": "survey prediction failed",
            "detail": str(e),
            "trace": traceback.format_exc()
        }
