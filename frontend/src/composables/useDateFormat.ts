import { useI18n } from 'vue-i18n'

export function useDateFormat() {
  const { locale } = useI18n()

  function formatDate(date: string | Date, options?: Intl.DateTimeFormatOptions): string {
    const d = typeof date === 'string' ? new Date(date) : date
    const defaults: Intl.DateTimeFormatOptions = {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    }
    return d.toLocaleDateString(locale.value === 'ar-EG' ? 'ar-EG' : 'en-US', { ...defaults, ...options })
  }

  function formatDateTime(date: string | Date): string {
    const d = typeof date === 'string' ? new Date(date) : date
    return d.toLocaleDateString(locale.value === 'ar-EG' ? 'ar-EG' : 'en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  function formatTime(time: string): string {
    const [h, m] = time.split(':')
    const hours = parseInt(h, 10)
    const ampm = hours >= 12 ? 'PM' : 'AM'
    const h12 = hours % 12 || 12
    return `${h12}:${m} ${ampm}`
  }

  function timeAgo(date: string | Date): string {
    const d = typeof date === 'string' ? new Date(date) : date
    const now = Date.now()
    const diff = now - d.getTime()
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(diff / 3600000)
    const days = Math.floor(diff / 86400000)

    if (minutes < 1) return 'just now'
    if (minutes < 60) return `${minutes}m ago`
    if (hours < 24) return `${hours}h ago`
    if (days < 7) return `${days}d ago`
    return formatDate(date)
  }

  return { formatDate, formatDateTime, formatTime, timeAgo }
}
