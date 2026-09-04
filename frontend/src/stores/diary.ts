import { defineStore } from 'pinia'
import { ref } from 'vue'

export type DiaryVisibility = 'private' | 'shared'

export interface DiaryEntry {
  day: number
  title: string
  date: string // ISO date
  content: string
  imageUrl: string | null
  visibility: DiaryVisibility
}

export const useDiaryStore = defineStore('diary', () => {
  const arrivalDay = 100 // "這是我來臺灣的第 N 天"
  const careRecipientCount = 2 // "這是我照顧的第 N 個人"

  const entries = ref<DiaryEntry[]>([
    {
      day: 100,
      title: '',
      date: '2026-08-25',
      content: '',
      imageUrl: null,
      visibility: 'private',
    },
  ])

  function entryForDay(day: number): DiaryEntry {
    const existing = entries.value.find((e) => e.day === day)
    if (existing) return existing
    const created: DiaryEntry = {
      day,
      title: '',
      date: new Date().toISOString().slice(0, 10),
      content: '',
      imageUrl: null,
      visibility: 'private',
    }
    entries.value.push(created)
    return created
  }

  return { arrivalDay, careRecipientCount, entries, entryForDay }
})
