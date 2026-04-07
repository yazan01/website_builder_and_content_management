import { create } from 'zustand'

interface BuilderState {
  isDirty: boolean          // unsaved draft changes
  isSaving: boolean         // saving draft in progress
  isPublishing: boolean     // publishing draft in progress
  lastSaved: Date | null
  hasUnpublishedChanges: boolean  // draft differs from live
  setDirty: (v: boolean) => void
  setSaving: (v: boolean) => void
  setIsPublishing: (v: boolean) => void
  setLastSaved: (d: Date) => void
  setHasUnpublishedChanges: (v: boolean) => void
}

export const useBuilderStore = create<BuilderState>((set) => ({
  isDirty: false,
  isSaving: false,
  isPublishing: false,
  lastSaved: null,
  hasUnpublishedChanges: false,
  setDirty: (v) => set({ isDirty: v }),
  setSaving: (v) => set({ isSaving: v }),
  setIsPublishing: (v) => set({ isPublishing: v }),
  setLastSaved: (d) => set({ lastSaved: d, isDirty: false }),
  setHasUnpublishedChanges: (v) => set({ hasUnpublishedChanges: v }),
}))
