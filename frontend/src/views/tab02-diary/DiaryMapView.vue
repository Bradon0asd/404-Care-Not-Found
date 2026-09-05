<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'
import DiaryStatsBar from '@/components/tab02-diary/DiaryStatsBar.vue'
import DiaryDayBubble from '@/components/tab02-diary/DiaryDayBubble.vue'
import FootprintDots from '@/components/tab02-diary/FootprintDots.vue'
import BackgroundBlobs from '@/components/common/BackgroundBlobs.vue'
import { useDiaryStore } from '@/stores/diary'

const router = useRouter()
const diaryStore = useDiaryStore()
const dayAlignments = ['left', 'right', 'center', 'left', 'center', 'right', 'left'] as const

// The path climbs from today at the bottom toward the upcoming days.
const days = computed(() =>
  Array.from({ length: 7 }, (_, i) => diaryStore.arrivalDay + 6 - i).map((day, i) => ({
    day,
    align: dayAlignments[i]!,
  })),
)

function openDay(day: number) {
  router.push(`/diary/${day}`)
}
</script>

<template>
  <PageContainer>
    <template #header><AppHeader /></template>

    <div class="relative isolate flex flex-1 flex-col">
      <BackgroundBlobs />
      <DiaryStatsBar
        :arrival-day="diaryStore.arrivalDay"
        :care-recipient-count="diaryStore.careRecipientCount"
      />
      <p class="mt-3 px-6 text-center text-[10px] text-ink-600">
        每天撰寫日記，累積一定天數將獲得特定獎勵
      </p>

      <div class="flex flex-1 flex-col justify-between gap-1 px-8 py-6">
        <template v-for="(item, i) in days" :key="item.day">
          <DiaryDayBubble
            class="relative shrink-0"
            :day="item.day"
            :align="item.align"
            :highlighted="item.day === diaryStore.arrivalDay"
            @open="openDay(item.day)"
          />
          <FootprintDots v-if="i < days.length - 1" :from="days[i + 1]!.align" :to="item.align" />
        </template>
      </div>
    </div>

    <template #footer><BottomTabBar /></template>
  </PageContainer>
</template>
