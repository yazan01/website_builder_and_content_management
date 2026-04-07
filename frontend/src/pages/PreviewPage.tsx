import { useRef, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { ArrowLeft, Edit2, Smartphone, Tablet, Monitor } from 'lucide-react'
import { pagesApi } from '../api/pages'
import { sitesApi } from '../api/sites'
import client from '../api/client'
import { cn } from '../utils/cn'

type DeviceMode = 'desktop' | 'tablet' | 'mobile'

const DEVICE_WIDTHS: Record<DeviceMode, string> = {
  desktop: '100%',
  tablet: '768px',
  mobile: '390px',
}

async function fetchPreviewHtml(pageId: number): Promise<string> {
  const res = await client.get(`/builder/pages/${pageId}/preview`, {
    responseType: 'text',
    headers: { Accept: 'text/html' },
  })
  return res.data as string
}

export default function PreviewPage() {
  const { siteId, pageId } = useParams<{ siteId: string; pageId: string }>()
  const iframeRef = useRef<HTMLIFrameElement>(null)
  const [device, setDevice] = useState<DeviceMode>('desktop')

  const { data: page } = useQuery({
    queryKey: ['page', Number(siteId), Number(pageId)],
    queryFn: () => pagesApi.get(Number(siteId), Number(pageId)),
  })

  const { data: site } = useQuery({
    queryKey: ['site', Number(siteId)],
    queryFn: () => sitesApi.get(Number(siteId)),
  })

  const { data: html = '' } = useQuery({
    queryKey: ['preview-html', Number(pageId)],
    queryFn: () => fetchPreviewHtml(Number(pageId)),
    staleTime: 0,
  })


  return (
    <div className="flex flex-col h-screen bg-slate-900 overflow-hidden">
      {/* Toolbar */}
      <div className="flex items-center gap-3 px-4 py-2.5 bg-slate-800 border-b border-slate-700 h-12 shrink-0">
        <Link to={`/sites/${siteId}`} className="flex items-center gap-1.5 text-slate-400 hover:text-white text-sm">
          <ArrowLeft size={15} /> Back
        </Link>

        <div className="w-px h-5 bg-slate-600" />

        <span className="text-slate-300 text-sm font-medium">{page?.title}</span>
        <span className="text-slate-500 text-xs font-mono">{page?.slug}</span>

        {site?.name && (
          <span className="text-slate-600 text-xs">— {site.name}</span>
        )}

        <div className="flex-1" />

        {/* Device switcher */}
        <div className="flex items-center gap-1 bg-slate-700 rounded-lg p-1">
          {([['desktop', Monitor], ['tablet', Tablet], ['mobile', Smartphone]] as const).map(([mode, Icon]) => (
            <button
              key={mode}
              onClick={() => setDevice(mode)}
              title={mode}
              className={cn(
                'p-1.5 rounded transition-colors',
                device === mode ? 'bg-slate-500 text-white' : 'text-slate-400 hover:text-white'
              )}
            >
              <Icon size={14} />
            </button>
          ))}
        </div>

        <div className="w-px h-5 bg-slate-600" />

        <Link
          to={`/sites/${siteId}/builder/${pageId}`}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors"
        >
          <Edit2 size={13} /> Edit
        </Link>
      </div>

      {/* Preview canvas */}
      <div className="flex-1 overflow-auto bg-slate-700 flex items-start justify-center py-6">
        <div
          className="bg-white shadow-2xl rounded-lg overflow-hidden transition-all duration-300"
          style={{ width: DEVICE_WIDTHS[device], minHeight: '100%' }}
        >
          <iframe
            ref={iframeRef}
            srcDoc={html || undefined}
            title="preview"
            className="w-full border-0"
            style={{ minHeight: 'calc(100vh - 80px)', display: 'block' }}
            sandbox="allow-same-origin allow-scripts allow-forms"
          />
        </div>
      </div>
    </div>
  )
}
