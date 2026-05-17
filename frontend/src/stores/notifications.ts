import { defineStore } from 'pinia'
import api from '../api'
import type { Notification, PaginatedResponse } from '../types'

export const useNotificationStore = defineStore('notifications', {
  state: () => ({
    notifications: [] as Notification[],
    unreadCount: 0,
    loading: false,
    error: null as string | null,
  }),

  getters: {
    unread: (state) => state.notifications.filter((n) => !n.is_read),
  },

  actions: {
    async fetchNotifications(params?: Record<string, unknown>) {
      this.loading = true
      try {
        const response = await api.get<PaginatedResponse<Notification>>('notifications/my-notifications/', { params })
        this.notifications = response.data.results || []
        this.unreadCount = this.notifications.filter((n) => !n.is_read).length
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch notifications'
      } finally {
        this.loading = false
      }
    },

    async markRead(id: string) {
      try {
        await api.post(`notifications/my-notifications/${id}/mark-read/`)
        const n = this.notifications.find((n) => n.id === id)
        if (n) {
          n.is_read = true
          n.read_at = new Date().toISOString()
          this.unreadCount = Math.max(0, this.unreadCount - 1)
        }
      } catch (err: any) {
        this.error = err.message || 'Failed to mark notification as read'
      }
    },

    async markAllRead() {
      try {
        await api.post('notifications/my-notifications/mark-all-read/')
        this.notifications.forEach((n) => {
          n.is_read = true
          n.read_at = new Date().toISOString()
        })
        this.unreadCount = 0
      } catch (err: any) {
        this.error = err.message || 'Failed to mark all as read'
      }
    },

    reset() {
      this.notifications = []
      this.unreadCount = 0
      this.loading = false
      this.error = null
    },
  },
})
