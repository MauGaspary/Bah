import api from './api'
import type { IniciativasResponse } from '@/interfaces/IIniciativas'

export async function fetchIniciativas(
  searchQuery?: string,
  page: number = 1,
  size: number = 5
): Promise<IniciativasResponse> {
  const params: Record<string, string | number> = { page, size }
  if (searchQuery && searchQuery.trim().length > 0) {
    params.q = searchQuery
  }

  const response = await api.get<IniciativasResponse>('/admin/iniciativas', {
    params,
  })
  return response.data
}

export async function deleteIniciativa(iniciativaId: string | number): Promise<void> {
  await api.delete(`/admin/iniciativas/${iniciativaId}`)
}
