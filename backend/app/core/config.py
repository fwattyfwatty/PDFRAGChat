from pydantic_settings import BaseSettings
from typing import NamedTuple, Any

class OllamaSettings(NamedTuple):
    api_endpoint: str
    llm_model: str
    embedding_model: str

class RAGSettings(NamedTuple):
    chunk_size: int
    chunk_overlap: int
    top_k: int

class Settings(BaseSettings):
    ollama: OllamaSettings = OllamaSettings(
        api_endpoint="http://localhost",
        llm_model="mistral:7b-instruct-v2",
        embedding_model="BAAI/bge-small-en-v1.5",
    )
    rag: RAGSettings = RAGSettings(
        chunk_size=500,
        chunk_overlap=50,
        top_k=5,
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "PDFRAG_"

def get_settings() -> Settings:
    return Settings()