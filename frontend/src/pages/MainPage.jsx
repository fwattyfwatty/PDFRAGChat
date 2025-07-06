import React, { useState } from 'react';
import PdfViewer from '../components/PdfViewer';
import ChatWindow from '../components/ChatWindow';
import { uploadPdf } from '../services/api';

function MainPage() {
  const [currentPdf, setCurrentPdf] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileUpload = async (file) => {
    setIsUploading(true);
    try {
      const response = await uploadPdf(file);
      setCurrentPdf(URL.createObjectURL(file));
      setSessionId(response.filename); // バックエンドから返されたファイル名をセッションIDとして使用
      console.log('Upload successful:', response);
    } catch (error) {
      console.error('Upload failed:', error);
      alert('PDFのアップロードに失敗しました。');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <div style={{ flex: 1, borderRight: '1px solid #ccc', padding: '1rem' }}>
        {isUploading ? (
          <div>アップロード中...</div>
        ) : (
          <PdfViewer pdfUrl={currentPdf} onFileUpload={handleFileUpload} />
        )}
      </div>
      <div style={{ flex: 1, padding: '1rem' }}>
        {sessionId ? (
          <ChatWindow sessionId={sessionId} />
        ) : (
          <div>PDFをアップロードしてチャットを開始してください。</div>
        )}
      </div>
    </div>
  );
}

export default MainPage;