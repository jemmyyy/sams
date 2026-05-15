import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const api = axios.create({
  baseURL: process.env.API_URL || 'http://localhost/api/v1/',
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

// Bulletproof 401/403 Handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore();
      authStore.logout();
    }
    return Promise.reject(error);
  }
);

export default api;
