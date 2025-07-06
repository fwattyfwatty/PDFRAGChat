import os
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse

router = APIRouter()
SESSIONS_DIR = "data/sessions"

def get_session_path(session_id: str) -> str:
    """セッションIDからJSONファイルのパスを生成する"""
    if not os.path.exists(SESSIONS_DIR):
        os.makedirs(SESSIONS_DIR)
    return os.path.join(SESSIONS_DIR, f"{session_id}.json")

@router.get("/sessions")
def list_sessions():
    """保存されているすべてのセッションのリストを返す"""
    if not os.path.exists(SESSIONS_DIR):
        return []
    files = [f.replace('.json', '') for f in os.listdir(SESSIONS_DIR) if f.endswith('.json')]
    return files

@router.get("/sessions/{session_id}")
def get_session_history(session_id: str):
    """特定のセッションの会話履歴を取得する"""
    session_file = get_session_path(session_id)
    if not os.path.exists(session_file):
        raise HTTPException(status_code=404, detail="Session not found")
    return FileResponse(session_file)

@router.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    """特定のセッションを削除する"""
    session_file = get_session_path(session_id)
    if os.path.exists(session_file):
        os.remove(session_file)
        return {"message": "Session deleted successfully"}
    raise HTTPException(status_code=404, detail="Session not found")

@router.get("/export/{session_id}/{format}")
def export_session(session_id: str, format: str):
    """セッション履歴を指定のフォーマットでエクスポートする"""
    session_file = get_session_path(session_id)
    if not os.path.exists(session_file):
        raise HTTPException(status_code=404, detail="Session not found")

    with open(session_file, 'r', encoding='utf-8') as f:
        history = json.load(f)

    if format == "json":
        return JSONResponse(content=history, headers={"Content-Disposition": f"attachment; filename={session_id}.json"})
    
    if format == "md":
        md_content = f"# Chat History: {session_id}\n\n"
        for msg in history:
            if msg['role'] == 'user':
                md_content += f"**You:**\n{msg['content']}\n\n---\n\n"
            else:
                md_content += f"**Assistant:**\n{msg['content']}\n\n---\n\n"
        return FileResponse(md_content, media_type="text/markdown", headers={"Content-Disposition": f"attachment; filename={session_id}.md"})

    raise HTTPException(status_code=400, detail="Invalid format specified. Use 'json' or 'md'.")