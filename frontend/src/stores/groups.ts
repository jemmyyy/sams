import { defineStore } from 'pinia'
import api from '../api'
import type { Group, PaginatedResponse } from '../types'

export const useGroupStore = defineStore('groups', {
  state: () => ({
    groups: [] as Group[],
    currentGroup: null as Group | null,
    loading: false,
    error: null as string | null,
  }),

  actions: {
    async fetchGroups(params?: Record<string, unknown>) {
      this.loading = true
      try {
        const response = await api.get<PaginatedResponse<Group>>('groups/', { params })
        this.groups = response.data.results || response.data || []
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch groups'
      } finally {
        this.loading = false
      }
    },

    async fetchGroup(id: string) {
      this.loading = true
      try {
        const response = await api.get<Group>(`groups/${id}/`)
        this.currentGroup = response.data
        return response.data
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch group'
        return null
      } finally {
        this.loading = false
      }
    },

    async createGroup(data: Partial<Group>) {
      try {
        const response = await api.post<Group>('groups/', data)
        this.groups.push(response.data)
        return response.data
      } catch (err: any) {
        throw err
      }
    },

    async updateGroup(id: string, data: Partial<Group>) {
      try {
        const response = await api.patch<Group>(`groups/${id}/`, data)
        const idx = this.groups.findIndex((g) => g.id === id)
        if (idx !== -1) this.groups[idx] = response.data
        if (this.currentGroup?.id === id) this.currentGroup = response.data
        return response.data
      } catch (err: any) {
        throw err
      }
    },

    async deleteGroup(id: string) {
      try {
        await api.delete(`groups/${id}/`)
        this.groups = this.groups.filter((g) => g.id !== id)
        if (this.currentGroup?.id === id) this.currentGroup = null
      } catch (err: any) {
        throw err
      }
    },

    async addPlayer(groupId: string, playerId: string) {
      try {
        return await api.post(`groups/${groupId}/add-player/`, { player_id: playerId })
      } catch (err: any) {
        throw err
      }
    },

    async removePlayer(groupId: string, playerId: string) {
      try {
        return await api.post(`groups/${groupId}/remove-player/`, { player_id: playerId })
      } catch (err: any) {
        throw err
      }
    },

    reset() {
      this.groups = []
      this.currentGroup = null
      this.loading = false
      this.error = null
    },
  },
})
