import api from './api'
import type { Organizador } from '@/interfaces/IOrganizador'

export async function fetchOrganizadores(): Promise<Organizador[]> {
  const response = await api.get<Organizador[]>('/organizadores')
  return response.data
}
