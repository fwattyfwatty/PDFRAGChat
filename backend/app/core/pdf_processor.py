from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema.document import Document

def process_pdf(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    PDFファイルをロードし、テキストをチャンクに分割する。

    Args:
        file_path (str): PDFファイルのパス。
        chunk_size (int): 各チャンクの最大サイズ。
        chunk_overlap (int): チャンク間のオーバーラップ文字数。

    Returns:
        List[Document]: チャンク化されたドキュメントのリスト。
    """
    # 1. PDFをロード
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # 2. テキストをチャンクに分割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    
    print(f"PDF processed into {len(chunks)} chunks.")
    return chunks