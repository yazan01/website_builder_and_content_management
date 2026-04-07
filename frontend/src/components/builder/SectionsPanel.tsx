import { useState, useMemo, useCallback, memo } from 'react'
import { useQuery } from '@tanstack/react-query'
import type { Editor } from 'grapesjs'
import { Search, X, Plus, ChevronDown, GripVertical, ZoomIn } from 'lucide-react'
import { templatesApi } from '../../api/templates'
import type { TemplateSection } from '../../api/templates'
import { setPendingComponent } from '../../grapes/dragStore'
import { cn } from '../../utils/cn'

// ── Section HTML renderer (client-side, preview only) ──────────────────────

function compToHtml(comp: Record<string, unknown>): string {
  if (!comp) return ''
  if (comp.type === 'textnode') return String(comp.content ?? '')
  const tag = (comp.tagName as string) || 'div'
  const attrs = (comp.attributes as Record<string, string>) || {}
  const style = (comp.style as Record<string, string>) || {}
  const voidTags = ['img', 'input', 'br', 'hr', 'meta', 'link', 'source']
  const attrStr = Object.entries(attrs)
    .map(([k, v]) => `${k}="${String(v).replace(/"/g, '&quot;')}"`)
    .join(' ')
  const styleStr = Object.entries(style).map(([k, v]) => `${k}:${v}`).join(';')
  const extras = [attrStr, styleStr ? `style="${styleStr}"` : ''].filter(Boolean).join(' ')
  if (voidTags.includes(tag)) return `<${tag}${extras ? ' ' + extras : ''}>`
  const children = (comp.components as Record<string, unknown>[]) || []
  const inner = children.length
    ? children.map((c) => compToHtml(c as Record<string, unknown>)).join('')
    : String(comp.content ?? '')
  return `<${tag}${extras ? ' ' + extras : ''}>${inner}</${tag}>`
}

function sectionToHtml(comp: Record<string, unknown>): string {
  return `<!DOCTYPE html><html><head>
<meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet"/>
<style>*{box-sizing:border-box;margin:0;padding:0}body{font-family:'Inter',sans-serif;color:#1e293b;background:#fff}img{max-width:100%;height:auto}a{text-decoration:none;cursor:pointer}input,button,select{font-family:inherit}</style>
</head><body>${compToHtml(comp)}</body></html>`
}

// ── Mini preview iframe (scaled) ───────────────────────────────────────────

const PREVIEW_W = 232   // card content width (px)
const IFRAME_W  = 1100  // iframe logical width (px)
const SCALE     = PREVIEW_W / IFRAME_W
const IFRAME_H  = Math.round(160 / SCALE)  // iframe logical height

const MiniPreview = memo(({ comp }: { comp: Record<string, unknown> }) => {
  const html = useMemo(() => sectionToHtml(comp), [comp])
  return (
    <div
      className="overflow-hidden rounded-t-lg bg-slate-100"
      style={{ width: PREVIEW_W, height: 160 }}
    >
      <iframe
        title="preview"
        srcDoc={html}
        sandbox="allow-same-origin"
        style={{
          width: IFRAME_W,
          height: IFRAME_H,
          border: 'none',
          transformOrigin: 'top left',
          transform: `scale(${SCALE})`,
          pointerEvents: 'none',
          overflow: 'hidden',
        }}
      />
    </div>
  )
})

// ── Popup preview modal ────────────────────────────────────────────────────

function PreviewModal({
  section,
  onClose,
  onAdd,
}: {
  section: TemplateSection
  onClose: () => void
  onAdd: (s: TemplateSection) => void
}) {
  const html = useMemo(() => sectionToHtml(section.component), [section])

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-6 bg-black/70 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 rounded-2xl overflow-hidden shadow-2xl w-full max-w-4xl flex flex-col"
        style={{ maxHeight: '90vh' }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal header */}
        <div className="flex items-center justify-between px-5 py-3 border-b border-slate-700">
          <div>
            <span className="text-slate-200 font-semibold text-sm">{section.section_type}</span>
            <span className="mx-2 text-slate-600">·</span>
            <span className="text-slate-400 text-sm">{section.template_name}</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => { onAdd(section); onClose() }}
              className="flex items-center gap-1.5 px-4 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-semibold transition-colors"
            >
              <Plus size={14} /> Add to Page
            </button>
            <button
              onClick={onClose}
              className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-700 transition-colors"
            >
              <X size={16} />
            </button>
          </div>
        </div>

        {/* Large preview */}
        <div className="flex-1 overflow-auto bg-slate-800 p-4">
          <iframe
            title="section-preview"
            srcDoc={html}
            sandbox="allow-same-origin"
            className="w-full rounded-lg bg-white"
            style={{ height: 520, border: 'none' }}
          />
        </div>
      </div>
    </div>
  )
}

