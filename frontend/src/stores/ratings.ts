import { defineStore } from 'pinia';
import api from '../api';

export interface PlayerRating {
  id: string;
  player: string;
  coach: string;
  technique: number;
  stamina: number;
  teamwork: number;
  notes?: string;
  created_at?: string;
}

export const useRatingsStore = defineStore('ratings', {
  state: () => ({
    ratings: [] as PlayerRating[],
    loading: false,
    error: null as string | null,
  }),
  actions: {
    async fetchRatings(playerId?: string) {
      this.loading = true;
      try {
        const params = playerId ? { player: playerId } : {};
        const response = await api.get('ratings/', { params });
        this.ratings = response.data.results || response.data;
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch ratings';
      } finally {
        this.loading = false;
      }
    },
    async submitRating(data: Partial<PlayerRating>) {
      try {
        const response = await api.post('ratings/', data);
        this.ratings.push(response.data);
        return response.data;
      } catch (err: any) {
        throw err;
      }
    }
  }
});
