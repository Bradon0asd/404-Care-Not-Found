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
  function todayDate() {
    return new Intl.DateTimeFormat('en-CA', {
      timeZone: 'Asia/Taipei',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    }).format(new Date())
  }
  const arrivalDay = 100 // "這是我來臺灣的第 N 天"
  const careRecipientCount = 2 // "這是我照顧的第 N 個人"

  const entries = ref<DiaryEntry[]>([
    {
      day: 100,
      title: '',
      date: todayDate(),
      content: '',
      imageUrl: null,
      visibility: 'private',
    },
  ])

  function canWriteDay(day: number) {
    return Number.isInteger(day) && day === arrivalDay
  }

  function entryForDay(day: number): DiaryEntry {
    if (!canWriteDay(day)) throw new Error('Only today’s diary can be written')
    const existing = entries.value.find((e) => e.day === day)
    if (existing) return existing
    const created: DiaryEntry = {
      day,
      title: '',
      date: todayDate(),
      content: '',
      imageUrl: null,
      visibility: 'private',
    }
    entries.value.push(created)
    return entries.value[entries.value.length - 1]!
  }

  return { arrivalDay, careRecipientCount, entries, entryForDay, canWriteDay, todayDate }
})
