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

export async function deleteIniciativa(iniciativaId: number): Promise<void> {
  await api.delete(`/admin/iniciativas/${iniciativaId}`)
}

export type CreateIniciativaPayload = {
  titulo: string
  descricao: string
  organizador_id: string
  link: string
  local: string
  imagem_url: string
  destaque: boolean
  horarios: Array<{
    data_evento: string
    hora_inicio: string
    hora_fim: string
    tipo: string
  }>
  tag_ids: string[]
  descricoes_extras?: string[]
}

export async function createIniciativa(
  payload: CreateIniciativaPayload
): Promise<void> {
  await api.post('/admin/iniciativas', payload)
}
