import asyncio
from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
import uvicorn
import json
from read_json import read_json
import numpy as np

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)


# 判断连接是否成功路由
@app.get('/')
@app.post('/')
@app.put('/')
@app.delete('/')
async def read_root():
    return {"Connect Succeed"}


# 前端发请求和json运行用户自设路径
@app.post("/post_json")
async def put_path(model_request: Request):
    model_json = await model_request.json()
    value = read_json(model_json)
    return value


# 主监听函数
if __name__ == "__main__":
    uvicorn.run(app="web:app", host="192.168.0.240", port=8080, reload=False)  # 华为云
    # uvicorn.run(app="web:app", host="127.0.0.1", port=8080, reload=False)
