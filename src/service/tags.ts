import api from './api'
import type { Tag } from '@/interfaces/ITag'

export interface TagCreate {
  nome: string
  descricao?: string
}

export interface TagUpdate {
  nome?: string
  descricao?: string
}

export async function fetchTags(): Promise<Tag[]> {
  const response = await api.get<Tag[]>('/admin/tags')
  return response.data
}

export async function fetchTagById(tagId: string): Promise<Tag> {
  const response = await api.get<Tag>(`/admin/tags/${tagId}`)
  return response.data
}

export async function createTag(tagData: TagCreate): Promise<Tag> {
  const response = await api.post<Tag>('/admin/tags/', tagData)
  return response.data
}

export async function updateTag(
  tagId: string,
  tagData: TagUpdate
): Promise<Tag> {
  const response = await api.patch<Tag>(`/admin/tags/${tagId}`, tagData)
  return response.data
}

export async function deleteTag(tagId: string): Promise<void> {
  await api.delete(`/admin/tags/${tagId}`)
}
