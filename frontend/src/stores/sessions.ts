import { defineStore } from 'pinia';
import api from '../api';

export interface SessionOccurrence {
  id: string;
  series: string;
  date: string;
  start_time: string;
  end_time: string;
  status: 'scheduled' | 'live' | 'completed' | 'cancelled';
  venue?: string;
  coach?: string;
}

export const useSessionsStore = defineStore('sessions', {
  state: () => ({
    sessions: [] as SessionOccurrence[],
    loading: false,
    error: null as string | null,
  }),
  actions: {
    async fetchSessions() {
      this.loading = true;
      try {
        const response = await api.get('sessions/occurrences/');
        this.sessions = response.data.results || response.data;
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch sessions';
      } finally {
        this.loading = false;
      }
    },
    async cancelSession(id: string, reason: string) {
      try {
        await api.post(`sessions/occurrences/${id}/cancel/`, { reason });
        const index = this.sessions.findIndex(s => s.id === id);
        if (index !== -1) {
          this.sessions[index].status = 'cancelled';
        }
      } catch (err: any) {
        throw err;
      }
    }
  }
});
