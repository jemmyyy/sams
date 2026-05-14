import axios from 'axios';

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

export default api;
