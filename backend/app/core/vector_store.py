from faiss import IndexFlatL2, read_index, write_index
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import pickle
from typing import Dict, Any


class VectorStore:
    def __init__(self, index: IndexFlatL2, chunk_ids: Dict[int, Any]):
        self.index = index
        self._chunk_ids = chunk_ids

    def add_embeddings(self, embeddings):
        self.index.add(embeddings)

    def search(self, query_embedding, top_k):
        distances, indices = self.index.search(query_embedding.reshape(1, -1), top_k)
        return indices.flatten()

    def get_chunk(self, idx):
        return self._chunk_ids[idx]

loaded_stores: Dict[str, VectorStore] = {}

def load_vector_store(filename: str) -> VectorStore:
    if filename in loaded_stores:
        return loaded_stores[filename]
    
    # Initialize the SentenceTransformer and encode the chunks
    filename = "_".join(filename.split("."))  # Remove file extension
    path = f'data/vector_stores/{filename}'
    
    chunk_ids_path = path + "_ids"
    if not os.path.exists(path):
        index = IndexFlatL2(384)  # Example with 384-dimensional embeddings
        chunk_ids = {}
    else:
        with open(chunk_ids_path, 'rb') as f:
            chunk_ids = pickle.load(f)
        index = read_index(path)
        for store in loaded_stores.values():
            if store._chunk_ids == chunk_ids:
                index = store.index
                break
    
    store = VectorStore(index, chunk_ids)
    loaded_stores[filename] = store

def get_vector_store(filename: str) -> VectorStore:
    """ファイル名に基づいてベクトルストアを取得（または生成）します。"""
    return load_vector_store(filename)

    return store

def create_vector_store(chunks, filename: str):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode([chunk.page_content for chunk in chunks])
    
    # Convert chunks to a dictionary for easy access
    chunk_ids = {i: chunk for i, chunk in enumerate(chunks)}
    
    filename = "_".join(filename.split("."))  # Remove file extension
    path = f'data/vector_stores/{filename}'
    chunk_ids_path = path + "_ids"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Create the index to be used
    index = IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    
    # Save the vector store and chunk IDs
    write_index(index, path)
    with open(chunk_ids_path, 'wb') as f:
        pickle.dump(chunk_ids, f)
    
    store = VectorStore(index, chunk_ids)
    loaded_stores[filename] = store
    return store