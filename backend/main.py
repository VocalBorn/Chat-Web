# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio

# 建立 Socket.IO 非同步伺服器
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')

# 建立 FastAPI 應用
app = FastAPI()

# 加入 CORS 中介層（讓前端可以連線）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開發階段先允許全部來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 加入簡單的 HTTP 測試路由
@app.get("/")
async def index():
    return {"message": "FastAPI + Socket.IO is running!"}

# 綁定 Socket.IO 到 FastAPI 上
app_sio = socketio.ASGIApp(sio, app)

# 必須把 app 指到 app_sio，讓 uvicorn 可以找到正確的 ASGI 入口點
app = app_sio

# Socket.IO 事件處理
@sio.event
async def connect(sid, environ):
    print("✅ Client connected:", sid)

@sio.event
async def chat_message(sid, data):
    user = data.get("user", "Anonymous")
    message = data.get("message", "")
    print(f"Message from {user}: {message}")
    await sio.emit("chat_message", f"[{user}] {message}")
@sio.event
async def disconnect(sid):
    print("❌ Client disconnected:", sid)
