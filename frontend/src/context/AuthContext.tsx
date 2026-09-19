import {
  createContext,
  type PropsWithChildren,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react'

import { api } from '../services/api'
import type { LoginResponse, User } from '../types/auth'

type AuthContextValue = {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, full_name: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: PropsWithChildren) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('darukaa_token')
    if (!token) {
      setLoading(false)
      return
    }

    api
      .get('/auth/me')
      .then((response) => setUser(response.data))
      .catch(() => localStorage.removeItem('darukaa_token'))
      .finally(() => setLoading(false))
  }, [])

  const login = async (email: string, password: string) => {
    const response = await api.post<LoginResponse>('/auth/login', { email, password })
    localStorage.setItem('darukaa_token', response.data.access_token)
    const profile = await api.get<User>('/auth/me')
    setUser(profile.data)
  }

  const register = async (email: string, password: string, full_name: string) => {
    await api.post('/auth/register', { email, password, full_name })
    await login(email, password)
  }

  const logout = () => {
    localStorage.removeItem('darukaa_token')
    setUser(null)
  }

  const value = useMemo<AuthContextValue>(
    () => ({ user, loading, login, register, logout }),
    [user, loading],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
