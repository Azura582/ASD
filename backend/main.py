from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from . import adapters
import os

app = FastAPI(title="Unified ASD Detection API")


class SurveyPayload(BaseModel):
    data: dict


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


@app.post("/predict/video")
async def predict_video(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    # For large files you can return a job id and process in background
    content = await file.read()
    # immediate processing (synchronous) for simplicity
    res = adapters.predict_video(content)
    if res is None:
        raise HTTPException(status_code=500, detail="video prediction failed")
    return JSONResponse(res)


@app.post("/predict/survey")
async def predict_survey(payload: SurveyPayload):
    res = adapters.predict_survey(payload.data)
    if res is None:
        raise HTTPException(status_code=500, detail="survey prediction failed")
    return JSONResponse(res)


@app.get("/models")
async def models_list():
    return adapters.get_models_info()


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
