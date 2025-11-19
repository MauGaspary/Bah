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
  console.log('222')
  //ERRO DA LISTA NA LINHA ABAIXO
  const response = await api.get<UsersResponse>('/admin/usuarios/', {
    params,
  })
  console.log('999');
  return response.data
}

export async function fetchUserById(userId: string): Promise<User> {
  const response = await api.get<User>(`/admin/usuarios/${userId}`)
  return response.data
}

export async function createUser(
  userData: UserCreate
): Promise<User> {
  const response = await api.post<User>('/admin/usuarios/', userData)
  return response.data
}

export async function deleteUser(userId: string): Promise<void> {
  await api.delete(`/admin/usuarios/${userId}`)
}

export async function patchUser(
  userId: string,
  payload: UserPatch
): Promise<User> {
  const response = await api.patch<User>(`/admin/usuarios/${userId}`, payload)
  return response.data
}