import { defineStore } from 'pinia'
import api from '../api'

interface DailyRevenue {
  date: string
  total: number
  cash: number
  bank_transfer: number
}

interface DailyAttendance {
  date: string
  total_sessions: number
  attended: number
  absent: number
  attendance_rate: number
}

interface MonthlyEnrollment {
  month: string
  new_enrollments: number
  cancelled: number
  net_change: number
}

interface CoachPerformance {
  coach_id: string
  coach_name: string
  sessions_held: number
  avg_attendance: number
  avg_rating: number
}

export const useAnalyticsStore = defineStore('analytics', {
  state: () => ({
    dailyRevenue: [] as DailyRevenue[],
    dailyAttendance: [] as DailyAttendance[],
    monthlyEnrollment: [] as MonthlyEnrollment[],
    coachPerformance: [] as CoachPerformance[],
    loading: false,
    error: null as string | null,
  }),

  actions: {
    async fetchRevenue(params?: Record<string, unknown>) {
      this.loading = true
      try {
        const response = await api.get('analytics/revenue/', { params })
        this.dailyRevenue = response.data.results || response.data
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch revenue data'
      } finally {
        this.loading = false
      }
    },

    async fetchAttendance(params?: Record<string, unknown>) {
      this.loading = true
      try {
        const response = await api.get('analytics/attendance/', { params })
        this.dailyAttendance = response.data.results || response.data
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch attendance data'
      } finally {
        this.loading = false
      }
    },

    async fetchEnrollment(params?: Record<string, unknown>) {
      this.loading = true
      try {
        const response = await api.get('analytics/enrollment/', { params })
        this.monthlyEnrollment = response.data.results || response.data
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch enrollment data'
      } finally {
        this.loading = false
      }
    },

    async fetchCoachPerformance(params?: Record<string, unknown>) {
      this.loading = true
      try {
        const response = await api.get('analytics/coach-performance/', { params })
        this.coachPerformance = response.data.results || response.data
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch coach performance'
      } finally {
        this.loading = false
      }
    },

    reset() {
      this.dailyRevenue = []
      this.dailyAttendance = []
      this.monthlyEnrollment = []
      this.coachPerformance = []
      this.loading = false
      this.error = null
    },
  },
})
