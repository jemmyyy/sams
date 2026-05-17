import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const api = axios.create({
  baseURL: process.env.API_URL || '/api/v1/',
});

let isRefreshing = false;
let failedQueue: Array<{
  resolve: (token: string) => void;
  reject: (error: unknown) => void;
}> = [];

const processQueue = (error: unknown, token: string | null = null) => {
  failedQueue.forEach((promise) => {
    if (error) {
      promise.reject(error);
    } else {
      promise.resolve(token!);
    }
  });
  failedQueue = [];
};

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  const academyId = localStorage.getItem('academy_id');

  // Skip tenant header for auth endpoints — no academy scoping needed
  const isAuthEndpoint = config.url?.includes('accounts/login/')
    || config.url?.includes('accounts/register/')
    || config.url?.includes('token/refresh/')
    || config.url?.includes('token/verify/');

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  if (academyId && !isAuthEndpoint) {
    config.headers['X-Academy-ID'] = academyId;
  }
  return config;
});

// Unwrap StandardizedJSONRenderer response wrapper
api.interceptors.response.use(
  (response) => {
    if (response.data && typeof response.data === 'object' && 'success' in response.data && 'data' in response.data) {
      response.data = response.data.data;
    }
    return response;
  },
  async (error) => {
    if (error.response?.data && typeof error.response.data === 'object' && 'errors' in error.response.data) {
      error.response.data = error.response.data.errors;
    }

    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      const isLoginRequest = originalRequest?.url?.includes('login/');
      const isRefreshRequest = originalRequest?.url?.includes('token/refresh/');

      if (isLoginRequest || isRefreshRequest) {
        return Promise.reject(error);
      }

      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
        const authStore = useAuthStore();
        authStore.logout();
        return Promise.reject(error);
      }

      if (isRefreshing) {
        return new Promise<string>((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return api(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const response = await axios.post(
          `${api.defaults.baseURL}accounts/token/refresh/`,
          { refresh: refreshToken }
        );
        const newAccessToken = response.data.access;
        localStorage.setItem('access_token', newAccessToken);
        processQueue(null, newAccessToken);
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        const authStore = useAuthStore();
        authStore.logout();
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default api;
