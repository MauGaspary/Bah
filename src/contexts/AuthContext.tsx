import {
  createContext,
  useContext,
  useState,
  useEffect,
  type ReactNode,
} from 'react'

import {
  login as authLogin,
  setToken as setAuthToken,
  removeToken,
  getToken,
  is_authenticated,
} from '@/lib/auth'

// Rotas protegidas que requerem autenticação
const PROTECTED_ROUTES = [
  '/admin/criarIniciativa',
  '/admin/usuarios',
  '/admin/iniciativas',
]

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
  // Inicialização síncrona para evitar piscada
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
  const [isLoading, setIsLoading] = useState(false) // Não começa loading

  useEffect(() => {
    // Verifica a validade do token periodicamente
    const interval = setInterval(() => {
      if (isAuthenticated && !is_authenticated()) {
        setToken(null)
        setIsAuthenticated(false)
        removeToken()
      }
    }, 30000) // 30 segundos

    return () => clearInterval(interval)
  }, [isAuthenticated])

  // Redirecionamento imediato para rotas protegidas
  useEffect(() => {
    const currentPath = window.location.pathname
    const isProtectedRoute = PROTECTED_ROUTES.includes(currentPath)

    if (!isAuthenticated && isProtectedRoute) {
      // Redirecionamento imediato
      window.location.href = '/admin'
    }
  }, [isAuthenticated])

  const login = async (email: string, password: string) => {
    setIsLoading(true)
    try {
      const res = await authLogin(email, password)
      if (!res.access_token) throw new Error('Token ausente')

      // Verifica se o token é válido antes de definir como autenticado
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

  // Verifica se está em rota protegida
  const currentPath = window.location.pathname
  const isProtectedRoute = PROTECTED_ROUTES.includes(currentPath)

  // Se não estiver autenticado em rota protegida, não renderiza nada (evita piscada)
  if (!isAuthenticated && isProtectedRoute) {
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
