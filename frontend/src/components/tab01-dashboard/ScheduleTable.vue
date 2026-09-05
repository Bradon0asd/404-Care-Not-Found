<script setup lang="ts">
import { computed, ref } from 'vue'
import SegmentedToggle from '@/components/common/SegmentedToggle.vue'
import { scheduleHours as hours } from '@/utils/schedule'

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

function activityFor(day: string, hour: number) {
  return props.entries.find((e) => e.day === day && e.hour === hour)?.activity
}
</script>

<template>
  <div>
    <div class="mb-3 flex items-center justify-between">
      <h2 class="text-base font-bold text-ink-950">
        {{ $t(careRecipientName) }}{{ $t('的日常照護統整排程表') }}
      </h2>
    </div>

    <SegmentedToggle
      class="mx-auto mb-4 max-w-[200px]"
      variant="chip"
      :model-value="dayType"
      :options="[
        { value: 'weekday', label: '平日' },
        { value: 'weekend', label: '周末' },
      ]"
      @update:model-value="(v) => (dayType = v as 'weekday' | 'weekend')"
    />

    <div class="overflow-hidden rounded-[20px] border border-ink-500">
      <table class="w-full table-fixed border-collapse text-center text-xs">
        <thead>
          <tr class="text-ink-950">
            <th class="w-[60px] border-r border-accent bg-accent py-2 font-bold">
              {{ $t('時間') }}
            </th>
            <th
              v-for="(col, index) in columns"
              :key="col.day"
              class="border-r border-accent py-2 font-bold last:border-r-0"
              :class="index % 2 === 1 ? 'bg-accent' : 'bg-white'"
            >
              {{ $t(col.label) }}
            </th>
          </tr>
        </thead>
        <tbody>
          <template v-for="hour in hours" :key="hour">
            <tr v-if="hour === 12" class="h-5 border-y border-accent bg-white">
              <td :colspan="columns.length + 1"></td>
            </tr>
            <tr class="h-[51px] border-t border-accent">
              <td class="border-r border-accent bg-accent py-2 text-sm font-medium text-ink-600">
                {{ $t(String(hour).padStart(2, '0')) }}:00
              </td>
              <td
                v-for="(col, index) in columns"
                :key="col.day"
                class="border-r border-accent px-1 py-2 font-medium last:border-r-0"
                :class="index % 2 === 1 ? 'bg-accent' : 'bg-white'"
              >
                {{ $t(activityFor(col.day, hour) ?? '') }}
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>
