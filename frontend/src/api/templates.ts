import client from './client'
import type { Template } from '../types/api'

export interface TemplateSection {
  id: string
  template_id: number
  template_name: string
  template_slug: string
  template_category: string
  section_type: string
  icon: string
  label: string
  component: Record<string, unknown>
}

export const templatesApi = {
  list: (category?: string) =>
    client.get<Template[]>('/templates', { params: { category } }).then((r) => r.data),

  categories: () =>
    client.get<string[]>('/templates/categories').then((r) => r.data),

  get: (id: number) =>
    client.get<Template>(`/templates/${id}`).then((r) => r.data),

  apply: (pageId: number, templateId: number, themeVars?: Record<string, unknown>) =>
    client.post(`/templates/apply/${pageId}`, { template_id: templateId, theme_vars: themeVars }).then((r) => r.data),

  updateTheme: (siteId: number, themeVars: Record<string, string>, templateId?: number) =>
    client.put(`/templates/theme/${siteId}`, { theme_vars: themeVars, template_id: templateId }).then((r) => r.data),

  sections: (sectionType?: string, templateId?: number) =>
    client.get<TemplateSection[]>('/templates/sections', {
      params: { section_type: sectionType || undefined, template_id: templateId || undefined },
    }).then((r) => r.data),

  sectionTypes: () =>
    client.get<string[]>('/templates/section-types').then((r) => r.data),
}
