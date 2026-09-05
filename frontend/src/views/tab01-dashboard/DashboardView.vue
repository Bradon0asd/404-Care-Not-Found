<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'
import MedicalDisclaimerBanner from '@/components/common/MedicalDisclaimerBanner.vue'
import SegmentedToggle from '@/components/common/SegmentedToggle.vue'
import FloatingAddButton from '@/components/common/FloatingAddButton.vue'
import VitalSignCard from '@/components/tab01-dashboard/VitalSignCard.vue'
import ScheduleTable from '@/components/tab01-dashboard/ScheduleTable.vue'
import { useScheduleStore } from '@/stores/schedule'
import { useAccountStore } from '@/stores/account'

const router = useRouter()
const view = ref<'vitals' | 'schedule'>('vitals')
const scheduleStore = useScheduleStore()
const account = useAccountStore()

const vitals = [
  {
    label: '血壓',
    todayValue: '120/70',
    updatedAt: '2026/08/29 09:00 A.M.',
    weekAvgValue: '125/76',
    changeNote: '收縮壓下降 5 mmHg；舒張壓下降 6 mmHg',
    assessment: '與過去一週相近，數值穩定。如有疑慮，建議諮詢醫療人員。',
    trendTone: 'positive' as const,
  },
  {
    label: '血糖',
    todayValue: '80',
    updatedAt: '2026/08/29 09:30 A.M.',
    weekAvgValue: '70',
    changeNote: '今日上升 10 mg/dL',
    assessment: '較過去一週略低，建議留意。如有疑慮，建議諮詢醫療人員。',
    trendTone: 'positive' as const,
  },
  {
    label: '心跳',
    todayValue: '80',
    updatedAt: '2026/08/29 09:35 A.M.',
    weekAvgValue: '85',
    changeNote: '今日心跳一分鐘下降 5 次',
    assessment: '與過去一週相近，數值穩定。如有疑慮，建議諮詢醫療人員。',
    trendTone: 'negative' as const,
  },
  {
    label: '血氧飽和度',
    todayValue: '98%',
    updatedAt: '2026/08/29 09:40 A.M.',
    weekAvgValue: '95%',
    changeNote: '今日血氧飽和度上升 2%',
    assessment: '較過去一週略升。如有疑慮，建議諮詢醫療人員。',
    trendTone: 'positive' as const,
  },
  {
    label: '體溫',
    todayValue: '36.9°C',
    updatedAt: '2026/08/29 09:42 A.M.',
    weekAvgValue: '36.6°C',
    changeNote: '今日體溫相較過去平均上升 0.3°C',
    assessment: '較過去一週略升 0.3°C。如有疑慮，建議諮詢醫療人員。',
    trendTone: 'positive' as const,
  },
  {
    label: '呼吸頻率',
    todayValue: '24',
    updatedAt: '2026/08/29 09:48 A.M.',
    weekAvgValue: '22',
    changeNote: '今日呼吸頻率一分鐘提高 2 次',
    assessment: '較過去一週略高，建議留意。如有疑慮，建議諮詢醫療人員。',
    trendTone: 'negative' as const,
  },
]
</script>

<template>
  <PageContainer>
    <template #header>
      <AppHeader />
      <MedicalDisclaimerBanner />
    </template>

    <div class="flex-1 px-5 py-4">
      <SegmentedToggle
        class="mb-4"
        variant="tab"
        :model-value="view"
        :options="[
          { value: 'vitals', label: '儀錶板' },
          { value: 'schedule', label: '每日排程表' },
        ]"
        @update:model-value="(v) => (view = v as 'vitals' | 'schedule')"
      />

      <div v-if="view === 'vitals'" class="grid grid-cols-2 gap-3">
        <VitalSignCard v-for="vital in vitals" :key="vital.label" v-bind="vital" />
      </div>

      <ScheduleTable
        v-else
        :care-recipient-name="account.careRecipient.name"
        :entries="scheduleStore.entries"
      />
    </div>

    <template #fab><FloatingAddButton @click="router.push('/dashboard/add-schedule')" /></template>
    <template #footer><BottomTabBar /></template>
  </PageContainer>
</template>
