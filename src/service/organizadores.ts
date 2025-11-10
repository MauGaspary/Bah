import api from './api'
import type { Organizador } from '@/interfaces/IOrganizador'

export interface OrganizadorCreate {
  nome: string
}

export interface OrganizadorUpdate {
  nome?: string
}

export async function fetchOrganizadores(): Promise<Organizador[]> {
  const response = await api.get<Organizador[]>('/admin/organizadores/')
  return response.data
}

export async function fetchOrganizadorById(
  organizadorId: string
): Promise<Organizador> {
  const response = await api.get<Organizador>(
    `/admin/organizadores/${organizadorId}`
  )
  return response.data
}

export async function createOrganizador(
  organizadorData: OrganizadorCreate
): Promise<Organizador> {
  const response = await api.post<Organizador>(
    '/admin/organizadores/',
    organizadorData
  )
  return response.data
}

export async function updateOrganizador(
  organizadorId: string,
  organizadorData: OrganizadorUpdate
): Promise<Organizador> {
  const response = await api.patch<Organizador>(
    `/admin/organizadores/${organizadorId}`,
    organizadorData
  )
  return response.data
}

export async function deleteOrganizador(
  organizadorId: string
): Promise<void> {
  await api.delete(`/admin/organizadores/${organizadorId}`)
}
