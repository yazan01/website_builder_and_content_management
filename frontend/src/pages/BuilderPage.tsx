import { useState, useRef, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import type { Editor } from 'grapesjs'
import { Layers, Palette, Layout, Settings, Puzzle } from 'lucide-react'
import { pagesApi } from '../api/pages'
import { GrapesEditor } from '../components/builder/GrapesEditor'
import { BuilderToolbar } from '../components/builder/BuilderToolbar'
import { SectionsPanel } from '../components/builder/SectionsPanel'
import { useBuilderStore } from '../store/builderStore'
import { cn } from '../utils/cn'

type PanelTab = 'blocks' | 'sections' | 'layers' | 'styles' | 'traits'

export default function BuilderPage() {
  const { siteId, pageId } = useParams<{ siteId: string; pageId: string }>()
  const [activeTab, setActiveTab] = useState<PanelTab>('blocks')
  const editorRef = useRef<Editor | null>(null)
  const [editorReady, setEditorReady] = useState(false)
  const { setHasUnpublishedChanges } = useBuilderStore()

  const { data: page } = useQuery({
    queryKey: ['page', Number(siteId), Number(pageId)],
    queryFn: () => pagesApi.get(Number(siteId), Number(pageId)),
  })

  // Seed initial unpublished-changes state from server
  const { data: builderData } = useQuery({
    queryKey: ['builder', Number(pageId)],
    queryFn: () => pagesApi.loadBuilder(Number(pageId)),
  })
  useEffect(() => {
    if (builderData) setHasUnpublishedChanges(builderData.has_unpublished_changes ?? false)
  }, [builderData])

  const tabs: { id: PanelTab; icon: React.ReactNode; label: string }[] = [
    { id: 'blocks',   icon: <Layout size={15} />,  label: 'Blocks' },
    { id: 'sections', icon: <Puzzle size={15} />,  label: 'Sections' },
    { id: 'layers',   icon: <Layers size={15} />,  label: 'Layers' },
    { id: 'styles',   icon: <Palette size={15} />, label: 'Styles' },
    { id: 'traits',   icon: <Settings size={15} />, label: 'Settings' },
  ]

  return (
    <div className="flex flex-col h-screen bg-slate-900 overflow-hidden">
      {/* Toolbar */}
      <BuilderToolbar
        editor={editorRef.current}
        siteId={Number(siteId)}
        pageId={Number(pageId)}
        pageTitle={page?.title ?? 'Loading...'}
      />

      <div className="flex flex-1 overflow-hidden">
        {/* Left Panel */}
        <div className="w-64 bg-slate-800 border-r border-slate-700 flex flex-col shrink-0">
          {/* Tab switcher */}
          <div className="flex border-b border-slate-700">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                title={tab.label}
                className={cn(
                  'flex-1 flex flex-col items-center gap-0.5 py-2 text-xs transition-colors',
                  activeTab === tab.id
                    ? 'text-blue-400 border-b-2 border-blue-400 -mb-px'
                    : 'text-slate-400 hover:text-slate-200'
                )}
              >
                {tab.icon}
                <span className="text-[9px]">{tab.label}</span>
              </button>
            ))}
          </div>

          {/* Panel content */}
          <div className="flex-1 overflow-hidden flex flex-col">
            <div id="blocks-panel" className={cn('flex-1 overflow-auto', activeTab !== 'blocks' && 'hidden')} />
            <div id="layers-panel" className={cn('flex-1 overflow-auto', activeTab !== 'layers' && 'hidden')} />
            <div id="styles-panel" className={cn('flex-1 overflow-auto', activeTab !== 'styles' && 'hidden')} />
            <div id="traits-panel" className={cn('flex-1 overflow-auto', activeTab !== 'traits' && 'hidden')} />
            <div className={cn('flex-1 overflow-hidden flex flex-col', activeTab !== 'sections' && 'hidden')}>
              <SectionsPanel editor={editorReady ? editorRef.current : null} />
            </div>
          </div>
        </div>

        {/* Canvas */}
        <div className="flex-1 overflow-hidden">
          {pageId && (
            <GrapesEditor
              pageId={Number(pageId)}
              onReady={(editor) => {
                editorRef.current = editor
                setEditorReady(true)
              }}
            />
          )}
        </div>
      </div>
    </div>
  )
}
