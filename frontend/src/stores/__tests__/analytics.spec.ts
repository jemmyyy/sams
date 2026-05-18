import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAnalyticsStore } from '../analytics'

describe('analytics store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('starts with empty state', () => {
    const store = useAnalyticsStore()
    expect(store.dailyRevenue).toEqual([])
    expect(store.dailyAttendance).toEqual([])
    expect(store.monthlyEnrollment).toEqual([])
    expect(store.coachPerformance).toEqual([])
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
  })

  it('resets state to defaults', () => {
    const store = useAnalyticsStore()
    store.dailyRevenue = [{ date: '2026-01-01', total: 100, cash: 50, bank_transfer: 50 }]
    store.loading = true
    store.error = 'something broke'

    store.reset()

    expect(store.dailyRevenue).toEqual([])
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
  })
})
