import asyncio
from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
import uvicorn
import json
from read_json import read_json
import numpy as np
import psutil

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


@app.get("/get_cpu_usage")
async def get_cpu_usage():
    # 获取CPU的总使用率
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"CPU使用率: {cpu_usage}%")
    # 计算总使用率
    cpu_cores_usage = psutil.cpu_percent(percpu=True, interval=1)
    total_cpu_usage = sum(cpu_cores_usage)
    print(f"全部CPU核心总使用率: {total_cpu_usage}% (可超过100%)")
    return cpu_usage


# 主监听函数
if __name__ == "__main__":
    uvicorn.run(app="web:app", host="10.21.56.118", port=11451, reload=False)  # QG118
    # uvicorn.run(app="web:app", host="10.21.56.119", port=11451, reload=False)  # QG119
    # uvicorn.run(app="web:app", host="127.0.0.1", port=8080, reload=False)
