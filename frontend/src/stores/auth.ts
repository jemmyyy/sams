import { defineStore } from 'pinia';
import api from '../api';

interface User {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone_number: string;
  roles: string[];
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    isAuthenticated: !!localStorage.getItem('access_token'),
    isInitialized: false,
    authError: null as string | null,
  }),
  getters: {
    hasRole: (state) => (role: string) => {
      if (!state.user) return false;
      return state.user.roles.includes(role) || 
             state.user.roles.includes('admin') || 
             state.user.roles.includes('super_admin');
    },
    primaryPortal: (state) => {
      if (!state.user) return 'home';
      const r = state.user.roles;
      if (r.includes('admin') || r.includes('operations')) return 'ops-dashboard';
      if (r.includes('coach')) return 'coach-timetable';
      if (r.includes('customer')) return 'customer-timetable';
      // If user is logged in but has NO known roles, send to a profile page or error
      return 'customer-profile'; 
    }
  },
  actions: {
    async init() {
      if (!this.isAuthenticated) {
        this.isInitialized = true;
        this.user = null;
        return;
      }
      try {
        const response = await api.get('accounts/profile/');
        this.user = response.data;
        this.isInitialized = true;
        this.authError = null;
      } catch (error) {
        console.error('Session initialization failed:', error);
        // Don't call logout() here because it does a hard redirect, 
        // just reset the state and let the guard handle it.
        this.isAuthenticated = false;
        this.user = null;
        this.isInitialized = true;
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
    },
    async login(credentials: Record<string, string>) {
      try {
        const response = await api.post('accounts/login/', credentials);
        this.user = response.data.user;
        this.isAuthenticated = true;
        this.isInitialized = true;
        this.authError = null;
        
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        // Also save user for immediate recovery on refresh before init finishes
        localStorage.setItem('user_meta', JSON.stringify(response.data.user));
      } catch (error: any) {
        this.authError = error.response?.data?.detail || 'Authentication failed';
        throw error;
      }
    },
    logout() {
      // 1. Clear memory state
      this.user = null;
      this.isAuthenticated = false;
      this.isInitialized = true;
      this.authError = null;
      
      // 2. Clear all sensitive local storage
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user_meta');
      localStorage.removeItem('academy_id');
      
      // 3. Force hard reload to home to kill all intervals/zombie states
      window.location.href = '/';
    }
  }
});
