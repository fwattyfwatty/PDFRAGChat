from pydantic import BaseModel
from typing import List, Optional

class OllamaSettings(BaseModel):
    llm_model: str = "llama3"
    embedding_model: str = "mxbai-embed-large"
    reranker_model: Optional[str] = None

class RagSettings(BaseModel):
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 5