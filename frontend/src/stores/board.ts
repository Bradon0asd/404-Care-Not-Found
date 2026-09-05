import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  createNote,
  deleteNote,
  listNotes,
  updateNote,
  type StickyNoteDto,
  type StickyNotePriority,
} from '@/api/notes'

export type NoteLevel = 'urgent' | 'normal' | 'minor'
export type NoteVisibility = 'private' | 'employer'
export type EmployerReadStatus = 'read' | 'unread' | 'no-access'

export interface StickyNote {
  demo?: boolean
  id: string
  level: NoteLevel
  title: string
  tag: string
  content: string
  imageUrl: string | null
  visibility: NoteVisibility
  employerStatus: EmployerReadStatus
}

const PRIORITY_TO_BACKEND: Record<NoteLevel, StickyNotePriority> = {
  urgent: 'urgent',
  normal: 'normal',
  minor: 'low',
}

const PRIORITY_FROM_BACKEND: Record<StickyNotePriority, NoteLevel> = {
  urgent: 'urgent',
  normal: 'normal',
  low: 'minor',
}

function toNote(note: StickyNoteDto): StickyNote {
  const visibility: NoteVisibility = note.is_private ? 'private' : 'employer'
  return {
    id: String(note.id),
    level: PRIORITY_FROM_BACKEND[note.priority],
    title: note.title,
    tag: note.category ?? 'other',
    content: note.content,
    imageUrl: note.images[0] ?? null,
    visibility,
    employerStatus: visibility === 'private' ? 'no-access' : note.is_reviewed ? 'read' : 'unread',
  }
}

export const useBoardStore = defineStore('board', () => {
  const notes = ref<StickyNote[]>([])
  const loading = ref(false)
  const saving = ref(false)
  const error = ref<string | null>(null)

  async function loadNotes() {
    loading.value = true
    error.value = null
    try {
      notes.value = (await listNotes()).map(toNote)
      return notes.value
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load notes'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function addNote(note: Omit<StickyNote, 'id' | 'employerStatus'>) {
    saving.value = true
    error.value = null
    try {
      const saved = toNote(
        await createNote({
          title: note.title.trim() || note.content.trim().slice(0, 40),
          content: note.content.trim(),
          category: note.tag.trim() ? 'other' : null,
          priority: PRIORITY_TO_BACKEND[note.level],
          images: note.imageUrl ? [note.imageUrl] : [],
          is_private: note.visibility === 'private',
        }),
      )
      notes.value.unshift(saved)
      return saved.id
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to save note'
      throw err
    } finally {
      saving.value = false
    }
  }

  async function editNote(note: StickyNote) {
    saving.value = true
    error.value = null
    try {
      const saved = toNote(
        await updateNote(Number(note.id), {
          title: note.title.trim() || note.content.trim().slice(0, 40),
          content: note.content.trim(),
          category: note.tag.trim() ? 'other' : null,
          priority: PRIORITY_TO_BACKEND[note.level],
          images: note.imageUrl ? [note.imageUrl] : [],
          is_private: note.visibility === 'private',
        }),
      )
      const index = notes.value.findIndex((item) => item.id === note.id)
      if (index >= 0) notes.value[index] = saved
      return saved
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update note'
      throw err
    } finally {
      saving.value = false
    }
  }

  async function removeNote(note: StickyNote) {
    saving.value = true
    error.value = null
    try {
      await deleteNote(Number(note.id))
      notes.value = notes.value.filter((item) => item.id !== note.id)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete note'
      throw err
    } finally {
      saving.value = false
    }
  }

  return { notes, loading, saving, error, loadNotes, addNote, editNote, removeNote }
})
