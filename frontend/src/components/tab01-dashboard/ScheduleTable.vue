<script setup lang="ts">
import { computed, ref } from 'vue'
import SegmentedToggle from '@/components/common/SegmentedToggle.vue'

export interface ScheduleEntry {
  day: 'mon' | 'tue' | 'wed' | 'thu' | 'fri' | 'sat' | 'sun'
  hour: number
  activity: string
}

const props = defineProps<{
  careRecipientName: string
  entries: ScheduleEntry[]
}>()

const dayType = ref<'weekday' | 'weekend'>('weekday')

const weekdayCols = [
  { day: 'mon', label: '一' },
  { day: 'tue', label: '二' },
  { day: 'wed', label: '三' },
  { day: 'thu', label: '四' },
  { day: 'fri', label: '五' },
] as const
const weekendCols = [
  { day: 'sat', label: '六' },
  { day: 'sun', label: '日' },
] as const

const columns = computed(() => (dayType.value === 'weekday' ? weekdayCols : weekendCols))
const hours = Array.from({ length: 14 }, (_, i) => 7 + i) // 07:00–21:00

function activityFor(day: string, hour: number) {
  return props.entries.find((e) => e.day === day && e.hour === hour)?.activity
}
</script>

<template>
  <div>
    <div class="mb-3 flex items-center justify-between">
      <h2 class="text-sm font-bold text-ink-950">{{ careRecipientName }} 的日常照護統整排程表</h2>
    </div>

    <SegmentedToggle
      class="mb-3"
      variant="chip"
      :model-value="dayType"
      :options="[
        { value: 'weekday', label: '平日' },
        { value: 'weekend', label: '周末' },
      ]"
      @update:model-value="(v) => (dayType = v as 'weekday' | 'weekend')"
    />

    <div class="overflow-x-auto rounded-xl border border-ink-400">
      <table class="w-full min-w-[280px] border-collapse text-center text-[11px]">
        <thead>
          <tr class="bg-accent text-ink-950">
            <th class="w-14 border-r border-ink-300 py-2 font-bold">時間</th>
            <th v-for="col in columns" :key="col.day" class="border-r border-ink-300 py-2 font-bold last:border-r-0">
              {{ col.label }}
            </th>
          </tr>
        </thead>
        <tbody>
          <template v-for="hour in hours" :key="hour">
            <tr v-if="hour === 12" class="h-2 bg-white">
              <td :colspan="columns.length + 1"></td>
            </tr>
            <tr class="border-t border-ink-300">
              <td class="border-r border-ink-300 py-2 text-ink-600">{{ String(hour).padStart(2, '0') }}:00</td>
              <td
                v-for="col in columns"
                :key="col.day"
                class="border-r border-ink-300 py-2 last:border-r-0"
                :class="activityFor(col.day, hour) ? 'bg-accent/20 font-medium text-ink-950' : ''"
              >
                {{ activityFor(col.day, hour) ?? '' }}
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>