// ── Section card ───────────────────────────────────────────────────────────

function SectionCard({
  section,
  onAdd,
  onPreview,
  justAdded,
}: {
  section: TemplateSection
  onAdd: (s: TemplateSection) => void
  onPreview: (s: TemplateSection) => void
  justAdded: boolean
}) {
  const handleDragStart = (e: React.DragEvent) => {
    setPendingComponent(section.component)
    e.dataTransfer.effectAllowed = 'copy'
    // Ghost image
    const ghost = document.createElement('div')
    ghost.textContent = `${section.icon} ${section.section_type}`
    ghost.style.cssText =
      'position:fixed;top:-200px;left:0;background:#1e40af;color:#fff;padding:6px 14px;border-radius:8px;font-size:13px;font-weight:600;pointer-events:none'
    document.body.appendChild(ghost)
    e.dataTransfer.setDragImage(ghost, 60, 20)
    setTimeout(() => document.body.removeChild(ghost), 0)
  }

  const handleDragEnd = () => setPendingComponent(null)

  return (
    <div
      draggable
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
      className="group mx-2 my-1.5 rounded-xl border border-slate-700 hover:border-blue-500 bg-slate-800 hover:bg-slate-750 overflow-hidden transition-all cursor-grab active:cursor-grabbing shadow-sm hover:shadow-md"
    >
      {/* Mini preview */}
      <div className="relative">
        <MiniPreview comp={section.component} />

        {/* Hover overlay */}
        <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-all flex items-center justify-center gap-2 opacity-0 group-hover:opacity-100">
          <button
            onClick={() => onPreview(section)}
            className="flex items-center gap-1 px-3 py-1.5 bg-white/90 hover:bg-white text-slate-900 rounded-lg text-xs font-semibold shadow transition-colors"
          >
            <ZoomIn size={12} /> Preview
          </button>
          <button
            onClick={() => onAdd(section)}
            className={cn(
              'flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-semibold shadow transition-colors',
              justAdded
                ? 'bg-green-500 text-white'
                : 'bg-blue-600 hover:bg-blue-500 text-white'
            )}
          >
            <Plus size={12} />
            {justAdded ? 'Added ✓' : 'Add'}
          </button>
        </div>

        {/* Drag handle hint */}
        <div className="absolute top-2 right-2 bg-black/40 text-white/70 rounded p-0.5 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
          <GripVertical size={12} />
        </div>
      </div>

      {/* Footer label */}
      <div className="px-2.5 py-2 flex items-center gap-2">
        <span className="text-base leading-none">{section.icon}</span>
        <div className="flex-1 min-w-0">
          <div className="text-slate-200 text-[11px] font-semibold truncate">{section.section_type}</div>
          <div className="text-slate-500 text-[10px] truncate">{section.template_name}</div>
        </div>
      </div>
    </div>
  )
}

// ── Main panel ─────────────────────────────────────────────────────────────

interface Props {
  editor: Editor | null
}

