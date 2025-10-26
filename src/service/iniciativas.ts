import api from './api'
import type {
  IniciativasResponse,
  IniciativaCreate,
  Iniciativa,
  IniciativaAdmin,
  IniciativaPatch,
} from '@/interfaces/IIniciativas'

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

export async function deleteIniciativa(iniciativaId: string): Promise<void> {
  await api.delete(`/admin/iniciativas/${iniciativaId}`)
}

export async function createIniciativa(
  iniciativaData: IniciativaCreate
): Promise<Iniciativa> {
  const response = await api.post<Iniciativa>(
    '/admin/iniciativas/',
    iniciativaData
  )
  return response.data
}

export async function fetchIniciativaById(
  iniciativaId: string
): Promise<IniciativaAdmin> {
  const response = await api.get<IniciativaAdmin>(
    `/admin/iniciativas/${iniciativaId}`
  )
  return response.data
}

export async function patchIniciativa(
  iniciativaId: string,
  payload: IniciativaPatch
): Promise<IniciativaAdmin> {
  const response = await api.patch<IniciativaAdmin>(
    `/admin/iniciativas/${iniciativaId}`,
    payload
  )
  return response.data
}
