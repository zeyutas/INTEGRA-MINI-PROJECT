import axios from 'axios';
import { getAccessToken } from './auth';

// Use proxy (vue.config.js) in dev to avoid CORS; configure full URL via env for prod
export const API_BASE_URL =
  process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000';

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
