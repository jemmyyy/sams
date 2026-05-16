import { useAuthStore } from '@/stores/auth'
import { api } from '@/api'

export function useApi() {
  const auth = useAuthStore()

  async function get<T>(url: string, params?: Record<string, unknown>) {
    const response = await api.get<T>(url, { params })
    return response.data
  }

  async function post<T>(url: string, data?: unknown) {
    const response = await api.post<T>(url, data)
    return response.data
  }

  async function put<T>(url: string, data?: unknown) {
    const response = await api.put<T>(url, data)
    return response.data
  }

  async function patch<T>(url: string, data?: unknown) {
    const response = await api.patch<T>(url, data)
    return response.data
  }

  async function del(url: string) {
    await api.delete(url)
  }

  function getAcademyHeader() {
    return { 'X-Academy-ID': auth.currentAcademyId || '' }
  }

  return { get, post, put, patch, del, getAcademyHeader }
}
