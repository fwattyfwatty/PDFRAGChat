import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // バックエンドAPIのURL
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadPdf = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await apiClient.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getSettings = async () => {
  const response = await apiClient.get('/settings');
  return response.data;
};

export const updateSettings = async (settings) => {
  // バックエンドAPIのスキーマに合わせて整形
  const payload = {
    ollama_settings: settings.ollama,
    rag_settings: settings.rag
  };
  const response = await apiClient.post('/settings', payload);
  return response.data;
};

export const getOllamaModels = async () => {
  const response = await apiClient.get('/ollama/models');
  return response.data;
};