import React from 'react';
import { useDropzone } from 'react-dropzone';

function PdfViewer({ pdfUrl, onFileUpload }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: acceptedFiles => onFileUpload(acceptedFiles[0]),
    accept: { 'application/pdf': ['.pdf'] },
    multiple: false,
  });

  return (
    <div>
      {!pdfUrl ? (
        <div {...getRootProps()} style={dropzoneStyle}>
          <input {...getInputProps()} />
          {isDragActive ? (
            <p>ここにファイルをドロップ...</p>
          ) : (
            <p>PDFファイルをドラッグ＆ドロップするか、クリックして選択</p>
          )}
        </div>
      ) : (
        <iframe
          src={pdfUrl}
          title="PDF Viewer"
          width="100%"
          height="90vh"
          style={{ border: 'none' }}
        />
      )}
    </div>
  );
}

const dropzoneStyle = {
  border: '2px dashed #ccc',
  borderRadius: '5px',
  padding: '20px',
  textAlign: 'center',
  cursor: 'pointer',
  height: '80vh',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
};

export default PdfViewer;