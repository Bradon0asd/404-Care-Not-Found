<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import SegmentedToggle from '@/components/common/SegmentedToggle.vue'
import { useScheduleStore } from '@/stores/schedule'
import type { ScheduleEntry } from '@/components/tab01-dashboard/ScheduleTable.vue'

const router = useRouter()
const scheduleStore = useScheduleStore()

const dayType = ref<'weekday' | 'weekend'>('weekday')
const day = ref<ScheduleEntry['day']>('mon')
const hour = ref(9)
const note = ref('')

const weekdayOptions = [
  { value: 'mon', label: '星期一' },
  { value: 'tue', label: '星期二' },
  { value: 'wed', label: '星期三' },
  { value: 'thu', label: '星期四' },
  { value: 'fri', label: '星期五' },
]
const weekendOptions = [
  { value: 'sat', label: '星期六' },
  { value: 'sun', label: '星期日' },
]
const hourOptions = Array.from({ length: 14 }, (_, i) => 7 + i)

function submit() {
  if (!note.value.trim()) return
  scheduleStore.addEntry({ day: day.value, hour: hour.value, activity: note.value.trim() })
  router.push('/dashboard')
}
</script>

<template>
  <PageContainer>
    <template #header><AppHeader /></template>

    <div class="flex-1 space-y-5 px-4 py-4">
      <h1 class="text-base font-bold text-ink-950">新增排程</h1>

      <div>
        <p class="mb-2 text-sm text-ink-700">選擇類別</p>
        <SegmentedToggle
          variant="chip"
          :model-value="dayType"
          :options="[
            { value: 'weekday', label: '平日' },
            { value: 'weekend', label: '周末' },
          ]"
          @update:model-value="
            (v) => {
              dayType = v as 'weekday' | 'weekend'
              day = v === 'weekday' ? 'mon' : 'sat'
            }
          "
        />
      </div>

      <label class="block rounded-xl bg-ink-200 px-4 py-3">
        <span class="text-sm text-ink-700">選擇星期</span>
        <select v-model="day" class="mt-1 block w-full bg-transparent text-sm font-medium text-ink-950">
          <option v-for="opt in dayType === 'weekday' ? weekdayOptions : weekendOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
      </label>

      <label class="block rounded-xl bg-ink-200 px-4 py-3">
        <span class="text-sm text-ink-700">選擇詳細時間點</span>
        <select v-model.number="hour" class="mt-1 block w-full bg-transparent text-sm font-medium text-ink-950">
          <option v-for="h in hourOptions" :key="h" :value="h">{{ String(h).padStart(2, '0') }}:00</option>
        </select>
      </label>

      <label class="block">
        <span class="mb-2 block text-sm text-ink-700">新增事項</span>
        <textarea
          v-model="note"
          rows="4"
          placeholder="簡單概述 {{照顧者}} 日常紀錄"
          class="w-full rounded-xl bg-ink-200 px-4 py-3 text-sm text-ink-950 placeholder:text-ink-600"
        ></textarea>
      </label>

      <div class="space-y-3 pt-2">
        <BaseButton variant="primary" @click="submit">新增排程</BaseButton>
        <BaseButton variant="outline" @click="router.back()">取消</BaseButton>
      </div>
    </div>

    <template #footer><BottomTabBar /></template>
  </PageContainer>
</template>
