import React, { useState, useEffect } from 'react';
import SettingsForm from '../components/SettingsForm';
import { getSettings, updateSettings, getOllamaModels } from '../services/api';

function SettingsPage() {
  const [settings, setSettings] = useState(null);
  const [models, setModels] = useState([]);
  const [status, setStatus] = useState('');

  useEffect(() => {
    // 初期設定とモデルリストをロード
    const loadData = async () => {
      try {
        const currentSettings = await getSettings();
        const ollamaModels = await getOllamaModels();
        setSettings(currentSettings);
        setModels(ollamaModels.models || []);
      } catch (error) {
        console.error('Failed to load data:', error);
        setStatus('設定の読み込みに失敗しました。');
      }
    };
    loadData();
  }, []);

  const handleSave = async (newSettings) => {
    try {
      setStatus('保存中...');
      const response = await updateSettings(newSettings);
      setSettings(newSettings);
      setStatus(`保存しました！ (${new Date().toLocaleTimeString()})`);
    } catch (error) {
      console.error('Failed to save settings:', error);
      setStatus('設定の保存に失敗しました。');
    }
  };

  if (!settings) {
    return <div>読み込み中...</div>;
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h1>設定</h1>
      <SettingsForm
        initialSettings={settings}
        ollamaModels={models}
        onSave={handleSave}
      />
      {status && <p style={{ marginTop: '1rem' }}>{status}</p>}
    </div>
  );
}

export default SettingsPage;