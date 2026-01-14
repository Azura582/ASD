"""
adapters.py

Purpose: dynamically load existing model scripts and expose unified prediction functions:
  - load_adapters()
  - predict_video(bytes) -> dict
  - predict_image(bytes) -> dict
  - predict_survey(dict) -> dict
  - get_models_info() -> dict

This file is defensive: if an upstream module or model is missing it will return helpful errors
instead of crashing the whole service.
"""
from pathlib import Path
import importlib.util
import json
import tempfile
import traceback
from typing import Optional
from keras.models import load_model
import os
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
# config: adjust these paths if your workspace layout differs
ROOT = Path(__file__).resolve().parents[1]
ASD_APP_PY = ROOT / "ASD---DESECTION-SYSTEM-main" / "app.py"
SURVEY_APP_PY = ROOT / "AI ASD Detector" / "Code" / "app.py"
IMAGE_MODEL_PATH = ROOT / "autism-spectrum-disorder-detection-main" / "models" / "autism_behavior_mobilenet_v2.keras"
CLASS_NAMES_PATH = ROOT / "autism-spectrum-disorder-detection-main" / "config" / "class_names.json"

_asd_module = None
_survey_module = None
_image_model = None
_class_names = []


def _load_module_from_path(name: str, path: Path):
    if not path.exists():
        raise FileNotFoundError(f"module path not found: {path}")
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_adapters():
    global _asd_module, _survey_module, _image_model, _class_names
    # load class names
    try:
        if CLASS_NAMES_PATH.exists():
            _class_names = json.loads(CLASS_NAMES_PATH.read_text())
        else:
            _class_names = []
    except Exception:
        _class_names = []

    # try load ASD video app (python script)
    try:
        _asd_module = _load_module_from_path("asd_app", ASD_APP_PY)
    except Exception as e:
        _asd_module = None
        print("warn: failed to load ASD video module:", e)

    # try load survey/text app
    try:
        _survey_module = _load_module_from_path("survey_app", SURVEY_APP_PY)
    except Exception as e:
        _survey_module = None
        print("warn: failed to load survey module:", e)

    # try load keras image model
    try:
        # import lazily so dependency optional until needed
       

        if IMAGE_MODEL_PATH.exists():
            _image_model = load_model(str(IMAGE_MODEL_PATH))
        else:
            _image_model = None
    except Exception as e:
        _image_model = None
        print("warn: failed to load image model:", e)

    print("adapters: loaded. class_names:", _class_names)


def get_models_info():
    return {
        "video_adapter": bool(_asd_module),
        "survey_adapter": bool(_survey_module),
        "image_model_loaded": bool(_image_model),
        "class_names_count": len(_class_names),
    }


def predict_video(video_bytes: bytes) -> Optional[dict]:
    """Save bytes to temp file and call existing predict function from loaded module.
    Returns dict or error dict.
    """
    if _asd_module is None:
        return {"error": "video adapter not available"}

    try:
        # try common function names
        func = None
        for name in ("predict_video", "predict_from_file", "infer_video"):
            if hasattr(_asd_module, name):
                func = getattr(_asd_module, name)
                break

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp.write(video_bytes)
            tmp.flush()
            tmp_path = tmp.name

        if func is not None:
            out = func(tmp_path)
            # normalize common string responses to a dict
            if isinstance(out, str):
                return {"label": out}
            if isinstance(out, dict):
                return out
            return {"result": out}
        # fallback: if module exposes a Flask app handler or CLI, try common entrypoints
        if hasattr(_asd_module, "main"):
            try:
                out = _asd_module.main(tmp_path)
                if isinstance(out, str):
                    return {"label": out}
                return out
            except Exception:
                pass

        return {"error": "no suitable predict function in asd module"}
    except Exception as e:
        return {"error": "exception in predict_video", "detail": str(e), "trace": traceback.format_exc()}


def predict_image(image_bytes: bytes) -> Optional[dict]:
    if _image_model is None:
        return {"error": "image model not loaded"}
    try:
        from PIL import Image
        import numpy as np
        from io import BytesIO
        # determine target size from model input shape (fallback to 128x128)
        try:
            inp_shape = None
            if hasattr(_image_model, 'input_shape') and _image_model.input_shape is not None:
                inp_shape = _image_model.input_shape
            elif hasattr(_image_model, 'inputs') and _image_model.inputs:
                # keras tensor shape -> list
                try:
                    inp_shape = tuple(_image_model.inputs[0].shape.as_list())
                except Exception:
                    inp_shape = None
            if inp_shape and len(inp_shape) >= 4:
                # assume channels_last: (None, H, W, C)
                target_h = int(inp_shape[1]) if inp_shape[1] is not None else None
                target_w = int(inp_shape[2]) if inp_shape[2] is not None else None
            else:
                target_h = target_w = None
        except Exception:
            target_h = target_w = None

        if not target_h or not target_w:
            target_h = target_w = 128

        img = Image.open(BytesIO(image_bytes)).convert("RGB").resize((target_w, target_h))
        x = np.array(img).astype("float32") / 255.0
        x = np.expand_dims(x, axis=0)

        preds = _image_model.predict(x)
        # normalize prediction handling for logits/probs/labels
        try:
            if hasattr(preds, 'shape') and len(preds.shape) == 2:
                probs = preds[0]
                idx = int(np.argmax(probs))
                score = float(probs[idx])
            else:
                # e.g., single-dim or other shapes
                probs = np.array(preds).ravel()
                idx = int(np.argmax(probs))
                score = float(probs[idx])
        except Exception:
            # fallback
            idx = 0
            score = 0.0

        label = _class_names[idx] if idx < len(_class_names) else str(idx)
        return {"label": label, "score": score, "raw": preds.tolist()}
    except Exception as e:
        return {"error": "image prediction failed", "detail": str(e), "trace": traceback.format_exc()}


def predict_survey(payload: dict) -> Optional[dict]:
    if _survey_module is None:
        return {"error": "survey adapter not available"}
    try:
        # try specific function names (we know this repo exposes `predict_autism`)
        if hasattr(_survey_module, "predict_autism"):
            fn = getattr(_survey_module, "predict_autism")
            # the function expects a dict of inputs (as implemented in the repo)
            out = fn(payload)
            # ensure output is serializable/dict
            if isinstance(out, dict):
                return out
            return {"prediction": out}

        # fallback to generic names
        for name in ("predict_survey", "predict"):
            if hasattr(_survey_module, name):
                fn = getattr(_survey_module, name)
                try:
                    out = fn(payload)
                except TypeError:
                    out = fn(**payload)
                if isinstance(out, dict):
                    return out
                return {"prediction": out}

        return {"error": "no suitable predict function in survey module"}
    except Exception as e:
        return {"error": "exception in predict_survey", "detail": str(e), "trace": traceback.format_exc()}
