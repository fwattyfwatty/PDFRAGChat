import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from typing import List
from langchain.schema.document import Document
import os

# 設定からモデル名を取得するのが望ましい
EMBEDDING_MODEL = "mxbai-embed-large" 
VECTOR_STORE_DIR = "data/vector_stores"

def get_embedding_function():
    """OllamaのEmbeddingモデル関数を取得する"""
    return OllamaEmbeddings(model=EMBEDDING_MODEL)

def create_vector_store(chunks: List[Document], filename: str):
    """
    ドキュメントチャンクからFAISSベクトルストアを作成し、ローカルに保存する。
    """
    if not os.path.exists(VECTOR_STORE_DIR):
        os.makedirs(VECTOR_STORE_DIR)
        
    embeddings = get_embedding_function()
    vector_store = FAISS.from_documents(chunks, embedding=embeddings)
    
    # ファイル名から拡張子を除いて保存パスを生成
    base_filename = os.path.splitext(filename)[0]
    save_path = os.path.join(VECTOR_STORE_DIR, base_filename)
    
    vector_store.save_local(save_path)
    print(f"Vector store saved to {save_path}")

def load_vector_store(filename: str) -> FAISS:
    """
    ローカルからFAISSベクトルストアをロードする。
    """
    embeddings = get_embedding_function()
    
    # ファイル名から拡張子を除いてパスを生成
    base_filename = os.path.splitext(filename)[0]
    load_path = os.path.join(VECTOR_STORE_DIR, base_filename)

    if not os.path.exists(load_path):
        raise FileNotFoundError(f"Vector store not found at {load_path}")
        
    vector_store = FAISS.load_local(load_path, embeddings, allow_dangerous_deserialization=True)
    print(f"Vector store loaded from {load_path}")
    return vector_store