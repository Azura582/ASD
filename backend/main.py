from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from . import adapters
import os

app = FastAPI(title="Unified ASD Detection API")


@app.on_event("startup")
async def startup_event():
    adapters.load_adapters()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/version")
async def version():
    return {"app": "Unified ASD API", "backend_path": os.path.abspath(os.path.dirname(__file__))}


@app.post("/predict/image")
async def predict_image(file: UploadFile = File(...)):
    content = await file.read()
    res = adapters.predict_image(content)
    if res is None:
        raise HTTPException(status_code=500, detail="image prediction failed")
    return JSONResponse(res)


@app.post("/predict/survey")
async def predict_survey(request: Request):
    # Debug: capture raw body to help diagnose malformed requests
    raw = await request.body()
    try:
        payload = await request.json()
    except Exception:
        # not valid JSON
        print("[debug] predict_survey received non-json body:", raw)
        raise HTTPException(status_code=422, detail={"error": "request body is not valid JSON", "raw": raw.decode('utf-8', errors='replace')})

    # Accept either {"data": {...}} or direct data dict
    if isinstance(payload, dict) and "data" in payload and isinstance(payload["data"], dict):
        data = payload["data"]
    else:
        data = payload

    res = adapters.predict_survey({"data": data})
    if res is None:
        raise HTTPException(status_code=500, detail="survey prediction failed")
    return JSONResponse(res)


@app.get("/models")
async def models_list():
    return adapters.get_models_info()


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
