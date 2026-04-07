import { useState, useRef, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import grapesjs from 'grapesjs'
import type { Editor } from 'grapesjs'
import 'grapesjs/dist/css/grapes.min.css'
import { ArrowLeft, Save, CheckCircle } from 'lucide-react'
import { sitesApi } from '../api/sites'
import client from '../api/client'
import { registerBlocks } from '../grapes/blocks'
import { cn } from '../utils/cn'

type Section = 'header' | 'footer'

async function loadLayout(siteId: number) {
  return client.get(`/sites/${siteId}/layout`).then(r => r.data)
}
async function saveLayout(siteId: number, data: Record<string, unknown>) {
  return client.put(`/sites/${siteId}/layout`, data).then(r => r.data)
}

export default function LayoutEditorPage() {
  const { siteId } = useParams<{ siteId: string }>()
  const id = Number(siteId)
  const [activeSection, setActiveSection] = useState<Section>('header')
  const [saved, setSaved] = useState(false)
  const editorRef = useRef<Editor | null>(null)
  const layoutRef = useRef<Record<string, unknown>>({})
  const qc = useQueryClient()

  const { data: site } = useQuery({ queryKey: ['site', id], queryFn: () => sitesApi.get(id) })

  const saveMutation = useMutation({
    mutationFn: (data: Record<string, unknown>) => saveLayout(id, data),
    onSuccess: () => {
      setSaved(true)
      qc.invalidateQueries({ queryKey: ['site', id] })
      setTimeout(() => setSaved(false), 2000)
    },
  })

  const initEditor = async (section: Section) => {
    // Destroy existing editor
    if (editorRef.current) {
      editorRef.current.destroy()
      editorRef.current = null
    }

    const layout = await loadLayout(id)
    layoutRef.current = layout

    const existingComp = layout[section]

    const editor = grapesjs.init({
      container: '#layout-editor-canvas',
      fromElement: false,
      height: '100%',
      width: 'auto',
      storageManager: false,
      blockManager: { appendTo: '#layout-blocks' },
      styleManager: { appendTo: '#layout-styles' },
      layerManager: { appendTo: '#layout-layers' },
      panels: { defaults: [] },
      canvas: {
        styles: ['https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap'],
      },
    })

    registerBlocks(editor)

    // Load existing component if exists
    if (existingComp && typeof existingComp === 'object') {
      const comp = existingComp as Record<string, unknown>
      const components = comp.components as unknown[] || []
      if (components.length > 0) {
        editor.setComponents(components)
      }
    }

    editorRef.current = editor
  }

  useEffect(() => {
    initEditor(activeSection)
    return () => {
      editorRef.current?.destroy()
      editorRef.current = null
    }
  }, [id, activeSection])

  const handleSave = () => {
    if (!editorRef.current) return
    const projectData = editorRef.current.getProjectData()
    const pages = projectData.pages || []
    const frames = pages[0]?.frames || []
    const component = frames[0]?.component || {}

    const updated = {
      ...layoutRef.current,
      [activeSection]: component,
      styles: projectData.styles || layoutRef.current.styles || [],
    }

    saveMutation.mutate(updated)
  }

  return (
    <div className="flex flex-col h-screen bg-slate-900">
      {/* Top bar */}
      <div className="flex items-center gap-3 px-4 py-2.5 bg-slate-800 border-b border-slate-700 h-12 shrink-0">
        <Link to={`/sites/${siteId}`} className="flex items-center gap-1.5 text-slate-400 hover:text-white text-sm">
          <ArrowLeft size={15} /> Back
        </Link>

        <div className="w-px h-5 bg-slate-600" />
        <span className="text-slate-300 text-sm font-semibold">Global Layout — {site?.name}</span>

        <div className="flex-1" />

        {/* Section tabs */}
        <div className="flex bg-slate-700 rounded-lg p-1 gap-1">
          {(['header', 'footer'] as Section[]).map((s) => (
            <button
              key={s}
              onClick={() => setActiveSection(s)}
              className={cn(
                'px-4 py-1.5 rounded-md text-sm font-medium capitalize transition-colors',
                activeSection === s
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-400 hover:text-white'
              )}
            >
              {s === 'header' ? '🔝 Header' : '🔻 Footer'}
            </button>
          ))}
        </div>

        <div className="w-px h-5 bg-slate-600" />

        <button
          onClick={handleSave}
          disabled={saveMutation.isPending}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
        >
          {saved ? <CheckCircle size={14} /> : <Save size={14} />}
          {saved ? 'Saved!' : saveMutation.isPending ? 'Saving...' : 'Save Layout'}
        </button>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Left panel */}
        <div className="w-60 bg-slate-800 border-r border-slate-700 flex flex-col">
          <div className="p-3 border-b border-slate-700 text-xs text-slate-400 font-semibold uppercase tracking-wider">
            Blocks
          </div>
          <div id="layout-blocks" className="flex-1 overflow-auto" />
        </div>

        {/* Canvas */}
        <div className="flex-1 overflow-hidden bg-slate-600">
          <div id="layout-editor-canvas" className="w-full h-full" />
        </div>

        {/* Right panel */}
        <div className="w-60 bg-slate-800 border-l border-slate-700 flex flex-col">
          <div className="p-3 border-b border-slate-700 text-xs text-slate-400 font-semibold uppercase tracking-wider">
            Styles
          </div>
          <div id="layout-styles" className="flex-1 overflow-auto" />
          <div className="border-t border-slate-700 p-3">
            <div className="text-xs text-slate-400 font-semibold uppercase tracking-wider mb-2">Layers</div>
            <div id="layout-layers" />
          </div>
        </div>
      </div>
    </div>
  )
}
