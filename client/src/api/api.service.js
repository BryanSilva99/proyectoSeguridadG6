import axios from 'axios';

// base URL from Vite env, fallback to localhost
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1/';

// axios instance used across the app
export const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' }
});

// Helper axios instance without interceptors for auth calls (refresh/login)
const plainClient = axios.create({ baseURL: BASE_URL });

// Request interceptor: attach access token if present
apiClient.interceptors.request.use(config => {
  try {
    const token = localStorage.getItem('access_token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
  } catch (err) {
    // ignore
  }
  return config;
}, error => Promise.reject(error));

// Response interceptor: try refresh on 401
apiClient.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refresh = localStorage.getItem('refresh_token');
      if (!refresh) {
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(error);
      }

      try {
        const { data } = await plainClient.post('/auth/refresh/', { refresh });

        // persist new tokens
        if (data.access) localStorage.setItem('access_token', data.access);
        if (data.refresh) localStorage.setItem('refresh_token', data.refresh);

        // set header and retry original request
        originalRequest.headers.Authorization = `Bearer ${data.access}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // refresh failed -> clear and redirect to login
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export const setAccessToken = token => {
  if (token) localStorage.setItem('access_token', token);
  else localStorage.removeItem('access_token');
};

export const setRefreshToken = token => {
  if (token) localStorage.setItem('refresh_token', token);
  else localStorage.removeItem('refresh_token');
};

export default apiClient;
