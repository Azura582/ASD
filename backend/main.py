
from fastapi import FastAPI, UploadFile, File, Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, Any
from . import adapters

app = FastAPI(
    title="ASD 检测统一 API",
    description="整合问卷评估和图片行为分类的自闭症谱系障碍检测系统",
    version="1.0.0"
)

# CORS 配置
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
    print("正在加载模型...")
    adapters.load_adapters()
    print("模型加载完成！")


@app.get("/")
async def root():
    
    return {
        "message": "ASD 检测 API",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "models": "/models",
            "survey": "/predict/survey",
            "image": "/predict/image"
        }
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/models")
async def models_info():
    
    return adapters.get_models_info()


@app.post("/predict/survey")
async def predict_survey(payload: Dict[Any, Any] = Body(..., example={
    "age": 36,
    "sex": "Male",
    "ethnicity": "Other",
    "jaundice": "no",
    "asd_history": "no",
    "respondent": "parent",
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
    
    try:
        result = adapters.predict_survey(payload)
        if result and "error" not in result:
            return JSONResponse(content=result)
        else:
            raise HTTPException(status_code=500, detail=result.get("detail", "预测失败"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/image")
async def predict_image(file: UploadFile = File(...)):
    
    try:
        # 读取文件内容
        contents = await file.read()
        
        # 调用预测函数
        result = adapters.predict_image(contents)
        
        if result and "error" not in result:
            return JSONResponse(content=result)
        else:
            raise HTTPException(status_code=500, detail=result.get("detail", "预测失败"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
