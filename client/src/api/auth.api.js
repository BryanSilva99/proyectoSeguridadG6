import axios from 'axios';
import apiClient from './api.service';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1/';
const authClient = axios.create({ baseURL: BASE_URL, headers: { 'Content-Type': 'application/json' } });

export const login = (credentials) => {
  // POST /auth/login/
  return authClient.post('/auth/login/', credentials).then(res => res.data);
};

export const register = (payload) => {
  return authClient.post('/auth/register/', payload).then(res => res.data);
};

export const logout = (refreshToken) => {
  // POST /auth/logout/ requires Authorization header (apiClient will add it)
  return apiClient.post('/auth/logout/', { refresh: refreshToken }).then(res => res.data);
};

export const refresh = (refreshToken) => {
  // POST /auth/refresh/
  return authClient.post('/auth/refresh/', { refresh: refreshToken }).then(res => res.data);
};

export const me = () => {
  return apiClient.get('/auth/me/').then(res => res.data);
};

export const verify = () => {
  return apiClient.get('/auth/verify/').then(res => res.data);
};

export default { login, register, logout, refresh, me, verify };
