import { createContext, useContext, useState, type ReactNode } from 'react'
import { login as authLogin } from '@/lib/auth'

interface AuthContextType {
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps { children: ReactNode }

export function AuthProvider({ children }: AuthProviderProps) {
  const [token, setToken] = useState<string | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const login = async (email: string, password: string) => {
    setIsLoading(true)
    try {
      const res = await authLogin(email, password)
      if (!res.access_token) throw new Error('Token ausente')
      setToken(res.access_token)
      setIsAuthenticated(true)
      localStorage.setItem('access_token', res.access_token)
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    setToken(null)
    setIsAuthenticated(false)
  }

  return (
    <AuthContext.Provider value={{ token, isAuthenticated, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth deve ser usado dentro de um AuthProvider')
  return context
}
