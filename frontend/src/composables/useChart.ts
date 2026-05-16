import { computed } from 'vue'

export function useChart() {
  const darkTheme = computed(() => ({
    color: '#9CA3AF',
    borderColor: 'var(--sams-border, #2D2D2D)',
    backgroundColor: 'transparent',
    grid: { color: 'rgba(255,255,255,0.06)' },
  }))

  function baseOptions(overrides?: Record<string, unknown>) {
    return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: '#9CA3AF' } } },
      scales: {
        x: { ticks: { color: '#6B7280' }, grid: darkTheme.value.grid },
        y: { ticks: { color: '#6B7280' }, grid: darkTheme.value.grid },
      },
      ...overrides,
    }
  }

  return { darkTheme, baseOptions }
}
