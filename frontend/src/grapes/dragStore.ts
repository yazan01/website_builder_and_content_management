/**
 * Shared state between SectionsPanel (drag source) and GrapesEditor (drop target).
 * Module-level variable — safe because only one editor is mounted at a time.
 */
let pendingComponent: Record<string, unknown> | null = null

export function setPendingComponent(c: Record<string, unknown> | null) {
  pendingComponent = c
}

export function consumePendingComponent(): Record<string, unknown> | null {
  const c = pendingComponent
  pendingComponent = null
  return c
}
