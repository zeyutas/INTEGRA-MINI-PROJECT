import api from './api';

const ACCESS_TOKEN_KEY = 'access';
const REFRESH_TOKEN_KEY = 'refresh';

export async function login({ username, password }) {
  const payload = {
    username: (username || '').trim(),
    password: (password || '').trim()
  };

  const { data } = await api.post('/auth/login/', payload);
  const { access, refresh } = data || {};

  if (!access || !refresh) {
    throw new Error('登录响应缺少令牌');
  }

  persistTokens({ access, refresh });
  return { access, refresh };
}

export function persistTokens({ access, refresh }) {
  localStorage.setItem(ACCESS_TOKEN_KEY, access);
  localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
}

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function isAuthenticated() {
  return Boolean(getAccessToken());
}

export function logout() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}
