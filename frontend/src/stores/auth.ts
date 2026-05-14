import { defineStore } from 'pinia';
import api from '../api';

interface User {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone_number: string;
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    isAuthenticated: !!localStorage.getItem('access_token'),
  }),
  actions: {
    async login(credentials: Record<string, string>) {
      const response = await api.post('accounts/login/', credentials);
      this.user = response.data.user;
      this.isAuthenticated = true;
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
    },
    logout() {
      this.user = null;
      this.isAuthenticated = false;
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  }
});
