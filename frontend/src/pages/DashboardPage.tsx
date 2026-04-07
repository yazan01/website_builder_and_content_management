import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Globe, Trash2, ExternalLink, Settings } from 'lucide-react'
import { sitesApi } from '../api/sites'
import { AppShell } from '../components/layout/AppShell'
import { Button } from '../components/ui/Button'
import { Modal } from '../components/ui/Modal'
import { Input } from '../components/ui/Input'

function slugify(text: string) {
  return text.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')
}

export default function DashboardPage() {
  const [showCreate, setShowCreate] = useState(false)
  const [form, setForm] = useState({ name: '', slug: '', description: '' })
  const qc = useQueryClient()

  const { data: sites = [], isLoading } = useQuery({
    queryKey: ['sites'],
    queryFn: sitesApi.list,
  })

  const createMutation = useMutation({
    mutationFn: sitesApi.create,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['sites'] }); setShowCreate(false); setForm({ name: '', slug: '', description: '' }) },
  })

  const deleteMutation = useMutation({
    mutationFn: sitesApi.delete,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['sites'] }),
  })

  const update = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((f) => {
      const next = { ...f, [k]: e.target.value }
      if (k === 'name') next.slug = slugify(e.target.value)
      return next
    })
  }

  return (
    <AppShell>
      <div className="p-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">My Sites</h1>
            <p className="text-slate-500 text-sm mt-1">Manage your websites</p>
          </div>
          <Button onClick={() => setShowCreate(true)}>
            <Plus size={16} className="mr-1.5" /> New Site
          </Button>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-40 bg-slate-100 rounded-xl animate-pulse" />
            ))}
          </div>
        ) : sites.length === 0 ? (
          <div className="text-center py-20">
            <Globe size={48} className="mx-auto text-slate-300 mb-4" />
            <h3 className="text-lg font-medium text-slate-600 mb-2">No sites yet</h3>
            <p className="text-slate-400 text-sm mb-6">Create your first website to get started</p>
            <Button onClick={() => setShowCreate(true)}>
              <Plus size={16} className="mr-1.5" /> Create Site
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {sites.map((site) => (
              <div key={site.id} className="bg-white rounded-xl border border-slate-200 p-5 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between mb-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                    <Globe size={18} className="text-white" />
                  </div>
                  <div className="flex items-center gap-1">
                    {site.is_published && (
                      <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full font-medium">Live</span>
                    )}
                  </div>
                </div>
                <h3 className="font-semibold text-slate-900 mb-1">{site.name}</h3>
                <p className="text-xs text-slate-400 mb-4 font-mono">/{site.slug}</p>
                {site.description && <p className="text-sm text-slate-500 mb-4 line-clamp-2">{site.description}</p>}
                <div className="flex items-center gap-2 pt-3 border-t border-slate-100">
                  <Link to={`/sites/${site.id}`} className="flex-1">
                    <Button variant="secondary" size="sm" className="w-full">
                      <Settings size={13} className="mr-1.5" /> Manage
                    </Button>
                  </Link>
                  <button
                    onClick={() => { if (confirm('Delete this site?')) deleteMutation.mutate(site.id) }}
                    className="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <Modal open={showCreate} onClose={() => setShowCreate(false)} title="Create New Site">
        <form onSubmit={(e) => { e.preventDefault(); createMutation.mutate(form) }} className="space-y-4">
          <Input label="Site Name" value={form.name} onChange={update('name')} placeholder="My Awesome Site" required />
          <Input label="Slug" value={form.slug} onChange={update('slug')} placeholder="my-awesome-site" required
            className="font-mono text-sm" />
          <Input label="Description" value={form.description} onChange={update('description')} placeholder="Optional description" />
          <div className="flex gap-3 pt-2">
            <Button type="button" variant="secondary" className="flex-1" onClick={() => setShowCreate(false)}>Cancel</Button>
            <Button type="submit" className="flex-1" loading={createMutation.isPending}>Create Site</Button>
          </div>
        </form>
      </Modal>
    </AppShell>
  )
}
