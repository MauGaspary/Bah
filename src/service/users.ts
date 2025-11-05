import api from './api'
import type { 
    UsersResponse, 
    User, 
    UserCreate, 
    UserPatch
} from '@/interfaces/IUsers'

export async function fetchUsers(
  searchQuery?: string,
  page: number = 1,
  size: number = 5
): Promise<UsersResponse> {
  const params: Record<string, string | number> = { page, size }
  if (searchQuery && searchQuery.trim().length > 0) {
    params.q = searchQuery
  }

  const response = await api.get<UsersResponse>('/admin/users', {
    params,
  })
  return response.data
}

export async function fetchUserById(userId: string): Promise<User> {
  const response = await api.get<User>(`/admin/users/${userId}`)
  return response.data
}

export async function createUser(
  userData: UserCreate
): Promise<User> {
  const response = await api.post<User>('/admin/users', userData)
  return response.data
}

export async function deleteUser(userId: string): Promise<void> {
  await api.delete(`/admin/users/${userId}`)
}

export async function patchUser(
  userId: string,
  payload: UserPatch
): Promise<User> {
  const response = await api.patch<User>(`/admin/users/${userId}`, payload)
  return response.data
}