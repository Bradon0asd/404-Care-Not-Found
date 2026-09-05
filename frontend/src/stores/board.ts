import { defineStore } from 'pinia'
import { ref } from 'vue'

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

export const useBoardStore = defineStore('board', () => {
  const notes = ref<StickyNote[]>([
    {
      id: 'seed-1',
      level: 'urgent',
      title: '我印尼家人上週生病住院了，想跟雇主請假回去看看',
      tag: '家人生病',
      content: '我印尼家人上週生病住院了，想跟雇主請假回去看看，不確定假期怎麼安排比較好。',
      imageUrl: null,
      visibility: 'employer',
      employerStatus: 'read',
    },
    {
      id: 'seed-2',
      level: 'urgent',
      title: '我印尼家人上週生病住院了，想跟雇主請假回去看看',
      tag: '家人生病',
      content: '我印尼家人上週生病住院了，想跟雇主請假回去看看，不確定假期怎麼安排比較好。',
      imageUrl: null,
      visibility: 'employer',
      employerStatus: 'unread',
    },
    {
      id: 'seed-3',
      level: 'urgent',
      title: '我印尼家人上週生病住院了，想跟雇主請假回去看看',
      tag: '家人生病',
      content: '我印尼家人上週生病住院了，想跟雇主請假回去看看，不確定假期怎麼安排比較好。',
      imageUrl: null,
      visibility: 'private',
      employerStatus: 'no-access',
    },
    {
      id: 'seed-4',
      level: 'normal',
      title: '禮拜三想請假',
      tag: '請假',
      content:
        '我印尼非常好的朋友來臺灣旅遊，他們很久才來一次，我想請教他們出去玩，不知道可不可以。',
      imageUrl: null,
      visibility: 'private',
      employerStatus: 'no-access',
    },
    {
      id: 'seed-5',
      level: 'urgent',
      title: '阿嬤睡不著一直吵著要下床',
      tag: '照護',
      content: '阿嬤今天9:00開始就一直吵著要下床，一路吵到下午15:00自己累了睡著。',
      imageUrl: null,
      visibility: 'employer',
      employerStatus: 'unread',
    },
    {
      id: 'seed-6',
      level: 'normal',
      title: '超市紙尿布補貨',
      tag: '額外開銷',
      content: '家裡紙尿布快用完了，想跟雇主說一聲要補貨。',
      imageUrl: null,
      visibility: 'employer',
      employerStatus: 'read',
    },
  ])

  notes.value.forEach((note) => {
    note.demo = true
  })

  function addNote(note: Omit<StickyNote, 'id' | 'employerStatus'>) {
    const id = crypto.randomUUID()
    notes.value.unshift({
      ...note,
      id,
      employerStatus: note.visibility === 'employer' ? 'unread' : 'no-access',
    })
    return id
  }

  return { notes, addNote }
})
