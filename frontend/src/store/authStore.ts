import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User } from '../types/api'
import { setTokens, clearTokens } from '../utils/auth'

interface AuthState {
  user: User | null
  token: string | null
  setAuth: (user: User, access: string, refresh: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      setAuth: (user, access, refresh) => {
        setTokens(access, refresh)
        set({ user, token: access })
      },
      logout: () => {
        clearTokens()
        set({ user: null, token: null })
      },
    }),
    { name: 'wb-auth', partialize: (s) => ({ user: s.user, token: s.token }) }
  )
)
