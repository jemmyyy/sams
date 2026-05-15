import { defineStore } from 'pinia';
import api from '../api';

export interface Player {
  id: string;
  first_name: string;
  last_name: string;
  registration_number: string;
  birth_date: string;
  gender: string;
  medical_conditions?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
}

export const usePlayersStore = defineStore('players', {
  state: () => ({
    players: [] as Player[],
    loading: false,
    error: null as string | null,
  }),
  actions: {
    async fetchPlayers() {
      this.loading = true;
      try {
        const response = await api.get('players/');
        // Handle both paginated and non-paginated responses
        this.players = Array.isArray(response.data) ? response.data : response.data.results || [];
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch players';
      } finally {
        this.loading = false;
      }
    },
    async addPlayer(playerData: Partial<Player>) {
      try {
        const response = await api.post('players/', playerData);
        this.players.push(response.data);
        return response.data;
      } catch (err: any) {
        throw err;
      }
    }
  }
});
