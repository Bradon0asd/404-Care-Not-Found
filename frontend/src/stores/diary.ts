import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  createDiary,
  listDiaries,
  updateDiary,
  uploadDiaryImage,
  type DiaryDto,
} from '@/api/diaries'
import { ApiError } from '@/api/client'

export type DiaryVisibility = 'private' | 'shared'

export interface DiaryEntry {
  id: number | null
  day: number
  title: string
  date: string
  content: string
  imageUrl: string | null
  visibility: DiaryVisibility
}

export const useDiaryStore = defineStore('diary', () => {
  const arrivalDay = 100
  const careRecipientCount = 2

  const entries = ref<DiaryEntry[]>([])
  const loading = ref(false)
  const saving = ref(false)
  const error = ref<string | null>(null)

  function entryForDay(day: number): DiaryEntry {
    const existing = entries.value.find((entry) => entry.day === day)
    if (existing) return existing

    const created: DiaryEntry = {
      id: null,
      day,
      title: '',
      date: new Date().toISOString().slice(0, 10),
      content: '',
      imageUrl: null,
      visibility: 'private',
    }
    entries.value.push(created)
    return entries.value[entries.value.length - 1]!
  }

  async function loadEntries() {
    loading.value = true
    error.value = null
    try {
      const diaries = await listDiaries()
      entries.value = diaries.map(toEntry)
      return entries.value
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load diaries'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function saveEntry(entry: DiaryEntry, visibility: DiaryVisibility, imageFile?: File | null) {
    saving.value = true
    error.value = null
    try {
      const imageUrl = imageFile ? await uploadDiaryImage(imageFile) : entry.imageUrl
      const payload = {
        title: entry.title.trim() || null,
        content: entry.content.trim(),
        entry_date: entry.date,
        image_url: imageUrl,
        is_private: visibility === 'private',
      }

      const diary = await saveDiaryPayload(entry.id, payload)
      const saved = { ...toEntry(diary), day: entry.day }
      const index = entries.value.findIndex((item) => item.day === entry.day)
      if (index >= 0) entries.value[index] = saved
      else entries.value.unshift(saved)
      return saved
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to save diary'
      throw err
    } finally {
      saving.value = false
    }
  }

  function toEntry(diary: DiaryDto, index = 0): DiaryEntry {
    const createdAt = diary.created_at ? new Date(diary.created_at) : new Date()
    return {
      id: diary.id,
      day: arrivalDay + index,
      title: diary.title ?? '',
      date: diary.entry_date ?? createdAt.toISOString().slice(0, 10),
      content: diary.content,
      imageUrl: diary.image_url,
      visibility: diary.is_private ? 'private' : 'shared',
    }
  }

  async function saveDiaryPayload(
    id: number | null,
    payload: {
      title: string | null
      content: string
      entry_date: string
      image_url: string | null
      is_private: boolean
    },
  ) {
    try {
      return id ? await updateDiary(id, payload) : await createDiary(payload)
    } catch (err) {
      if (!isEntryDateUnsupported(err)) throw err
      const { entry_date: _entryDate, ...legacyPayload } = payload
      return id ? await updateDiary(id, legacyPayload) : await createDiary(legacyPayload)
    }
  }

  function isEntryDateUnsupported(err: unknown) {
    if (!(err instanceof ApiError) || err.status !== 422) return false
    const details = err.details as Record<string, unknown> | undefined
    const jsonDetails = details?.json as Record<string, unknown> | undefined
    return Array.isArray(details?.entry_date) || Array.isArray(jsonDetails?.entry_date)
  }

  return {
    arrivalDay,
    careRecipientCount,
    entries,
    loading,
    saving,
    error,
    entryForDay,
    loadEntries,
    saveEntry,
  }
})
