"""
api.py - FastAPI后端接口

提供统一的REST API用于ASD检测:
  - /predict/survey - 问卷预测
  - /predict/image - 图片预测
  - /health, /models - 健康检查和模型状态
"""
from fastapi import FastAPI, UploadFile, File, Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from . import adapters

app = FastAPI(
    title="ASD统一检测API",
    description="整合问卷和图片的自闭症谱系障碍检测接口",
    version="1.0.0"
)

# 启用CORS(允许前端跨域访问)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """启动时加载模型"""
    adapters.load_adapters()


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok"}


@app.get("/models")
async def models_list():
    """查看已加载的模型状态"""
    return adapters.get_models_info()


@app.post("/predict/survey")
async def predict_survey(payload: dict = Body(..., example={
    "age": 36,
    "sex": "Male",
    "ethnicity": "Others",
    "jaundice": "no",
    "asd_history": "no",
    "respondent": "Parent",
    "Q1": {"answer": "Yes"},
    "Q2": {"answer": "No"},
    "Q3": {"answer": "No"},
    "Q4": {"answer": "Yes"},
    "Q5": {"answer": "No"},
    "Q6": {"answer": "No"},
    "Q7": {"answer": "Yes"},
    "Q8": {"answer": "No"},
    "Q9": {"answer": "No"},
    "Q10": {"answer": "Yes"}
})):
    """
    问卷预测接口
    
    接受问卷数据,返回ASD风险评估
    """
    try:
        res = adapters.predict_survey(payload)
        if res is None or "error" in res:
            raise HTTPException(status_code=500, detail=res)
        return JSONResponse(res)
    except Exception as e:
        return JSONResponse({"error": "预测失败", "detail": str(e)}, status_code=500)


@app.post("/predict/image")
async def predict_image(file: UploadFile = File(...)):
    """
    图片预测接口
    
    上传图片,返回自闭症行为分类(head_banging/spinning/hand_flapping)
    """
    try:
        content = await file.read()
        res = adapters.predict_image(content)
        if res is None or "error" in res:
            raise HTTPException(status_code=500, detail=res)
        return JSONResponse(res)
    except Exception as e:
        return JSONResponse({"error": "预测失败", "detail": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run("backend.api:app", host="0.0.0.0", port=8000, reload=True)
