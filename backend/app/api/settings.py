from fastapi import APIRouter, HTTPException
from app.models.schemas import OllamaSettings, RagSettings
import json
import ollama

router = APIRouter()
SETTINGS_FILE = "data/settings.json"

def _load_settings():
    """設定ファイルを読み込むヘルパー関数"""
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # デフォルト設定を返す
        return {
            "ollama": {"llm_model": "llama3", "embedding_model": "mxbai-embed-large"},
            "rag": {"chunk_size": 1000, "chunk_overlap": 200, "top_k": 5}
        }

@router.get("/settings")
def get_settings():
    """現在の設定を取得する"""
    return _load_settings()

@router.post("/settings")
def update_settings(ollama_settings: OllamaSettings, rag_settings: RagSettings):
    """設定を更新してファイルに保存する"""
    all_settings = {
        "ollama": ollama_settings.model_dump(),
        "rag": rag_settings.model_dump()
    }
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(all_settings, f, indent=2)
    return {"message": "Settings updated successfully."}

@router.get("/ollama/models")
def get_ollama_models():
    """Ollamaで利用可能なモデルのリストを取得する"""
    try:
        response = ollama.list()
        return {"models": response['models']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not connect to Ollama: {e}")