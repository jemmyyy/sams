export function formatCurrency(amount: number | string, currency = 'EGP', locale = 'en-US'): string {
  const n = typeof amount === 'string' ? parseFloat(amount) : amount
  if (isNaN(n)) return '—'
  try {
    return new Intl.NumberFormat(locale === 'ar' ? 'ar-EG' : locale, {
      style: 'currency',
      currency,
      minimumFractionDigits: 2,
    }).format(n)
  } catch {
    return `${currency} ${n.toFixed(2)}`
  }
}

export function parseCurrency(formatted: string): number {
  const cleaned = formatted.replace(/[^0-9.\-]/g, '')
  return parseFloat(cleaned) || 0
}
