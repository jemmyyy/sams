import { defineStore } from 'pinia';
import api from '../api';

export interface AttendanceRecord {
  id: string;
  session: string;
  player: string;
  status: 'Present' | 'Absent' | 'Late' | 'Excused';
  notes?: string;
  marked_by?: string;
  created_at?: string;
}

export const useAttendanceStore = defineStore('attendance', {
  state: () => ({
    records: [] as AttendanceRecord[],
    loading: false,
    error: null as string | null,
  }),
  actions: {
    async fetchAttendance(sessionId?: string) {
      this.loading = true;
      try {
        const params = sessionId ? { session: sessionId } : {};
        const response = await api.get('attendance/', { params });
        this.records = response.data.results || response.data;
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch attendance';
      } finally {
        this.loading = false;
      }
    },
    async markAttendance(data: Partial<AttendanceRecord>) {
      try {
        const response = await api.post('attendance/', data);
        this.records.push(response.data);
        return response.data;
      } catch (err: any) {
        throw err;
      }
    }
  }
});
