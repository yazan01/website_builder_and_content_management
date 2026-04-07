import type { Editor } from 'grapesjs'
import { pagesApi } from '../../api/pages'

export function registerBackendStorage(editor: Editor, pageId: number) {
  const sm = editor.StorageManager

  sm.add('backend', {
    async load() {
      const data = await pagesApi.loadBuilder(pageId)
      return data.grapes_data || {}
    },
    async store(data: Record<string, unknown>) {
      await pagesApi.saveBuilder(pageId, data)
    },
  })
}
