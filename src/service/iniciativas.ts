import api from './api'
import type { IniciativasResponse } from '@/interfaces/IIniciativas'


export async function fetchIniciativas(searchQuery?: string): Promise<IniciativasResponse> {
    const response = await api.get<IniciativasResponse>('/admin/iniciativas', {
      params: searchQuery ? { q: searchQuery } : {},
    })
    return response.data
  }