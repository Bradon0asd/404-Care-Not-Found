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

// Newest day first, today (arrivalDay) highlighted; path renders bottom-up visually via column-reverse.
const days = computed(() =>
  Array.from({ length: 7 }, (_, i) => diaryStore.arrivalDay + 6 - i).map((day, i) => ({
    day,
    align: (i % 2 === 0 ? 'right' : 'left') as 'left' | 'right',
  })),
)

function openDay(day: number) {
  router.push(`/diary/${day}`)
}
</script>

<template>
  <PageContainer>
    <template #header><AppHeader /></template>

    <DiaryStatsBar :arrival-day="diaryStore.arrivalDay" :care-recipient-count="diaryStore.careRecipientCount" />
    <p class="mt-1 px-6 text-center text-[10px] text-pink-600">每天撰寫日記，累積一定天數將獲得特定獎勵</p>

    <div class="relative flex min-h-0 flex-1 flex-col justify-between px-6 py-1">
      <BackgroundBlobs />
      <template v-for="(item, i) in days" :key="item.day">
        <DiaryDayBubble
          class="relative z-10"
          :day="item.day"
          :align="item.align"
          :highlighted="item.day === diaryStore.arrivalDay"
          @open="openDay(item.day)"
        />
        <FootprintDots v-if="i < days.length - 1" class="relative z-10" :align="item.align" />
      </template>
    </div>

    <template #footer><BottomTabBar /></template>
  </PageContainer>
</template>
