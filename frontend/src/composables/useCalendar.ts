import { ref, computed } from 'vue'

export interface CalendarDay {
  date: Date
  dayNumber: number
  isCurrentMonth: boolean
  isToday: boolean
  iso: string
}

export function useCalendar() {
  const currentDate = ref(new Date())
  const viewMode = ref<'month' | 'week'>('month')

  const currentYear = computed(() => currentDate.value.getFullYear())
  const currentMonth = computed(() => currentDate.value.getMonth())

  const monthDays = computed(() => {
    const year = currentYear.value
    const month = currentMonth.value
    const firstDay = new Date(year, month, 1)
    const lastDay = new Date(year, month + 1, 0)
    const startPad = (firstDay.getDay() + 6) % 7 // Monday start
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    const days: CalendarDay[] = []

    for (let i = startPad - 1; i >= 0; i--) {
      const d = new Date(year, month, -i)
      days.push({ date: d, dayNumber: d.getDate(), isCurrentMonth: false, isToday: d.getTime() === today.getTime(), iso: d.toISOString().slice(0, 10) })
    }
    for (let i = 1; i <= lastDay.getDate(); i++) {
      const d = new Date(year, month, i)
      days.push({ date: d, dayNumber: i, isCurrentMonth: true, isToday: d.getTime() === today.getTime(), iso: d.toISOString().slice(0, 10) })
    }
    const remaining = 42 - days.length
    for (let i = 1; i <= remaining; i++) {
      const d = new Date(year, month + 1, i)
      days.push({ date: d, dayNumber: d.getDate(), isCurrentMonth: false, isToday: d.getTime() === today.getTime(), iso: d.toISOString().slice(0, 10) })
    }
    return days
  })

  const weeks = computed(() => {
    const result: CalendarDay[][] = []
    for (let i = 0; i < monthDays.value.length; i += 7) {
      result.push(monthDays.value.slice(i, i + 7))
    }
    return result
  })

  const weekDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

  function prevMonth() { currentDate.value = new Date(currentYear.value, currentMonth.value - 1, 1) }
  function nextMonth() { currentDate.value = new Date(currentYear.value, currentMonth.value + 1, 1) }
  function goToday() { currentDate.value = new Date() }

  const monthLabel = computed(() =>
    currentDate.value.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
  )

  return { viewMode, currentDate, monthDays, weeks, weekDays, prevMonth, nextMonth, goToday, monthLabel }
}
