<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import SegmentedToggle from '@/components/common/SegmentedToggle.vue'
import { useScheduleStore } from '@/stores/schedule'
import { useAccountStore } from '@/stores/account'
import type { ScheduleEntry } from '@/components/tab01-dashboard/ScheduleTable.vue'
import { scheduleHours as hourOptions } from '@/utils/schedule'

const router = useRouter()
const scheduleStore = useScheduleStore()
const account = useAccountStore()

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

async function submit() {
  if (!note.value.trim()) return
  if (!account.currentCareRecipientId) {
    await account.loadAccount()
  }
  if (!account.currentCareRecipientId) return
  await scheduleStore.addEntry(account.currentCareRecipientId, {
    day: day.value,
    hour: hour.value,
    activity: note.value.trim(),
  })
  router.push('/dashboard')
}
</script>

<template>
  <PageContainer>
    <template #header><AppHeader /></template>

    <div class="flex flex-1 flex-col px-5 py-7">
      <h1 class="mb-3 text-lg font-bold tracking-[0.18em] text-ink-950">{{ $t('新增排程') }}</h1>

      <div class="flex h-[60px] items-center gap-4 rounded-xl bg-ink-200 px-5">
        <p class="shrink-0 text-sm font-bold tracking-[0.12em] text-ink-600">
          {{ $t('選擇類別') }}
        </p>
        <SegmentedToggle
          class="flex-1"
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

      <label class="mt-5 flex h-[60px] items-center rounded-xl bg-ink-200 px-5">
        <span class="shrink-0 text-sm font-bold tracking-[0.12em] text-ink-600">{{
          $t('選擇星期')
        }}</span>
        <select
          v-model="day"
          class="ml-auto bg-transparent text-right text-sm font-bold text-ink-600 outline-none"
        >
          <option
            v-for="opt in dayType === 'weekday' ? weekdayOptions : weekendOptions"
            :key="opt.value"
            :value="opt.value"
          >
            {{ $t(opt.label) }}
          </option>
        </select>
      </label>

      <label class="mt-5 flex h-[60px] items-center rounded-xl bg-ink-200 px-5">
        <span class="shrink-0 text-sm font-bold tracking-[0.12em] text-ink-600">{{
          $t('選擇詳細時間點')
        }}</span>
        <select
          v-model.number="hour"
          class="ml-auto bg-transparent text-right font-mono text-base font-bold tracking-[0.12em] text-ink-600 outline-none"
        >
          <option v-for="h in hourOptions" :key="h" :value="h">
            {{ $t(String(h).padStart(2, '0')) }}:00
          </option>
        </select>
      </label>

      <label class="mt-5 block h-[200px] rounded-xl bg-ink-200 px-5 py-5">
        <span class="mb-4 block text-sm font-bold tracking-[0.12em] text-ink-600">{{
          $t('新增事項')
        }}</span>
        <textarea
          v-model="note"
          rows="5"
          :placeholder="$t('簡單概述 {name} 的日常紀錄', { name: account.careRecipient.name })"
          class="w-full resize-none bg-transparent p-0 text-sm text-ink-950 outline-none placeholder:text-ink-500"
        ></textarea>
      </label>

      <div class="mt-auto space-y-5 pt-8">
        <BaseButton variant="primary" @click="submit">{{ $t('新增排程') }}</BaseButton>
        <BaseButton variant="outline" @click="router.back()">{{ $t('取消') }}</BaseButton>
      </div>
    </div>

    <template #footer><BottomTabBar /></template>
  </PageContainer>
</template>
