import client from './client'
import type { Page, BuilderData, Revision } from '../types/api'

export const pagesApi = {
  list: (siteId: number) => client.get<Page[]>(`/sites/${siteId}/pages`).then((r) => r.data),

  create: (siteId: number, data: { title: string; slug: string; is_homepage?: boolean }) =>
    client.post<Page>(`/sites/${siteId}/pages`, data).then((r) => r.data),

  get: (siteId: number, pageId: number) =>
    client.get<Page>(`/sites/${siteId}/pages/${pageId}`).then((r) => r.data),

  update: (siteId: number, pageId: number, data: Partial<Page>) =>
    client.put<Page>(`/sites/${siteId}/pages/${pageId}`, data).then((r) => r.data),

  delete: (siteId: number, pageId: number) =>
    client.delete(`/sites/${siteId}/pages/${pageId}`),

  // Builder save/load
  loadBuilder: (pageId: number) =>
    client.get<BuilderData>(`/builder/pages/${pageId}`).then((r) => r.data),

  saveBuilder: (pageId: number, grapesData: Record<string, unknown>) =>
    client.put<BuilderData>(`/builder/pages/${pageId}`, { grapes_data: grapesData }).then((r) => r.data),

  publishDraft: (pageId: number) =>
    client.post<BuilderData>(`/builder/pages/${pageId}/publish-draft`).then((r) => r.data),

  listRevisions: (pageId: number) =>
    client.get<Revision[]>(`/builder/pages/${pageId}/revisions`).then((r) => r.data),

  restoreRevision: (pageId: number, revisionId: number) =>
    client.post<BuilderData>(`/builder/pages/${pageId}/revisions/${revisionId}/restore`).then((r) => r.data),
}
