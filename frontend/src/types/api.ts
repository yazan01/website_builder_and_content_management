export interface User {
  id: number
  email: string
  username: string
  is_active: boolean
  is_admin: boolean
}

export interface Site {
  id: number
  owner_id: number
  name: string
  slug: string
  description: string | null
  favicon_url: string | null
  custom_domain: string | null
  is_published: boolean
  published_at: string | null
  settings: Record<string, unknown> | null
  created_at: string
  updated_at: string | null
}

export interface Page {
  id: number
  site_id: number
  title: string
  slug: string
  is_homepage: boolean
  is_published: boolean
  meta_title: string | null
  meta_desc: string | null
  order_index: number
  created_at: string
  updated_at: string | null
}

export interface BuilderData {
  id: number
  grapes_data: Record<string, unknown>
  has_unpublished_changes: boolean
  updated_at: string | null
}

export interface Component {
  id: number
  owner_id: number
  site_id: number | null
  name: string
  category: string
  thumbnail_url: string | null
  block_data: Record<string, unknown>
  created_at: string
  updated_at: string | null
}

export interface MediaItem {
  id: number
  owner_id: number
  site_id: number | null
  filename: string
  url: string
  mime_type: string
  file_size: number
  width: number | null
  height: number | null
  alt_text: string | null
  created_at: string
}

export interface Revision {
  id: number
  page_id: number
  created_by: number | null
  created_at: string
}

export interface ThemeVars {
  primary_color: string
  secondary_color: string
  accent_color: string
  background_color: string
  text_color: string
  heading_font: string
  body_font: string
  border_radius: string
}

export interface Template {
  id: number
  name: string
  slug: string
  category: string
  description: string | null
  thumbnail_url: string | null
  preview_url: string | null
  theme_vars: ThemeVars
  is_featured: boolean
  created_at: string
  grapes_data?: Record<string, unknown>
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}
