import React, { useState } from 'react';

function SettingsForm({ initialSettings, ollamaModels, onSave }) {
  const [ollama, setOllama] = useState(initialSettings.ollama);
  const [rag, setRag] = useState(initialSettings.rag);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({ ollama, rag });
  };

  const handleOllamaChange = (e) => {
    setOllama({ ...ollama, [e.target.name]: e.target.value });
  };

  const handleRagChange = (e) => {
    const value = parseInt(e.target.value, 10);
    setRag({ ...rag, [e.target.name]: isNaN(value) ? 0 : value });
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: '600px' }}>
      <fieldset style={fieldsetStyle}>
        <legend>Ollamaモデル設定</legend>
        <div style={formGroupStyle}>
          <label htmlFor="llm_model">LLMモデル:</label>
          <select id="llm_model" name="llm_model" value={ollama.llm_model} onChange={handleOllamaChange}>
            {ollamaModels.map(model => (
              <option key={model.name} value={model.name}>{model.name}</option>
            ))}
          </select>
        </div>
        <div style={formGroupStyle}>
          <label htmlFor="embedding_model">Embeddingモデル:</label>
          <select id="embedding_model" name="embedding_model" value={ollama.embedding_model} onChange={handleOllamaChange}>
             {ollamaModels.map(model => (
              <option key={model.name} value={model.name}>{model.name}</option>
            ))}
          </select>
        </div>
      </fieldset>

      <fieldset style={fieldsetStyle}>
        <legend>RAGパラメータ設定</legend>
        <div style={formGroupStyle}>
          <label htmlFor="chunk_size">チャンクサイズ:</label>
          <input type="number" id="chunk_size" name="chunk_size" value={rag.chunk_size} onChange={handleRagChange} min="0" /> {/* 追加 */}
        </div>
        <div style={formGroupStyle}>
          <label htmlFor="chunk_overlap">チャンクオーバーラップ:</label>
          <input type="number" id="chunk_overlap" name="chunk_overlap" value={rag.chunk_overlap} onChange={handleRagChange} min="0" /> {/* 追加 */}
        </div>
        <div style={formGroupStyle}>
          <label htmlFor="top_k">検索するチャンク数 (Top-K):</label>
          <input type="number" id="top_k" name="top_k" value={rag.top_k} onChange={handleRagChange} />
        </div>
      </fieldset>

      <button type="submit" style={{ padding: '10px 20px', backgroundColor: "#4CAF50", color: "white" }}>保存</button> {/* 修正 */}
    </form>
  );
}

// 簡単なスタイル定義
const fieldsetStyle = { border: '1px solid #ccc', padding: '1rem', marginBottom: '1rem' };
const formGroupStyle = { marginBottom: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' };

export default SettingsForm;