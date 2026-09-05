import { del, get, patch, post } from './client'
import { uploadImage } from './uploads'

export interface DiaryDto {
  id: number
  creator_id: number
  title: string | null
  content: string
  entry_date: string | null
  image_url: string | null
  is_private: boolean
  created_at: string
  updated_at: string
}

export interface DiaryPayload {
  title?: string | null
  content: string
  entry_date?: string | null
  image_url?: string | null
  is_private: boolean
}

export function listDiaries() {
  return get<DiaryDto[]>('/api/diaries')
}

export function createDiary(payload: DiaryPayload) {
  return post<DiaryDto>('/api/diaries', payload)
}

export function updateDiary(id: number, payload: Partial<DiaryPayload>) {
  return patch<DiaryDto>(`/api/diaries/${id}`, payload)
}

export function deleteDiary(id: number) {
  return del<null>(`/api/diaries/${id}`)
}

export async function uploadDiaryImage(file: File) {
  return uploadImage(file)
}
