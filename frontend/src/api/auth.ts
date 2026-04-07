import client from './client'
import type { User, TokenResponse } from '../types/api'

export const authApi = {
  register: (data: { email: string; username: string; password: string }) =>
    client.post<User>('/auth/register', data).then((r) => r.data),

  login: (data: { email: string; password: string }) =>
    client.post<TokenResponse>('/auth/login', data).then((r) => r.data),

  me: () => client.get<User>('/auth/me').then((r) => r.data),
}
