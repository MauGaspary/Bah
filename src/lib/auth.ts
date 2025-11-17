export interface LoginResponse {
  access_token: string
  user: {
    id: string
    email: string
    name: string
  }
}

export interface LoginCredentials {
  email: string
  password: string
}

export function logout(){
  removeToken()
  // Redireciona para a página de login usando window.location
  window.location.replace('/admin')
}

export async function login(
  email: string,
  password: string
): Promise<LoginResponse> {
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  })

  if (!response.ok) {
    throw new Error(`Login failed: ${response.status} ${response.statusText}`)
  }

  const data = await response.json()
  return data
}

export function verify_token(token: string): Record<string, unknown> {
  if (token && token.includes('.')) {
    const parts = token.split('.')
    if (parts.length === 3) {
      const decoded = atob(parts[1])
      try {
        const payload = JSON.parse(decoded)
        if (payload && typeof payload === 'object') {
          // Verifica se o token não expirou
          if (payload.exp && typeof payload.exp === 'number') {
            const currentTime = Math.floor(Date.now() / 1000)
            if (payload.exp < currentTime) {
              throw new Error('Token expired')
            }
          }
          return payload as Record<string, unknown>
        }
      } catch (error) {
        throw error
      }
    }
  }
  throw new Error('Invalid token')
}

export function getToken(): string | null {
  return localStorage.getItem('access_token')
}

export function setToken(token: string): void {
  localStorage.setItem('access_token', token)
}

export function removeToken(): void {
  localStorage.removeItem('access_token')
}

export function is_authenticated(): boolean {
  const token = localStorage.getItem('access_token')
  if (!token) return false

  try {
    verify_token(token)
    return true
  } catch {
    return false
  }
}

export interface UserInfo {
  name: string
  email: string
}

export function getUserFromToken(): UserInfo | null {
  const token = getToken()
  if (!token) return null

  try {
    const payload = verify_token(token)
    const name = (payload.name || payload.sub || 'Usuário') as string
    const email = (payload.email || '') as string
    return { name, email }
  } catch {
    return null
  }
}
