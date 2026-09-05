import { del, get, patch, post } from './client'

export type StickyNotePriority = 'urgent' | 'normal' | 'low'
export type StickyNoteCategory = 'leave' | 'family' | 'care' | 'shopping' | 'other'

export interface StickyNoteDto {
  id: number
  creator_id: number
  title: string
  content: string
  category: StickyNoteCategory | null
  priority: StickyNotePriority
  images: string[]
  is_reviewed: boolean
  is_private: boolean
  created_at: string
  updated_at: string
}

export interface StickyNotePayload {
  title: string
  content: string
  category?: StickyNoteCategory | null
  priority?: StickyNotePriority
  images?: string[]
  is_private?: boolean
}

export function listNotes() {
  return get<StickyNoteDto[]>('/api/notes')
}

export function createNote(payload: StickyNotePayload) {
  return post<StickyNoteDto>('/api/notes', payload)
}

export function updateNote(id: number, payload: Partial<StickyNotePayload>) {
  return patch<StickyNoteDto>(`/api/notes/${id}`, payload)
}

export function reviewNote(id: number) {
  return patch<StickyNoteDto>(`/api/notes/${id}/review`, {})
}

export function deleteNote(id: number) {
  return del<null>(`/api/notes/${id}`)
}
