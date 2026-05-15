import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const api = axios.create({
  baseURL: process.env.API_URL || '/api/v1/',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  const academyId = localStorage.getItem('academy_id');

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  if (academyId) {
    config.headers['X-Academy-ID'] = academyId;
  }
  return config;
});

// Unwrap StandardizedJSONRenderer: backend wraps all responses in { success, data, errors, message }
// Strip the wrapper so the rest of the app receives the original payload.
api.interceptors.response.use(
  (response) => {
    if (response.data && typeof response.data === 'object' && 'success' in response.data && 'data' in response.data) {
      response.data = response.data.data;
    }
    return response;
  },
  (error) => {
    // Unwrap error responses too: extract the original errors from the wrapper
    if (error.response?.data && typeof error.response.data === 'object' && 'errors' in error.response.data) {
      error.response.data = error.response.data.errors;
    }

    // Do NOT logout on 401 from the login endpoint — that's a failed login attempt.
    if (error.response?.status === 401) {
      const isLoginRequest = error.config?.url?.includes('/login/');
      if (!isLoginRequest) {
        const authStore = useAuthStore();
        authStore.logout();
      }
    }
    return Promise.reject(error);
  }
);

export default api;
