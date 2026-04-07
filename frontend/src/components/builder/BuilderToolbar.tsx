import { Save, Eye, Undo2, Redo2, Smartphone, Tablet, Monitor, ArrowLeft, LayoutTemplate, Globe, CheckCircle } from 'lucide-react'
import { Link } from 'react-router-dom'
import type { Editor } from 'grapesjs'
import { useBuilderStore } from '../../store/builderStore'
import { pagesApi } from '../../api/pages'
import { cn } from '../../utils/cn'

interface BuilderToolbarProps {
  editor: Editor | null
  siteId: number
  pageId: number
  pageTitle: string
}

export function BuilderToolbar({ editor, siteId, pageId, pageTitle }: BuilderToolbarProps) {
  const {
    isDirty, isSaving, isPublishing, lastSaved, hasUnpublishedChanges,
    setSaving, setLastSaved, setDirty, setIsPublishing, setHasUnpublishedChanges,
  } = useBuilderStore()

  const saveDraft = async () => {
    if (!editor || isSaving) return
    setSaving(true)
    try {
      const result = await pagesApi.saveBuilder(pageId, editor.getProjectData())
      setLastSaved(new Date())
      setDirty(false)
      setHasUnpublishedChanges(result.has_unpublished_changes ?? true)
    } finally {
      setSaving(false)
    }
  }

  const publishDraft = async () => {
    if (isPublishing) return
    // Save first if dirty
    if (isDirty && editor) await saveDraft()
    setIsPublishing(true)
    try {
      await pagesApi.publishDraft(pageId)
      setHasUnpublishedChanges(false)
    } finally {
      setIsPublishing(false)
    }
  }

  const undo = () => editor?.UndoManager.undo()
  const redo = () => editor?.UndoManager.redo()

  return (
    <div className="flex items-center gap-2 px-4 py-2 bg-slate-800 text-white border-b border-slate-700 h-12 shrink-0">
      {/* Back */}
      <Link to={`/sites/${siteId}`} className="flex items-center gap-1.5 text-slate-400 hover:text-white text-sm mr-1">
        <ArrowLeft size={15} /> Back
      </Link>

      <div className="w-px h-6 bg-slate-600" />

      <span className="text-sm font-medium text-slate-200">{pageTitle}</span>

      {/* Draft / live status badge */}
      {hasUnpublishedChanges && !isDirty && (
        <span className="text-[10px] bg-amber-500/20 text-amber-400 border border-amber-500/30 px-2 py-0.5 rounded-full font-medium">
          Draft not published
        </span>
      )}

      <div className="flex-1" />

      {/* Device switcher */}
      <div className="flex items-center gap-1 bg-slate-700 rounded-lg p-1">
        {([['Desktop', Monitor], ['Tablet', Tablet], ['Mobile', Smartphone]] as const).map(([d, Icon]) => (
          <button
            key={d}
            onClick={() => editor?.setDevice(d)}
            title={d}
            className="p-1.5 rounded hover:bg-slate-600 text-slate-300 hover:text-white"
          >
            <Icon size={14} />
          </button>
        ))}
      </div>

      <div className="w-px h-6 bg-slate-600" />

      {/* Undo/Redo */}
      <button onClick={undo} title="Undo" className="p-1.5 rounded hover:bg-slate-700 text-slate-300 hover:text-white">
        <Undo2 size={15} />
      </button>
      <button onClick={redo} title="Redo" className="p-1.5 rounded hover:bg-slate-700 text-slate-300 hover:text-white">
        <Redo2 size={15} />
      </button>

      <div className="w-px h-6 bg-slate-600" />

      {/* Templates */}
      <Link
        to={`/sites/${siteId}/templates/${pageId}`}
        className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-sm text-slate-300 hover:bg-slate-700 hover:text-white transition-colors"
      >
        <LayoutTemplate size={14} /> Templates
      </Link>

      {/* Preview */}
      <Link
        to={`/sites/${siteId}/preview/${pageId}`}
        target="_blank"
        className="p-1.5 rounded hover:bg-slate-700 text-slate-300 hover:text-white"
        title="Preview"
      >
        <Eye size={15} />
      </Link>

      <div className="w-px h-6 bg-slate-600" />

      {/* Save Draft + Publish — always visible */}
      <div className="flex items-center gap-1 bg-slate-700/60 rounded-xl p-1">
        {/* Status dot */}
        <span className={cn(
          'w-2 h-2 rounded-full ml-1 shrink-0',
          isSaving        ? 'bg-yellow-400 animate-pulse' :
          isDirty         ? 'bg-orange-400 animate-pulse' :
          hasUnpublishedChanges ? 'bg-amber-400' :
          lastSaved       ? 'bg-green-400' : 'bg-slate-500'
        )} />

        <button
          onClick={saveDraft}
          disabled={isSaving || !isDirty}
          title={isDirty ? 'Save draft (live site stays unchanged)' : 'No unsaved changes'}
          className={cn(
            'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all',
            isDirty
              ? 'bg-slate-600 hover:bg-slate-500 text-white'
              : 'text-slate-500 cursor-default'
          )}
        >
          <Save size={13} />
          {isSaving ? 'Saving…' : 'Save Draft'}
        </button>

        <button
          onClick={publishDraft}
          disabled={isPublishing || (!isDirty && !hasUnpublishedChanges)}
          title={(isDirty || hasUnpublishedChanges) ? 'Push draft to live site' : 'Nothing to publish'}
          className={cn(
            'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-semibold transition-all',
            (isDirty || hasUnpublishedChanges)
              ? 'bg-blue-600 hover:bg-blue-500 text-white shadow-md shadow-blue-900/40'
              : 'text-slate-500 cursor-default'
          )}
        >
          {isPublishing
            ? <><CheckCircle size={13} className="animate-spin" /> Publishing…</>
            : <><Globe size={13} /> Publish</>}
        </button>
      </div>

      {lastSaved && !isDirty && (
        <span className="text-[11px] text-slate-500 hidden xl:block">
          {lastSaved.toLocaleTimeString()}
        </span>
      )}
    </div>
  )
}
