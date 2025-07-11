from fastapi import WebSocket, WebSocketDisconnect
from app.core.rag_pipeline import RagPipeline
from app.api.sessions import get_session_path # 追加
import json
import os
import datetime

def save_message_to_history(session_id: str, role: str, content: str):
    """会話履歴をJSONファイルに追記保存する"""
    session_file = get_session_path(session_id)
    history = []
    if os.path.exists(session_file):
        with open(session_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
    
    history.append({
        "role": role,
        "content": content,
        "timestamp": datetime.datetime.now().isoformat()
    })

    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket接続を処理し、RAGパイプラインを通じてチャットを行う。
    (会話履歴の読み書き機能付き)
    """
    await websocket.accept()
    # RAGパイプラインを初期化
    rag_pipeline = RagPipeline(get_session_filename(session_id)) # 追加

    try:
        while True:
            question = await websocket.receive_text()
            save_message_to_history(session_id, "user", question)

            # RAGパイプラインを使って応答を生成
            tokens, full_response = retrieve_and_generate_answer(rag_pipeline, question) # 追加

            for token in tokens:
                await websocket.send_text(token)

            # 最終的な生成された応答を履歴に保存
            if full_response:
                save_message_to_history(session_id, "assistant", full_response)

            await websocket.send_text("[END_OF_STREAM]")

    except WebSocketDisconnect:
        print(f"Client disconnected from session {session_id}")
    except Exception as e:
        print(f"Error in chat session {session_id}: {e}")