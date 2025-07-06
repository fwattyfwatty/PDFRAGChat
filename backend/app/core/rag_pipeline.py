import numpy as np
from sentence_transformers import SentenceTransformer
from app.core.vector_store import get_vector_store
from app.core.config import get_settings

# RAGの処理を行うクラス
class RagPipeline:
    def __init__(self, filename):
        self.embedding_model = SentenceTransformer(get_settings().embedding_model)
        self.vector_store = get_vector_store(filename)
        self.top_k = get_settings().rag.top_k

    def get_relevant_chunks(self, query: str) -> list[str]:
        query_embedding = self.embedding_model.encode(query)
        distances, indices = self.vector_store.search(query_embedding, self.top_k)
        relevant_chunks = []
        for idx in indices:
            chunk = self.vector_store.get_chunk(idx)
            relevant_chunks.append(chunk)
        return relevant_chunks

    def generate_rag_prompt(self, query: str, chunks: list[str]) -> str:
        prompt = f"Question: {query}\n"
        prompt += "Relevant Information:\n"
        for chunk in chunks:
            prompt += f"- {chunk}\n"
        return prompt

    # クエリに対する応答を生成
    def generate_answer(self, query: str) -> str:
        relevant_chunks = self.get_relevant_chunks(query)
        rag_prompt = self.generate_rag_prompt(query, relevant_chunks)
        # NOTE: ここでLLMを呼び出す処理を実装する必要があります
        # 例：response = make_llm_call(rag_prompt)
        # response = make_llm_call(rag_prompt)
        response = "This is a sample response from the LLM."
        return response
    
    # ストリームで応答を生成
    def generate_answer_stream(self, query: str):
        # NOTE: ストリーミング適用時は、生成された各トークンをyieldでストリームとして返します
        yield from ["Th", "is", " is", " a s", "ampl", "e s", "tre", "am", "ed ", "res", "pon", "se ", "fro", "m t", "he ", "LL", "M."]

import ollama
from app.core.vector_store import load_vector_store

class RagPipeline:
    def __init__(self, vector_store_path: str):
        # 設定ファイルからモデル名を取得するのが望ましい
        self.llm_model = "llama3" 
        self.embedding_model = "mxbai-embed-large"
        self.vector_store = load_vector_store(vector_store_path, self.embedding_model)

    def retrieve(self, question: str, top_k: int = 5) -> list[str]:
        """ベクトルストアから関連性の高いチャンクを検索する"""
        results = self.vector_store.similarity_search(question, k=top_k)
        return [doc.page_content for doc in results]

    def generate_answer_stream(self, question: str):
        """検索したコンテキストを元にLLMで回答をストリーミング生成する"""
        retrieved_chunks = self.retrieve(question)
        context = "\n---\n".join(retrieved_chunks)

        prompt = f"""
        以下のコンテキスト情報のみを使用して、ユーザーの質問に日本語で回答してください。
        コンテキストに情報がない場合は、「分かりません」と回答してください。

        コンテキスト:
        {context}

        質問: {question}
        """
        
        # Ollama APIをストリーミングモードで呼び出す
        stream = ollama.chat(
            model=self.llm_model,
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
        )

        for chunk in stream:
            yield chunk['message']['content']