export function SectionsPanel({ editor }: Props) {
  const [search, setSearch] = useState('')
  const [activeType, setActiveType] = useState('All')
  const [activeTemplate, setActiveTemplate] = useState('All')
  const [showFilters, setShowFilters] = useState(false)
  const [added, setAdded] = useState<string | null>(null)
  const [previewing, setPreviewing] = useState<TemplateSection | null>(null)

  const { data: sections = [], isLoading } = useQuery({
    queryKey: ['template-sections'],
    queryFn: () => templatesApi.sections(),
    staleTime: Infinity,
  })

  const { data: sectionTypes = [] } = useQuery({
    queryKey: ['section-types'],
    queryFn: () => templatesApi.sectionTypes(),
    staleTime: Infinity,
  })

  const templateNames = useMemo(
    () => [...new Set(sections.map((s) => s.template_name))].sort(),
    [sections]
  )

  const filtered = useMemo(() => {
    return sections.filter((s) => {
      const q = search.toLowerCase()
      const matchSearch = !q || s.section_type.toLowerCase().includes(q) || s.template_name.toLowerCase().includes(q)
      const matchType = activeType === 'All' || s.section_type === activeType
      const matchTpl = activeTemplate === 'All' || s.template_name === activeTemplate
      return matchSearch && matchType && matchTpl
    })
  }, [sections, search, activeType, activeTemplate])

  const addSection = useCallback((section: TemplateSection) => {
    if (!editor) return
    editor.addComponents(section.component)
    setAdded(section.id)
    setTimeout(() => setAdded(null), 1800)
  }, [editor])

  return (
    <>
      <div className="flex flex-col h-full text-xs">
        {/* Search */}
        <div className="p-2 border-b border-slate-700">
          <div className="flex items-center gap-1.5 bg-slate-700/80 rounded-lg px-2.5 py-1.5">
            <Search size={11} className="text-slate-400 shrink-0" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search sections..."
              className="bg-transparent text-slate-200 placeholder-slate-500 text-[11px] outline-none w-full"
            />
            {search && (
              <button onClick={() => setSearch('')} className="text-slate-500 hover:text-slate-300">
                <X size={10} />
              </button>
            )}
          </div>
        </div>

        {/* Filters toggle */}
        <div className="px-2.5 py-1.5 border-b border-slate-700">
          <button
            onClick={() => setShowFilters((v) => !v)}
            className="flex items-center gap-1 text-slate-400 hover:text-slate-200 text-[11px] font-medium w-full"
          >
            <ChevronDown size={11} className={cn('transition-transform', showFilters && 'rotate-180')} />
            <span>Filters</span>
            {(activeType !== 'All' || activeTemplate !== 'All') && (
              <span className="ml-auto bg-blue-600 text-white rounded-full px-1.5 text-[9px] leading-4">
                {[activeType !== 'All', activeTemplate !== 'All'].filter(Boolean).length}
              </span>
            )}
          </button>

          {showFilters && (
            <div className="mt-2 space-y-2 pb-1">
              {/* Type chips */}
              <div className="flex flex-wrap gap-1">
                {['All', ...sectionTypes].map((t) => (
                  <button
                    key={t}
                    onClick={() => setActiveType(t)}
                    className={cn(
                      'px-2 py-0.5 rounded-full text-[10px] font-medium transition-colors',
                      activeType === t ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-400 hover:text-white'
                    )}
                  >
                    {t}
                  </button>
                ))}
              </div>

              {/* Template select */}
              <select
                value={activeTemplate}
                onChange={(e) => setActiveTemplate(e.target.value)}
                className="w-full bg-slate-700 text-slate-200 text-[11px] rounded px-2 py-1 outline-none"
              >
                <option value="All">All Templates</option>
                {templateNames.map((n) => (
                  <option key={n} value={n}>{n}</option>
                ))}
              </select>

              {(activeType !== 'All' || activeTemplate !== 'All') && (
                <button
                  onClick={() => { setActiveType('All'); setActiveTemplate('All') }}
                  className="text-[10px] text-blue-400 hover:text-blue-300"
                >
                  Clear filters
                </button>
              )}
            </div>
          )}
        </div>

        {/* Count + drag hint */}
        <div className="px-3 py-1 border-b border-slate-700 flex items-center justify-between">
          <span className="text-[10px] text-slate-500">
            {isLoading ? 'Loading...' : `${filtered.length} sections`}
          </span>
          <span className="text-[9px] text-slate-600 italic">drag into canvas</span>
        </div>

        {/* List */}
        <div className="flex-1 overflow-auto py-1">
          {isLoading ? (
            <div className="space-y-2 p-2">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-44 bg-slate-700 rounded-xl animate-pulse" />
              ))}
            </div>
          ) : filtered.length === 0 ? (
            <div className="text-center text-slate-500 py-10 text-xs">No sections found</div>
          ) : (
            filtered.map((section) => (
              <SectionCard
                key={section.id}
                section={section}
                onAdd={addSection}
                onPreview={setPreviewing}
                justAdded={added === section.id}
              />
            ))
          )}
        </div>
      </div>

      {/* Preview modal */}
      {previewing && (
        <PreviewModal
          section={previewing}
          onClose={() => setPreviewing(null)}
          onAdd={addSection}
        />
      )}
    </>
  )
}
