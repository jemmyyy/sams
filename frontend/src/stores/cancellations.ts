import { defineStore } from 'pinia';
import api from '../api';

export interface Cancellation {
  id: string;
  session: string;
  player: string;
  reason: string;
  status: 'Pending' | 'Approved' | 'Rejected';
  created_at: string;
}

export const useCancellationsStore = defineStore('cancellations', {
  state: () => ({
    cancellations: [] as Cancellation[],
    loading: false,
    error: null as string | null,
  }),
  actions: {
    async fetchCancellations() {
      this.loading = true;
      try {
        const response = await api.get('cancellations/');
        this.cancellations = response.data.results || response.data;
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch cancellations';
      } finally {
        this.loading = false;
      }
    },
    async requestCancellation(data: Partial<Cancellation>) {
      try {
        const response = await api.post('cancellations/', data);
        this.cancellations.push(response.data);
        return response.data;
      } catch (err: any) {
        throw err;
      }
    }
  }
});
