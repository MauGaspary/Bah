const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000'

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

export async function login(
  email: string,
  password: string
): Promise<LoginResponse> {
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

export function make_token(payload: Record<string, unknown>): string {
  const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }))
  const payloadEncoded = btoa(JSON.stringify(payload))
  const signature = btoa('mock-signature')

  return `${header}.${payloadEncoded}.${signature}`
}

export function verify_token(token: string): Record<string, unknown> {
  if (token && token.includes('.')) {
    const parts = token.split('.')
    if (parts.length === 3) {
      const decoded = atob(parts[1])
      try {
        const payload = JSON.parse(decoded)
        if (payload && typeof payload === 'object') return payload as Record<string, unknown>
      } catch {
      }
    }
  }
  throw new Error('Invalid token')
}

export function extract_token(authHeader: string | null): string | null {
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return null
  }
  return authHeader.substring(7)
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
