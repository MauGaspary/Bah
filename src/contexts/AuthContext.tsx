import {
  createContext,
  useContext,
  useState,
  useEffect,
  type ReactNode,
} from 'react'
import { useNavigate, useLocation } from 'react-router-dom'

import {
  login as authLogin,
  setToken as setAuthToken,
  removeToken,
  getToken,
  is_authenticated,
} from '@/lib/auth'

const isProtectedRoute = (pathname: string): boolean => {
  return pathname.startsWith('/admin') && pathname !== '/admin'
}

interface AuthContextType {
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const navigate = useNavigate()
  const location = useLocation()

  const initAuth = () => {
    try {
      const existingToken = getToken()
      if (existingToken && is_authenticated()) {
        return { token: existingToken, isAuthenticated: true }
      } else {
        removeToken()
        return { token: null, isAuthenticated: false }
      }
    } catch (error) {
      removeToken()
      return { token: null, isAuthenticated: false }
    }
  }

  const initialState = initAuth()
  const [token, setToken] = useState<string | null>(initialState.token)
  const [isAuthenticated, setIsAuthenticated] = useState(
    initialState.isAuthenticated
  )
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    const interval = setInterval(() => {
      if (isAuthenticated && !is_authenticated()) {
        setToken(null)
        setIsAuthenticated(false)
        removeToken()
      }
    }, 30000)

    return () => clearInterval(interval)
  }, [isAuthenticated])

  useEffect(() => {
    const currentPath = location.pathname
    const isProtected = isProtectedRoute(currentPath)

    if (!isAuthenticated && isProtected) {
      navigate('/admin', { replace: true })
    }
  }, [isAuthenticated, location.pathname, navigate])

  const login = async (email: string, password: string) => {
    setIsLoading(true)
    try {
      const res = await authLogin(email, password)
      if (!res.access_token) throw new Error('Token ausente')

      try {
        setAuthToken(res.access_token)
        if (is_authenticated()) {
          setToken(res.access_token)
          setIsAuthenticated(true)
        } else {
          throw new Error('Token inválido')
        }
      } catch (tokenError) {
        removeToken()
        throw new Error('Token inválido recebido do servidor')
      }
    } catch (error) {
      setToken(null)
      setIsAuthenticated(false)
      removeToken()
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    setToken(null)
    setIsAuthenticated(false)
    removeToken()
  }

  const currentPath = location.pathname
  const isProtected = isProtectedRoute(currentPath)

  if (!isAuthenticated && isProtected) {
    return null
  }

  return (
    <AuthContext.Provider
      value={{ token, isAuthenticated, isLoading, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context)
    throw new Error('useAuth deve ser usado dentro de um AuthProvider')
  return context
}
