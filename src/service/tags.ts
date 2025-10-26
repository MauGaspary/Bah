import api from './api'
import type { Tag } from '@/interfaces/ITag'

export async function fetchTags(): Promise<Tag[]> {
  const response = await api.get<Tag[]>('/tags')
  return response.data
}
