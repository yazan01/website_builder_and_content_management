import { useEffect, useRef } from 'react'
import grapesjs from 'grapesjs'
import type { Editor } from 'grapesjs'
import 'grapesjs/dist/css/grapes.min.css'
import { buildGrapesConfig } from '../../grapes/config'
import { registerBlocks } from '../../grapes/blocks'
import { registerBackendStorage } from '../../grapes/plugins/backendStorage'
import { useBuilderStore } from '../../store/builderStore'
import { consumePendingComponent } from '../../grapes/dragStore'

interface GrapesEditorProps {
  pageId: number
  onReady?: (editor: Editor) => void
}

export function GrapesEditor({ pageId, onReady }: GrapesEditorProps) {
  const editorRef = useRef<Editor | null>(null)
  const { setDirty, setSaving, setLastSaved } = useBuilderStore()

  useEffect(() => {
    if (editorRef.current) {
      editorRef.current.destroy()
      editorRef.current = null
    }

    const editor = grapesjs.init(buildGrapesConfig(pageId))
    editorRef.current = editor

    registerBackendStorage(editor, pageId)
    registerBlocks(editor)

    // Mark dirty on any change — no auto-save
    editor.on('change:changesCount', () => setDirty(true))

    // Track manual save state (toolbar Save button)
    editor.on('storage:start:store', () => setSaving(true))
    editor.on('storage:end:store', () => {
      setSaving(false)
      setLastSaved(new Date())
      setDirty(false)
    })
    editor.on('storage:error:store', () => setSaving(false))

    // Drag-drop from Sections panel into canvas iframe
    editor.on('load', () => {
      try {
        const frameEl = editor.Canvas.getFrameEl() as HTMLIFrameElement | null
        const doc = frameEl?.contentDocument
        if (!doc) return
        doc.addEventListener('dragover', (e) => e.preventDefault())
        doc.addEventListener('drop', (e) => {
          e.preventDefault()
          const comp = consumePendingComponent()
          if (comp) editor.addComponents(comp)
        })
      } catch (_) { /* cross-origin guard */ }
    })

    onReady?.(editor)

    return () => {
      editor.destroy()
      editorRef.current = null
    }
  }, [pageId])

  return (
    <div id="gjs" className="flex-1 h-full" />
  )
}

export function getEditorInstance(): Editor | null {
  // Access via window for external triggers
  return (window as unknown as { __grapes?: Editor }).__grapes ?? null
}
