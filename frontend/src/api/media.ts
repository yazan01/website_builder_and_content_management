import client from './client'
import type { MediaItem } from '../types/api'

interface MediaListResponse {
  items: MediaItem[]
  total: number
}

export const mediaApi = {
  list: (siteId?: number) =>
    client.get<MediaListResponse>('/media', { params: { site_id: siteId } }).then((r) => r.data),

  upload: (file: File, siteId?: number) => {
    const form = new FormData()
    form.append('file', file)
    if (siteId) form.append('site_id', String(siteId))
    return client.post<MediaItem>('/media/upload', form).then((r) => r.data)
  },

  update: (id: number, data: { alt_text?: string; filename?: string }) =>
    client.put<MediaItem>(`/media/${id}`, data).then((r) => r.data),

  delete: (id: number) => client.delete(`/media/${id}`),
}
