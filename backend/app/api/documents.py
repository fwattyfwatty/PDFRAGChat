from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from app.core.pdf_processor import process_pdf
from app.core.vector_store import create_vector_store

router = APIRouter()

@router.post("/upload")
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    PDFファイルをアップロードし、バックグラウンドで処理を開始する。
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")

    # 一時ファイルとして保存
    file_path = f"data/pdfs/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 重い処理をバックグラウンドで実行
    background_tasks.add_task(process_and_store_pdf, file_path, file.filename)

    return {"filename": file.filename, "message": "File uploaded and processing started."}

def process_and_store_pdf(file_path: str, filename: str):
    """
    PDFを処理し、ベクトルストアを作成する一連のタスク。
    """
    print(f"Processing {filename}...")
    # 1. PDFからテキストを抽出し、チャンクに分割
    chunks = process_pdf(file_path)
    # 2. チャンクをベクトル化し、FAISSストアを作成・保存
    create_vector_store(chunks, filename)
    print(f"Finished processing {filename}.")