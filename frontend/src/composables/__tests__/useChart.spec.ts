import { describe, it, expect } from 'vitest'
import { useChart } from '../useChart'

describe('useChart composable', () => {
  it('returns dark theme colors', () => {
    const { darkTheme } = useChart()
    expect(darkTheme.value).toHaveProperty('color')
    expect(darkTheme.value).toHaveProperty('borderColor')
    expect(darkTheme.value).toHaveProperty('backgroundColor')
    expect(darkTheme.value).toHaveProperty('grid')
  })

  it('baseOptions returns responsive config', () => {
    const { baseOptions } = useChart()
    const opts = baseOptions()
    expect(opts.responsive).toBe(true)
    expect(opts.maintainAspectRatio).toBe(false)
    expect(opts.plugins?.legend?.labels?.color).toBe('#9CA3AF')
  })

  it('baseOptions merges overrides', () => {
    const { baseOptions } = useChart()
    const opts = baseOptions({ animation: false })
    expect(opts.animation).toBe(false)
    expect(opts.responsive).toBe(true)
  })
})
