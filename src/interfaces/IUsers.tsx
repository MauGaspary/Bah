export interface UserCreate {
  nome: string
  sobrenome: string
  email: string
  password: string
}

export interface UsersListProps {
  searchQuery: string
}

export interface UsersResponse {
  items: User[]
  total: number
}

export interface UserResponse {
  id: string
  nome: string
  sobrenome: string
  email: string
  criado_em?: string
  criado_por?: string
  editado_em?: string
  editado_por?: string
}

export type User = UserResponse

export interface UserPatch {
  nome?: string
  sobrenome?: string
  email?: string
  senha?: string
}
