import { boot } from 'quasar/wrappers'
import { Notify } from 'quasar'

export default boot(({ app }) => {
  app.config.errorHandler = (err, instance, info) => {
    console.error('[Global Error]', err, info)

    try {
      Notify.create({
        type: 'negative',
        message: 'An unexpected error occurred. Please try again.',
        caption: String(err).slice(0, 200),
        timeout: 8000,
        multiLine: true,
        actions: [{ label: 'Dismiss', color: 'white' }],
      })
    } catch {
      // Notify may not be available if error is during initial boot
    }
  }

  window.addEventListener('unhandledrejection', (event) => {
    console.error('[Unhandled Promise Rejection]', event.reason)
    try {
      Notify.create({
        type: 'warning',
        message: 'Operation failed. Please try again.',
        caption: String(event.reason).slice(0, 200),
        timeout: 6000,
      })
    } catch {}
  })
})
