import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation } from '@tanstack/react-query'
import { CheckCircle, ArrowLeft, Wand2, Palette } from 'lucide-react'
import { templatesApi } from '../api/templates'
import { pagesApi } from '../api/pages'
import type { Template, ThemeVars } from '../types/api'
import { Button } from '../components/ui/Button'
import { cn } from '../utils/cn'

// ─── Theme Customizer Panel ─────────────────────────────────────────────────

const FONTS = ['Inter', 'Georgia', 'Roboto', 'Playfair Display', 'Montserrat', 'Lato', 'Poppins']

const PRESETS: { name: string; vars: Partial<ThemeVars> }[] = [
  { name: 'Ocean Blue',    vars: { primary_color: '#2563eb', secondary_color: '#1e40af', accent_color: '#f59e0b' } },
  { name: 'Royal Purple',  vars: { primary_color: '#7c3aed', secondary_color: '#5b21b6', accent_color: '#ec4899' } },
  { name: 'Emerald',       vars: { primary_color: '#059669', secondary_color: '#047857', accent_color: '#f59e0b' } },
  { name: 'Crimson',       vars: { primary_color: '#dc2626', secondary_color: '#991b1b', accent_color: '#f97316' } },
  { name: 'Slate Dark',    vars: { primary_color: '#334155', secondary_color: '#1e293b', accent_color: '#06b6d4' } },
  { name: 'Rose Gold',     vars: { primary_color: '#be185d', secondary_color: '#9d174d', accent_color: '#f59e0b' } },
]

interface ThemeCustomizerProps {
  baseVars: ThemeVars
  onChange: (vars: ThemeVars) => void
}

