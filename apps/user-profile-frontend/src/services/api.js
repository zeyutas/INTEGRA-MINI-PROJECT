import axios from 'axios';
import { getAccessToken } from './auth';

// Use proxy (vue.config.js) in dev to avoid CORS; fallback to full URL if provided
export const API_BASE_URL =
  process.env.VUE_APP_API_BASE_URL || 'http://10.0.0.171:8000';

const api = axios.create({
  baseURL: process.env.NODE_ENV === 'development' ? '/api' : API_BASE_URL
});

api.interceptors.request.use(
  config => {
    const token = getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);


export default api;
