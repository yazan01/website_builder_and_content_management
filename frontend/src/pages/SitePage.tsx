import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Edit2, Trash2, Image, Globe, Home, ExternalLink, LayoutTemplate, Eye, Layout } from 'lucide-react'
import { sitesApi } from '../api/sites'
import { pagesApi } from '../api/pages'
import { AppShell } from '../components/layout/AppShell'
import { Button } from '../components/ui/Button'
import { Modal } from '../components/ui/Modal'
import { Input } from '../components/ui/Input'

function slugify(text: string) {
  return '/' + text.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-/]/g, '')
}

export default function SitePage() {
  const { siteId } = useParams<{ siteId: string }>()
  const id = Number(siteId)
  const [showCreate, setShowCreate] = useState(false)
  const [form, setForm] = useState({ title: '', slug: '/', is_homepage: false })
  const qc = useQueryClient()

  const { data: site } = useQuery({ queryKey: ['site', id], queryFn: () => sitesApi.get(id) })
  const { data: pages = [], isLoading } = useQuery({ queryKey: ['pages', id], queryFn: () => pagesApi.list(id) })

  const createMutation = useMutation({
    mutationFn: (data: typeof form) => pagesApi.create(id, data),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['pages', id] }); setShowCreate(false); setForm({ title: '', slug: '/', is_homepage: false }) },
  })

  const deleteMutation = useMutation({
    mutationFn: (pageId: number) => pagesApi.delete(id, pageId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['pages', id] }),
  })

  const publishMutation = useMutation({
    mutationFn: () => site?.is_published ? sitesApi.unpublish(id) : sitesApi.publish(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['site', id] }),
  })

  const updateTitle = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((f) => ({ ...f, title: e.target.value, slug: slugify(e.target.value) }))
  }

  return (
    <AppShell>
      <div className="p-8">
        {/* Header */}
        <div className="flex items-start justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">{site?.name}</h1>
            <p className="text-slate-500 text-sm mt-1 font-mono">/{site?.slug}</p>

            {/* Public URL — shown when published */}
            {site?.is_published && (
              <a
                href={`http://localhost:8000/s/sites/${site.slug}`}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1.5 mt-2 text-sm text-green-600 hover:text-green-700 font-medium bg-green-50 px-3 py-1.5 rounded-lg border border-green-200"
              >
                <Globe size={13} className="text-green-500" />
                localhost:8000/s/sites/{site.slug}
                <ExternalLink size={11} />
              </a>
            )}
          </div>
          <div className="flex items-center gap-3">
            <Link to={`/sites/${id}/layout`}>
              <Button variant="secondary" size="sm">
                <Layout size={14} className="mr-1.5" /> Layout
              </Button>
            </Link>
            <Link to={`/sites/${id}/media`}>
              <Button variant="secondary" size="sm">
                <Image size={14} className="mr-1.5" /> Media
              </Button>
            </Link>
            <Button
              variant={site?.is_published ? 'secondary' : 'primary'}
              size="sm"
              onClick={() => publishMutation.mutate()}
              loading={publishMutation.isPending}
            >
              <Globe size={14} className="mr-1.5" />
              {site?.is_published ? 'Unpublish' : 'Publish'}
            </Button>
          </div>
        </div>

        {/* Pages */}
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-slate-800">Pages</h2>
          <Button size="sm" onClick={() => setShowCreate(true)}>
            <Plus size={14} className="mr-1.5" /> New Page
          </Button>
        </div>

        {isLoading ? (
          <div className="space-y-2">
            {[1, 2, 3].map((i) => <div key={i} className="h-16 bg-slate-100 rounded-xl animate-pulse" />)}
          </div>
        ) : pages.length === 0 ? (
          <div className="text-center py-16 bg-white rounded-xl border border-slate-200">
            <p className="text-slate-400 mb-4">No pages yet</p>
            <Button size="sm" onClick={() => setShowCreate(true)}>
              <Plus size={14} className="mr-1.5" /> Create First Page
            </Button>
          </div>
        ) : (
          <div className="space-y-2">
            {pages.map((page) => (
              <div key={page.id} className="flex items-center gap-4 bg-white rounded-xl border border-slate-200 px-5 py-4 hover:shadow-sm transition-shadow">
                <div className="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center shrink-0">
                  {page.is_homepage ? <Home size={15} className="text-blue-600" /> : <ExternalLink size={15} className="text-slate-400" />}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-slate-900 text-sm">{page.title}</span>
                    {page.is_homepage && <span className="text-xs bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded font-medium">Home</span>}
                    {page.is_published && <span className="text-xs bg-green-100 text-green-700 px-1.5 py-0.5 rounded font-medium">Published</span>}
                  </div>
                  <span className="text-xs text-slate-400 font-mono">{page.slug}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Link to={`/sites/${id}/preview/${page.id}`}>
                    <Button size="sm" variant="ghost" title="معاينة">
                      <Eye size={13} />
                    </Button>
                  </Link>
                  <Link to={`/sites/${id}/templates/${page.id}`}>
                    <Button size="sm" variant="ghost" title="قوالب">
                      <LayoutTemplate size={13} />
                    </Button>
                  </Link>
                  <Link to={`/sites/${id}/builder/${page.id}`}>
                    <Button size="sm" variant="secondary">
                      <Edit2 size={13} className="mr-1.5" /> Edit
                    </Button>
                  </Link>
                  <button
                    onClick={() => { if (confirm(`Delete "${page.title}"?`)) deleteMutation.mutate(page.id) }}
                    className="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-lg"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <Modal open={showCreate} onClose={() => setShowCreate(false)} title="Create New Page">
        <form onSubmit={(e) => { e.preventDefault(); createMutation.mutate(form) }} className="space-y-4">
          <Input label="Page Title" value={form.title} onChange={updateTitle} placeholder="About Us" required />
          <Input label="Slug" value={form.slug} onChange={(e) => setForm((f) => ({ ...f, slug: e.target.value }))} placeholder="/about" required className="font-mono text-sm" />
          <label className="flex items-center gap-2 text-sm text-slate-700 cursor-pointer">
            <input type="checkbox" checked={form.is_homepage} onChange={(e) => setForm((f) => ({ ...f, is_homepage: e.target.checked }))} className="rounded" />
            Set as homepage
          </label>
          <div className="flex gap-3 pt-2">
            <Button type="button" variant="secondary" className="flex-1" onClick={() => setShowCreate(false)}>Cancel</Button>
            <Button type="submit" className="flex-1" loading={createMutation.isPending}>Create Page</Button>
          </div>
        </form>
      </Modal>
    </AppShell>
  )
}
