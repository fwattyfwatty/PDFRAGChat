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