import client from './client'
import type { Site } from '../types/api'

export const sitesApi = {
  list: () => client.get<Site[]>('/sites').then((r) => r.data),

  create: (data: { name: string; slug: string; description?: string }) =>
    client.post<Site>('/sites', data).then((r) => r.data),

  get: (id: number) => client.get<Site>(`/sites/${id}`).then((r) => r.data),

  update: (id: number, data: Partial<Site>) =>
    client.put<Site>(`/sites/${id}`, data).then((r) => r.data),

  delete: (id: number) => client.delete(`/sites/${id}`),

  publish: (id: number) => client.post<Site>(`/sites/${id}/publish`).then((r) => r.data),

  unpublish: (id: number) => client.post<Site>(`/sites/${id}/unpublish`).then((r) => r.data),
}
