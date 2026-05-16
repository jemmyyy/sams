import { defineStore } from 'pinia'
import api from '../api'
import type { Coach, CoachAvailability, PaginatedResponse } from '../types'

export const useCoachStore = defineStore('coaches', {
  state: () => ({
    coaches: [] as Coach[],
    currentCoach: null as Coach | null,
    loading: false,
    error: null as string | null,
  }),

  actions: {
    async fetchCoaches(params?: Record<string, unknown>) {
      this.loading = true
      try {
        const response = await api.get<PaginatedResponse<Coach>>('coaches/profiles/', { params })
        this.coaches = response.data.results
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch coaches'
      } finally {
        this.loading = false
      }
    },

    async fetchCoach(id: string) {
      this.loading = true
      try {
        const response = await api.get<Coach>(`coaches/profiles/${id}/`)
        this.currentCoach = response.data
        return response.data
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch coach'
        return null
      } finally {
        this.loading = false
      }
    },

    async createCoach(data: Partial<Coach>) {
      try {
        const response = await api.post<Coach>('coaches/profiles/', data)
        this.coaches.push(response.data)
        return response.data
      } catch (err: any) {
        throw err
      }
    },

    async updateCoach(id: string, data: Partial<Coach>) {
      try {
        const response = await api.patch<Coach>(`coaches/profiles/${id}/`, data)
        const idx = this.coaches.findIndex((c) => c.id === id)
        if (idx !== -1) this.coaches[idx] = response.data
        if (this.currentCoach?.id === id) this.currentCoach = response.data
        return response.data
      } catch (err: any) {
        throw err
      }
    },

    async toggleActive(id: string) {
      try {
        const response = await api.post<{ is_active: boolean }>(`coaches/profiles/${id}/toggle-active/`)
        const coach = this.coaches.find((c) => c.id === id)
        if (coach) coach.is_active = response.data.is_active
        if (this.currentCoach?.id === id) this.currentCoach.is_active = response.data.is_active
      } catch (err: any) {
        throw err
      }
    },

    async fetchWorkload(id: string) {
      try {
        return await api.get(`coaches/profiles/${id}/workload/`)
      } catch (err: any) {
        return null
      }
    },

    async fetchAvailabilities(coachId: string) {
      try {
        const response = await api.get(`coaches/profiles/${coachId}/availabilities/`)
        return response.data
      } catch (err: any) {
        return []
      }
    },

    async addAvailability(coachId: string, data: Partial<CoachAvailability>) {
      try {
        return await api.post(`coaches/profiles/${coachId}/availabilities/`, data)
      } catch (err: any) {
        throw err
      }
    },

    async updateAvailability(coachId: string, availId: string, data: Partial<CoachAvailability>) {
      try {
        return await api.patch(`coaches/profiles/${coachId}/availabilities/${availId}/`, data)
      } catch (err: any) {
        throw err
      }
    },

    async removeAvailability(coachId: string, availId: string) {
      try {
        await api.delete(`coaches/profiles/${coachId}/availabilities/${availId}/`)
      } catch (err: any) {
        throw err
      }
    },

    reset() {
      this.coaches = []
      this.currentCoach = null
      this.loading = false
      this.error = null
    },
  },
})
