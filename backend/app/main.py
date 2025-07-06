from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, documents, settings, sessions

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI(title="PDF RAG Chatbot API")

# CORS (Cross-Origin Resource Sharing) ミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境ではフロントエンドのURLに限定する
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 各機能のAPIルーターをインクルード
app.include_router(documents.router, prefix="/api", tags=["Documents"])
app.include_router(settings.router, prefix="/api", tags=["Settings"])
app.include_router(sessions.router, prefix="/api", tags=["Sessions"])
# WebSocketは直接appインスタンスに追加
app.add_api_websocket_route("/ws/chat/{session_id}", chat.websocket_endpoint)

@app.get("/")
def read_root():
    return {"message": "Welcome to PDF RAG Chatbot API"}