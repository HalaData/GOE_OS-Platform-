import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v2';

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// واجهات API
export const governanceAPI = {
  analyze: (data: { text: string; domain?: string; consent_given?: boolean }) =>
    apiClient.post('/govern', data),
  getIndicators: () => apiClient.get('/govern/indicators'),
};

export const generationAPI = {
  generateCode: (data: { description: string; language?: string }) =>
    apiClient.post('/generate/code', data),
  generateContent: (data: { topic: string; type?: string }) =>
    apiClient.post('/generate/content', data),
};

export const foresightAPI = {
  generateScenarios: (data: { domain: string; count?: number }) =>
    apiClient.post('/foresight/scenarios', data),
};

export const translationAPI = {
  translate: (data: { text: string; target_lang: string }) =>
    apiClient.post('/translate', data),
  getLanguages: () => apiClient.get('/translate/languages'),
};

export const statusAPI = {
  getStatus: () => apiClient.get('/status'),
};
