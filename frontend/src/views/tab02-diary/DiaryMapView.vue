<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'
import DiaryStatsBar from '@/components/tab02-diary/DiaryStatsBar.vue'
import DiaryDayBubble from '@/components/tab02-diary/DiaryDayBubble.vue'
import IconFootprint from '@/components/tab02-diary/icons/IconFootprint.vue'
import BackgroundBlobs from '@/components/common/BackgroundBlobs.vue'
import { useDiaryStore } from '@/stores/diary'

const router = useRouter()
const diaryStore = useDiaryStore()
const dayPositions = [20, 80, 50, 20, 50, 80, 20]

function pathTop(progress: number) {
  return `calc(${progress * 100}% + ${36 - progress * 72}px)`
}

// The path climbs from today at the bottom toward the upcoming days.
const days = computed(() =>
  Array.from({ length: 7 }, (_, i) => diaryStore.arrivalDay + 6 - i).map((day, i) => ({
    day,
    x: dayPositions[i]!,
    top: pathTop(i / 6),
  })),
)

const footsteps = computed(() =>
  days.value.slice(0, -1).map((item, i) => ({
    x: (item.x + days.value[i + 1]!.x) / 2,
    top: pathTop((i + 0.5) / 6),
    angle: Math.sign(item.x - days.value[i + 1]!.x) * 55,
  })),
)

function openDay(day: number) {
  router.push(`/diary/${day}`)
}
</script>

<template>
  <PageContainer>
    <template #header><AppHeader /></template>

    <div class="relative isolate flex min-h-0 flex-1 flex-col">
      <BackgroundBlobs />
      <DiaryStatsBar
        :arrival-day="diaryStore.arrivalDay"
        :care-recipient-count="diaryStore.careRecipientCount"
      />
      <p class="mt-2 shrink-0 px-6 text-center text-[10px] text-ink-600">
        {{ $t('每天撰寫日記，累積一定天數將獲得特定獎勵') }}
      </p>

      <div class="relative mx-4 my-2 min-h-[280px] flex-1">
        <div
          v-for="item in days"
          :key="item.day"
          class="absolute w-[76px] -translate-x-1/2 -translate-y-1/2"
          :style="{ left: `${item.x}%`, top: item.top }"
        >
          <DiaryDayBubble
            :day="item.day"
            align="center"
            :highlighted="item.day === diaryStore.arrivalDay"
            @open="openDay(item.day)"
          />
        </div>
        <div
          v-for="(step, i) in footsteps"
          :key="i"
          aria-hidden="true"
          class="pointer-events-none absolute text-ink-800"
          :style="{ left: `${step.x}%`, top: step.top, transform: `rotate(${step.angle}deg)` }"
        >
          <IconFootprint class="absolute -top-1 -left-3 h-4 w-3 -rotate-6" />
          <IconFootprint class="absolute -top-3 left-0.5 h-4 w-3 scale-x-[-1] rotate-6" />
        </div>
      </div>
    </div>

    <template #footer><BottomTabBar /></template>
  </PageContainer>
</template>
