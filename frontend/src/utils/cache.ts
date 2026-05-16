const store = new Map<string, { data: unknown; expiry: number }>()

export function cacheGet<T>(key: string): T | null {
  const entry = store.get(key)
  if (!entry) return null
  if (Date.now() > entry.expiry) {
    store.delete(key)
    return null
  }
  return entry.data as T
}

export function cacheSet(key: string, data: unknown, ttlMs = 5 * 60 * 1000): void {
  store.set(key, { data, expiry: Date.now() + ttlMs })
}

export function cacheClear(key?: string): void {
  if (key) {
    store.delete(key)
  } else {
    store.clear()
  }
}

export function cacheHas(key: string): boolean {
  return cacheGet(key) !== null
}
