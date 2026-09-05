<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
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
import { fetchVitalDashboard, type DashboardDto, type VitalSignType } from '@/api/vitalSigns'
import type { ScheduleEntry } from '@/components/tab01-dashboard/ScheduleTable.vue'
import { scheduleHours } from '@/utils/schedule'

const router = useRouter()
const view = ref<'vitals' | 'schedule'>('vitals')
const scheduleStore = useScheduleStore()
const account = useAccountStore()

const dashboard = ref<DashboardDto | null>(null)
const editingSchedule = ref<ScheduleEntry | null>(null)
const editDay = ref<ScheduleEntry['day']>('mon')
const editHour = ref(9)
const editActivity = ref('')

const fallbackVitals = [
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

const metricLabels: Record<VitalSignType, string> = {
  blood_pressure: '血壓',
  blood_glucose: '血糖',
  heart_rate: '心率',
  oxygen_saturation: '血氧',
  temperature: '體溫',
  respiratory_rate: '呼吸',
}

const metricKeys = Object.keys(metricLabels) as VitalSignType[]

const vitals = computed(() => {
  if (!dashboard.value) return fallbackVitals
  const cards = metricKeys
    .map((key) => {
      const metric = dashboard.value?.[key]
      if (!metric?.latest && !metric?.current_average) return null
      const latest = metric.latest
      const average = metric.current_average
      const difference = metric.difference
      return {
        label: metricLabels[key],
        todayValue: latest ? formatMeasurement(latest.value, latest.secondary_value, metric.unit) : '-',
        updatedAt: latest ? formatDateTime(latest.measured_at) : '-',
        weekAvgValue:
          average?.value === null || average?.value === undefined
            ? '-'
            : formatMeasurement(average.value, average.secondary_value, metric.unit),
        changeNote: metric.change_text || formatDifference(difference, metric.unit),
        assessment: metric.latest ? '已同步後端最新紀錄。' : '目前尚未有最新紀錄。',
        trendTone: toneForDifference(difference),
      }
    })
    .filter((card): card is NonNullable<typeof card> => card !== null)

  return cards.length ? cards : fallbackVitals
})

onMounted(async () => {
  await account.loadAccount()
  const recipientId = account.currentCareRecipientId
  if (!recipientId) return
  await Promise.all([loadDashboard(recipientId), scheduleStore.loadEntries(recipientId)])
})

async function loadDashboard(recipientId: number) {
  try {
    dashboard.value = await fetchVitalDashboard(recipientId)
  } catch {
    dashboard.value = null
  }
}

function formatMeasurement(value: number, secondaryValue: number | null, unit: string) {
  const main = Number.isInteger(value) ? String(value) : value.toFixed(1)
  const secondary =
    secondaryValue === null ? '' : `/${Number.isInteger(secondaryValue) ? secondaryValue : secondaryValue.toFixed(1)}`
  return `${main}${secondary}${unit === 'mmHg' ? '' : unit}`
}

function formatDifference(
  difference: { value: number | null; secondary_value: number | null } | null,
  unit: string,
) {
  if (!difference?.value) return '和前期差不多'
  const amount = Math.abs(difference.value)
  const sign = difference.value > 0 ? '上升' : '下降'
  return `${sign} ${Number.isInteger(amount) ? amount : amount.toFixed(1)} ${unit}`
}

function toneForDifference(difference: { value: number | null } | null) {
  if (!difference?.value) return 'neutral' as const
  return difference.value > 0 ? ('negative' as const) : ('positive' as const)
}

function formatDateTime(value: string) {
  return new Intl.DateTimeFormat('zh-TW', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

function openScheduleEditor(entry: ScheduleEntry) {
  editingSchedule.value = entry
  editDay.value = entry.day
  editHour.value = entry.hour
  editActivity.value = entry.activity
}

async function saveScheduleEdit() {
  if (!editingSchedule.value || !editActivity.value.trim()) return
  await scheduleStore.updateEntry(editingSchedule.value, {
    day: editDay.value,
    hour: editHour.value,
    activity: editActivity.value.trim(),
  })
  editingSchedule.value = null
}

async function deleteScheduleEntry(entry: ScheduleEntry) {
  if (!window.confirm('確定要刪除這筆排程嗎？')) return
  await scheduleStore.deleteEntry(entry)
  if (editingSchedule.value?.id === entry.id) {
    editingSchedule.value = null
  }
}
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
        @edit="openScheduleEditor"
        @delete="deleteScheduleEntry"
      />
    </div>

    <Teleport to="body">
      <div
        v-if="editingSchedule"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-6"
        @click.self="editingSchedule = null"
      >
        <div class="w-full max-w-xs space-y-4 rounded-2xl bg-white p-5 shadow-lg">
          <h2 class="text-base font-bold text-ink-950">{{ $t('編輯排程') }}</h2>

          <label class="block text-sm text-ink-700">
            <span class="mb-1 block">{{ $t('星期') }}</span>
            <select
              v-model="editDay"
              class="w-full rounded-xl border border-ink-400 px-3 py-2 text-ink-950"
            >
              <option value="mon">{{ $t('星期一') }}</option>
              <option value="tue">{{ $t('星期二') }}</option>
              <option value="wed">{{ $t('星期三') }}</option>
              <option value="thu">{{ $t('星期四') }}</option>
              <option value="fri">{{ $t('星期五') }}</option>
              <option value="sat">{{ $t('星期六') }}</option>
              <option value="sun">{{ $t('星期日') }}</option>
            </select>
          </label>

          <label class="block text-sm text-ink-700">
            <span class="mb-1 block">{{ $t('時間') }}</span>
            <select
              v-model.number="editHour"
              class="w-full rounded-xl border border-ink-400 px-3 py-2 text-ink-950"
            >
              <option v-for="hour in scheduleHours" :key="hour" :value="hour">
                {{ String(hour).padStart(2, '0') }}:00
              </option>
            </select>
          </label>

          <label class="block text-sm text-ink-700">
            <span class="mb-1 block">{{ $t('內容') }}</span>
            <input
              v-model="editActivity"
              class="w-full rounded-xl border border-ink-400 px-3 py-2 text-ink-950"
            />
          </label>

          <div class="grid grid-cols-2 gap-2">
            <button
              type="button"
              class="rounded-full border border-red-200 px-4 py-2 text-sm font-bold text-red-600"
              @click="deleteScheduleEntry(editingSchedule)"
            >
              {{ $t('刪除') }}
            </button>
            <button
              type="button"
              class="rounded-full bg-pink-500 px-4 py-2 text-sm font-bold text-white disabled:bg-ink-400"
              :disabled="scheduleStore.saving || !editActivity.trim()"
              @click="saveScheduleEdit"
            >
              {{ $t('儲存') }}
            </button>
          </div>
          <button
            type="button"
            class="w-full rounded-full border border-ink-500 px-4 py-2 text-sm font-bold text-ink-800"
            @click="editingSchedule = null"
          >
            {{ $t('取消') }}
          </button>
        </div>
      </div>
    </Teleport>

    <template v-if="view === 'schedule'" #fab
      ><FloatingAddButton @click="router.push('/dashboard/add-schedule')"
    /></template>
    <template #footer><BottomTabBar /></template>
  </PageContainer>
</template>
