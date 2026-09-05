import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  createSchedule,
  deleteSchedule,
  listSchedules,
  updateSchedule,
  type CareScheduleDto,
  type ScheduleType,
} from '@/api/schedules'
import type { ScheduleEntry } from '@/components/tab01-dashboard/ScheduleTable.vue'

const DAY_TO_BACKEND: Record<ScheduleEntry['day'], number> = {
  mon: 0,
  tue: 1,
  wed: 2,
  thu: 3,
  fri: 4,
  sat: 5,
  sun: 6,
}

const DAY_FROM_BACKEND = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'] as const

export interface StoredScheduleEntry extends ScheduleEntry {
  id?: number
  scheduleType?: ScheduleType
  description?: string | null
}

function toEntry(schedule: CareScheduleDto): StoredScheduleEntry {
  return {
    id: schedule.id,
    day: DAY_FROM_BACKEND[schedule.weekday ?? 0] ?? 'mon',
    hour: Number(schedule.start_time.slice(0, 2)),
    activity: schedule.title,
    scheduleType: schedule.schedule_type,
    description: schedule.description,
  }
}

function scheduleTypeFor(day: ScheduleEntry['day']): ScheduleType {
  return day === 'sat' || day === 'sun' ? 'weekend' : 'weekday'
}

export const useScheduleStore = defineStore('schedule', () => {
  const entries = ref<StoredScheduleEntry[]>([])
  const loading = ref(false)
  const saving = ref(false)
  const error = ref<string | null>(null)

  async function loadEntries(recipientId: number) {
    loading.value = true
    error.value = null
    try {
      entries.value = (await listSchedules(recipientId)).map(toEntry)
      return entries.value
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load schedules'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function addEntry(recipientId: number, entry: ScheduleEntry) {
    saving.value = true
    error.value = null
    try {
      const schedule = await createSchedule(recipientId, {
        schedule_type: scheduleTypeFor(entry.day),
        weekday: DAY_TO_BACKEND[entry.day],
        start_time: `${String(entry.hour).padStart(2, '0')}:00`,
        title: entry.activity,
        description: null,
      })
      const saved = toEntry(schedule)
      entries.value.push(saved)
      return saved
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to save schedule'
      throw err
    } finally {
      saving.value = false
    }
  }

  async function updateEntry(entry: StoredScheduleEntry, changes: ScheduleEntry) {
    if (!entry.id) return null
    saving.value = true
    error.value = null
    try {
      const updated = toEntry(
        await updateSchedule(entry.id, {
          schedule_type: scheduleTypeFor(changes.day),
          weekday: DAY_TO_BACKEND[changes.day],
          start_time: `${String(changes.hour).padStart(2, '0')}:00`,
          title: changes.activity,
          description: entry.description ?? null,
        }),
      )
      const index = entries.value.findIndex((item) => item.id === entry.id)
      if (index >= 0) entries.value[index] = updated
      return updated
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update schedule'
      throw err
    } finally {
      saving.value = false
    }
  }

  async function deleteEntry(entry: StoredScheduleEntry) {
    if (!entry.id) return
    saving.value = true
    error.value = null
    try {
      await deleteSchedule(entry.id)
      entries.value = entries.value.filter((item) => item.id !== entry.id)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete schedule'
      throw err
    } finally {
      saving.value = false
    }
  }

  return { entries, loading, saving, error, loadEntries, addEntry, updateEntry, deleteEntry }
})
