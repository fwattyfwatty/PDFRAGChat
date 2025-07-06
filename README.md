# PDFRAGチャットボットWebアプリケーション

このプロジェクトは、PDFの内容をベースにしたRAG（Retrieval-Augmented Generation）チャットボットを作成するWebアプリケーションです。ユーザーがPDFドキュメントをアップロードすると、その内容に基づいてチャットボットがリアルタイムで回答を生成します。

## 目次

1. [プロジェクト概要](#プロジェクト概要)
2. [システム要件とセットアップ](#システム要件とセットアップ)
3. [使い方](#使い方)
4. [設定ファイル詳細](#設定ファイル詳細)

## プロジェクト概要

このアプリケーションは、機密性の高い文書や査読前の学術論文など、外部のAPIに送信したくない情報の対話的な読解・分析を支援します。ローカル環境で動作する大規模言語モデル（LLM）を用いて、安全かつ対話的に文書の内容を理解・活用することができます。

**Coreコンセプト:**
- **セキュアな環境**：ユーザーのプライバシーを守るために、PDFのテキストデータおよびチャットログはすべてローカル環境に保存されます。
- **高精度の回答生成**：RAGアーキテクチャを採用し、アップロードされたPDFの内容に関連した正確な回答を生成します。
- **柔軟なカスタマイズ**：ユーザーが利用するLLMモデルやベクトル化方法を自由に選択できます。

**プロジェクトのディレクトリ構成:**
```
PDFRAGChat/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── chat.py
│   │   │   ├── documents.py
│   │   │   ├── sessions.py
│   │   │   └── settings.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── pdf_processor.py
│   │   │   ├── rag_pipeline.py
│   │   │   └── vector_store.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py
│   │   ├── __init__.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── data/
│   │   ├── pdfs/
│   │   ├── vector_stores/
│   │   └── sessions/
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── PdfViewer.jsx
│   │   │   └── SettingsForm.jsx
│   │   ├── hooks/
│   │   │   └── useChat.js
│   │   ├── pages/
│   │   │   ├── MainPage.jsx
│   │   │   └── SettingsPage.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
├── LICENSE
└── README.md
```

### 環境要件:
- Python 3.8+
- Node.js 14+
- FastAPI
- React (Vite)
- Redis (オプション: 高度なコンテキスト管理の場合)

### テクノロジースタック:
- **バックエンド**: FastAPI, SQLAlchemy, Redis, FAISS (ベクトルストア)
- **フロントエンド**: React (Vite), Websockets
- **Ollama LLMサーバー**: Ollama API と互換性のあるモデル

## システム要件とセットアップ

本プロジェクトを動作させるためには、以下の前提条件を満たす必要があります:

**Ollamaサーバーのセットアップ:**
1. [Ollamaの公式ドキュメント](https://ollama.ai/docs/installation)に従って、Ollamaサーバーをインストールしてください。
2. `backend/.env` ファイルで `OLLAMA_API_ENDPOINT` 変数を`http://127.0.0.1:11434` に設定してください。(またはカスタムのOllamaサーバーエンドポイントに合わせて変更してください)
    ```env
    OLLAMA_API_ENDPOINT=http://127.0.0.1:11434
    ```

**Python環境のセットアップ:**
- Python 3.8+とpipがインストールされていることを確認してください。
- `backend/requirements.txt` にリストされた依存ライブラリをインストール:
    ```cmd
    cd backend
    pip install -r requirements.txt
    ```

**Node.js環境のセットアップ:**
- Node.js 14+とnpmがインストールされていることを確認してください。
- 次のコマンドでReact UIの依存ライブラリをインストールしてください:
    ```cmd
    cd frontend
    npm install
    ```

**FAISSライブラリの注意:**
- FAISSを利用するには、適切なホイールパッケージ（`faiss-cpu` または `faiss-gpu`）をインストールしておく必要がります。詳細は [FAISSのインストールガイド](https://github.com/facebookresearch/faiss/blob/main/INSTALL.md) を参照してください。

## 使い方

### バックエンドの起動:
`backend` ディレクトリ内で次のコマンドを実行してください:
```cmd
uvicorn app.main:app --reload --port 8000
```

### フロントエンドの起動:
`frontend` ディレクトリ内で次のコマンドを実行してください:
```cmd
npm run dev
```

### ブラウザで確認:
ブラウザで `http://localhost:5173` を開いてください。

**初回のセットアップ:**
1. **Ollamaのテスト:** フロントエンドの「設定」タブに移動し、「API Endpoint URL」を事前に設定したOllamaサーバーのエンドポイントに変更し、「Test Connection」ボタンを押します。
2. **PDFドキュメントのアップロード:** 「メイン」タブで左サイドのドラッグ＆ドロップエリアにPDFドキュメントをドロップします。
3. **チャットボットの利用:** 右サイドのチャットエリアでユーザーの質問を入力し、ボットからのリアルタイム回答を受け取ることができます。

### 開発環境向けコマンド:

**ブラックフォーマッター:** コードのフォーマットを整えるには:
```cmd
black backend/app/
black frontend/src/
```

**Pylint:** コードの静的解析:
```cmd
pylint backend/app/
```

**ESLint**:
```cmd
npx eslint frontend/src/
```

**TypeScriptチェック:**
```cmd
npx tsc --noEmit
```

---

### Tips for Development:

**開発時のデータ保持:**
- テストで使用したデータは自動で `backend/data` ディレクトリに保存されますが、プロジェクトのリビジョン管理には含まれません。不要な場合は適宜削除してください。

**チャットデータの永続化:**
- 各セッションは独立したJSONファイルで保存され、再起動後も会話履歴が保持されます。セッション管理やデータエクスポートは「メイン」タブ上部ボタンから行えます。

## 設定ファイル詳細

### フロントエンド設定:

フロントエンドは `frontend/src/components/SettingsForm.jsx` で定義されています。設定ファイルではOllamaサーバーやRAGパラメータ関連の設定項目が定義できます。

**Ollama設定:**
- `OLLAMA_API_ENDPOINT`: OllamaサーバーのエンドポイントURL。デフォルトは `http://127.0.0.1:11434` です。必要であれば、環境ファイル `backend/.env` かフロントエンドの「設定」タブ内URLテキストボックスから変更してください。

**RAG設定:**
- `chunk_size`: PDFファイルのテキストチャンクを分割する際の最大チャンクサイズ。デフォルト値は1000です。
- `chunk_overlap`: チャンク間で重複するテキストの文字数。デフォルト値は50です。
- `top_k`: PDFの中から検索するチャンクの数。デフォルト値は10です。

### 環境変数

主な設定値は `backend/.env`ファイルで管理されます:

```env
PORT=8000
OLLAMA_API_ENDPOINT=http://127.0.0.1:11434
```

開発設定:
- **WebSocketポート**: WebSocketサーバーのポート。デフォルトは8000に設定されています。
