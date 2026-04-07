import { useState, useRef } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Upload, Trash2, ArrowLeft, Image as ImageIcon, File } from 'lucide-react'
import { mediaApi } from '../api/media'
import { AppShell } from '../components/layout/AppShell'
import { Button } from '../components/ui/Button'

function formatBytes(bytes: number) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export default function MediaPage() {
  const { siteId } = useParams<{ siteId: string }>()
  const id = Number(siteId)
  const fileRef = useRef<HTMLInputElement>(null)
  const [uploading, setUploading] = useState(false)
  const qc = useQueryClient()

  const { data, isLoading } = useQuery({
    queryKey: ['media', id],
    queryFn: () => mediaApi.list(id),
  })

  const deleteMutation = useMutation({
    mutationFn: mediaApi.delete,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['media', id] }),
  })

  const handleUpload = async (files: FileList | null) => {
    if (!files) return
    setUploading(true)
    try {
      await Promise.all(Array.from(files).map((f) => mediaApi.upload(f, id)))
      qc.invalidateQueries({ queryKey: ['media', id] })
    } finally {
      setUploading(false)
    }
  }

  const items = data?.items ?? []

  return (
    <AppShell>
      <div className="p-8">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Link to={`/sites/${id}`} className="p-2 rounded-lg hover:bg-slate-100 text-slate-500">
              <ArrowLeft size={18} />
            </Link>
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Media Library</h1>
              <p className="text-slate-500 text-sm">{data?.total ?? 0} files</p>
            </div>
          </div>
          <div>
            <input ref={fileRef} type="file" multiple accept="image/*,video/*,application/pdf" className="hidden"
              onChange={(e) => handleUpload(e.target.files)} />
            <Button onClick={() => fileRef.current?.click()} loading={uploading}>
              <Upload size={15} className="mr-1.5" /> Upload Files
            </Button>
          </div>
        </div>

        {/* Drop zone */}
        <div
          className="border-2 border-dashed border-slate-200 rounded-xl p-8 text-center mb-6 cursor-pointer hover:border-blue-400 hover:bg-blue-50/50 transition-colors"
          onClick={() => fileRef.current?.click()}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => { e.preventDefault(); handleUpload(e.dataTransfer.files) }}
        >
          <Upload size={32} className="mx-auto text-slate-300 mb-2" />
          <p className="text-slate-500 text-sm">Drag & drop files here, or click to browse</p>
          <p className="text-slate-400 text-xs mt-1">Images, videos, PDFs up to 10MB</p>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {[1, 2, 3, 4, 5, 6].map((i) => <div key={i} className="aspect-square bg-slate-100 rounded-xl animate-pulse" />)}
          </div>
        ) : items.length === 0 ? (
          <div className="text-center py-12 text-slate-400">No files uploaded yet</div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {items.map((item) => (
              <div key={item.id} className="group relative bg-white rounded-xl border border-slate-200 overflow-hidden">
                {item.mime_type.startsWith('image/') ? (
                  <img src={item.url} alt={item.alt_text || item.filename} className="w-full aspect-square object-cover" />
                ) : (
                  <div className="w-full aspect-square flex items-center justify-center bg-slate-50">
                    <File size={32} className="text-slate-400" />
                  </div>
                )}
                <div className="p-2">
                  <p className="text-xs text-slate-600 truncate">{item.filename}</p>
                  <p className="text-xs text-slate-400">{formatBytes(item.file_size)}</p>
                </div>
                <button
                  onClick={() => { if (confirm('Delete this file?')) deleteMutation.mutate(item.id) }}
                  className="absolute top-2 right-2 p-1.5 bg-red-500 text-white rounded-lg opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <Trash2 size={12} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </AppShell>
  )
}
