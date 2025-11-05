import api from './api'
import type { 
    UsersResponse, 
    User, 
    UserInterfaceCreate 
} from '@/interfaces/IUsers'

export async function fetchUsers(): Promise<UsersResponse> {
  const response = await api.get<UsersResponse>('/admin/users')
  return response.data
}

export async function createUser(
  userData: UserInterfaceCreate
): Promise<User> {
  const response = await api.post<User>('/admin/users', userData)
  return response.data
}

export async function getUserById(
  userId: string
): Promise<User> {
  const response = await api.get<User>(
    `/admin/users/${userId}`
  )
  return response.data
}

export async function deleteUser(userId: string): Promise<void> {
  await api.delete(`/admin/users/${userId}`)
}