function ThemeCustomizer({ baseVars, onChange }: ThemeCustomizerProps) {
  const update = (key: keyof ThemeVars, val: string) =>
    onChange({ ...baseVars, [key]: val })

  return (
    <div className="space-y-5">
      {/* Color Presets */}
      <div>
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Color Presets</p>
        <div className="grid grid-cols-3 gap-2">
          {PRESETS.map((p) => (
            <button
              key={p.name}
              onClick={() => onChange({ ...baseVars, ...p.vars })}
              className="flex flex-col items-center gap-1.5 p-2 rounded-lg border border-slate-700 hover:border-blue-500 transition-colors"
            >
              <div className="flex gap-1">
                <div className="w-4 h-4 rounded-full" style={{ background: p.vars.primary_color }} />
                <div className="w-4 h-4 rounded-full" style={{ background: p.vars.secondary_color }} />
                <div className="w-4 h-4 rounded-full" style={{ background: p.vars.accent_color }} />
              </div>
              <span className="text-[10px] text-slate-400">{p.name}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Custom Colors */}
      <div>
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Custom Colors</p>
        <div className="space-y-2">
          {([
            ['primary_color', 'Primary'],
            ['secondary_color', 'Secondary'],
            ['accent_color', 'Accent'],
            ['background_color', 'Background'],
            ['text_color', 'Text'],
          ] as [keyof ThemeVars, string][]).map(([key, label]) => (
            <div key={key} className="flex items-center justify-between">
              <span className="text-xs text-slate-300">{label}</span>
              <div className="flex items-center gap-2">
                <input
                  type="color"
                  value={baseVars[key]}
                  onChange={(e) => update(key, e.target.value)}
                  className="w-8 h-8 rounded cursor-pointer border-0 bg-transparent"
                />
                <input
                  type="text"
                  value={baseVars[key]}
                  onChange={(e) => update(key, e.target.value)}
                  className="w-20 text-xs bg-slate-700 text-slate-200 px-2 py-1 rounded font-mono border border-slate-600"
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Fonts */}
      <div>
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Fonts</p>
        <div className="space-y-2">
          {([['heading_font', 'Heading Font'], ['body_font', 'Body Font']] as [keyof ThemeVars, string][]).map(([key, label]) => (
            <div key={key}>
              <label className="text-xs text-slate-400 mb-1 block">{label}</label>
              <select
                value={baseVars[key]}
                onChange={(e) => update(key, e.target.value)}
                className="w-full bg-slate-700 text-slate-200 text-xs px-2 py-1.5 rounded border border-slate-600"
              >
                {FONTS.map((f) => <option key={f} value={f}>{f}</option>)}
              </select>
            </div>
          ))}
        </div>
      </div>

      {/* Border Radius */}
      <div>
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Border Radius</p>
        <div className="flex gap-2">
          {['0px', '4px', '8px', '12px', '20px', '50px'].map((r) => (
            <button
              key={r}
              onClick={() => update('border_radius', r)}
              className={cn(
                'flex-1 py-1.5 text-xs rounded border transition-colors',
                baseVars.border_radius === r
                  ? 'border-blue-500 bg-blue-500/20 text-blue-300'
                  : 'border-slate-600 text-slate-400 hover:border-slate-400'
              )}
            >
              {r === '0px' ? 'None' : r === '50px' ? 'Full' : r}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

// ─── Template Card ───────────────────────────────────────────────────────────

function TemplateCard({ template, selected, onSelect }: {
  template: Template
  selected: boolean
  onSelect: () => void
}) {
  const colors = template.theme_vars

  return (
    <button
      onClick={onSelect}
      className={cn(
        'relative w-full text-left rounded-xl border-2 overflow-hidden transition-all hover:scale-[1.01]',
        selected ? 'border-blue-500 ring-2 ring-blue-500/30' : 'border-slate-200 hover:border-slate-300'
      )}
    >
      {/* Thumbnail / Preview */}
      <div
        className="h-40 relative overflow-hidden"
        style={{ background: `linear-gradient(135deg, ${colors.primary_color}22, ${colors.secondary_color}33)` }}
      >
        {/* Mini layout preview */}
        <div className="absolute inset-0 p-3 flex flex-col gap-1.5">
          {/* Navbar */}
          <div className="flex items-center justify-between px-2 py-1.5 rounded-md" style={{ background: colors.primary_color }}>
            <div className="w-10 h-1.5 rounded-full bg-white/70" />
            <div className="flex gap-1">
              {[1, 2, 3].map((i) => <div key={i} className="w-5 h-1 rounded-full bg-white/50" />)}
            </div>
          </div>
          {/* Hero */}
          <div className="flex-1 rounded-md flex flex-col items-center justify-center gap-1" style={{ background: `${colors.primary_color}15` }}>
            <div className="w-24 h-2 rounded-full" style={{ background: colors.primary_color + 'aa' }} />
            <div className="w-16 h-1.5 rounded-full bg-slate-300/50" />
            <div className="w-10 h-4 rounded-md mt-1" style={{ background: colors.accent_color }} />
          </div>
          {/* Cards row */}
          <div className="flex gap-1.5">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex-1 rounded h-8" style={{ background: colors.primary_color + '15', border: `1px solid ${colors.primary_color}30` }} />
            ))}
          </div>
        </div>

        {/* Featured badge */}
        {template.is_featured && (
          <div className="absolute top-2 right-2 bg-amber-400 text-amber-900 text-[10px] font-bold px-2 py-0.5 rounded-full">
            Featured
          </div>
        )}

        {/* Selected check */}
        {selected && (
          <div className="absolute inset-0 bg-blue-500/10 flex items-center justify-center">
            <CheckCircle size={32} className="text-blue-500" />
          </div>
        )}
      </div>

      <div className="p-3 bg-white">
        <div className="flex items-center justify-between mb-0.5">
          <h3 className="font-semibold text-slate-900 text-sm">{template.name}</h3>
          <span className="text-[10px] bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full capitalize">{template.category}</span>
        </div>
        <p className="text-xs text-slate-500 line-clamp-2">{template.description}</p>
      </div>
    </button>
  )
}

// ─── Main Page ───────────────────────────────────────────────────────────────

export default function TemplatesPage() {
  const { siteId, pageId } = useParams<{ siteId: string; pageId: string }>()
  const navigate = useNavigate()
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [activeCategory, setActiveCategory] = useState<string>('all')
  const [themeVars, setThemeVars] = useState<ThemeVars | null>(null)
  const [showTheme, setShowTheme] = useState(false)

  const { data: templates = [] } = useQuery({
    queryKey: ['templates'],
    queryFn: () => templatesApi.list(),
  })

  const { data: categories = [] } = useQuery({
    queryKey: ['template-categories'],
    queryFn: templatesApi.categories,
  })

  const selectedTemplate = templates.find((t) => t.id === selectedId)

  // When template is selected, init its theme vars
  const handleSelect = (t: Template) => {
    setSelectedId(t.id)
    setThemeVars(t.theme_vars)
  }

  const applyMutation = useMutation({
    mutationFn: () =>
      templatesApi.apply(Number(pageId), selectedId!, themeVars ? { ...themeVars } : undefined),
    onSuccess: () => navigate(`/sites/${siteId}/builder/${pageId}`),
  })

  const filtered = activeCategory === 'all'
    ? templates
    : templates.filter((t) => t.category === activeCategory)

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      {/* Left: Template Browser */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="bg-white border-b border-slate-200 px-6 py-4 flex items-center gap-4">
          <button
            onClick={() => navigate(`/sites/${siteId}`)}
            className="p-2 rounded-lg hover:bg-slate-100 text-slate-500"
          >
            <ArrowLeft size={18} />
          </button>
          <div>
            <h1 className="text-xl font-bold text-slate-900">Choose a Template</h1>
            <p className="text-sm text-slate-500">Select a template and customize the theme</p>
          </div>
          <div className="ml-auto flex items-center gap-3">
            {selectedId && (
              <Button variant="ghost" size="sm" onClick={() => setShowTheme(!showTheme)}>
                <Palette size={15} className="mr-1.5" />
                Customize Theme
              </Button>
            )}
            <Button
              disabled={!selectedId}
              loading={applyMutation.isPending}
              onClick={() => applyMutation.mutate()}
            >
              <Wand2 size={15} className="mr-1.5" />
              Apply Template
            </Button>
          </div>
        </div>

        {/* Category tabs */}
        <div className="bg-white border-b border-slate-200 px-6">
          <div className="flex gap-1">
            {['all', ...categories].map((cat) => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={cn(
                  'px-4 py-3 text-sm font-medium capitalize border-b-2 transition-colors',
                  activeCategory === cat
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-slate-500 hover:text-slate-700'
                )}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Grid */}
        <div className="flex-1 overflow-auto p-6">
          <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4">
            {filtered.map((t) => (
              <TemplateCard
                key={t.id}
                template={t}
                selected={selectedId === t.id}
                onSelect={() => handleSelect(t)}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Right: Theme Customizer (when open) */}
      {showTheme && selectedTemplate && themeVars && (
        <div className="w-72 bg-slate-800 border-l border-slate-700 flex flex-col overflow-hidden">
          <div className="p-4 border-b border-slate-700">
            <h2 className="text-sm font-semibold text-white flex items-center gap-2">
              <Palette size={15} className="text-blue-400" />
              Theme Customizer
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">{selectedTemplate.name}</p>
          </div>

          <div className="flex-1 overflow-auto p-4">
            <ThemeCustomizer baseVars={themeVars} onChange={setThemeVars} />
          </div>

          {/* Live preview bar */}
          <div className="p-3 border-t border-slate-700">
            <div
              className="h-8 rounded-lg flex items-center justify-center text-white text-xs font-semibold transition-all"
              style={{ background: themeVars.primary_color, borderRadius: themeVars.border_radius }}
            >
              Preview Button
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
