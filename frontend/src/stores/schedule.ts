import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ScheduleEntry } from '@/components/tab01-dashboard/ScheduleTable.vue'

export const useScheduleStore = defineStore('schedule', () => {
  const entries = ref<ScheduleEntry[]>([
    { day: 'mon', hour: 9, activity: '吃胃藥' },
    { day: 'tue', hour: 9, activity: '吃胃藥' },
    { day: 'wed', hour: 9, activity: '吃胃藥' },
    { day: 'thu', hour: 9, activity: '吃胃藥' },
    { day: 'fri', hour: 9, activity: '吃胃藥' },
    { day: 'mon', hour: 13, activity: '復健' },
    { day: 'mon', hour: 14, activity: '復健' },
    { day: 'wed', hour: 13, activity: '復健' },
    { day: 'fri', hour: 13, activity: '公廟拜拜' },
    { day: 'fri', hour: 14, activity: '公廟拜拜' },
    { day: 'sat', hour: 9, activity: '吃胃藥' },
    { day: 'sun', hour: 9, activity: '吃胃藥' },
  ])

  function addEntry(entry: ScheduleEntry) {
    entries.value.push(entry)
  }

  return { entries, addEntry }
})
