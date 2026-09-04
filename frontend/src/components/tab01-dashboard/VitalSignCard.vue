<script setup lang="ts">
defineProps<{
  label: string
  todayValue: string
  updatedAt: string
  weekAvgValue: string
  changeNote: string
  assessment: string
}>()
</script>

<template>
  <div class="rounded-2xl border-[3px] border-pink-400 bg-white p-4 text-xs">
    <div class="mb-3 flex justify-center">
      <h3 class="border-b-2 border-ink-950 pb-1 text-sm font-bold text-ink-950">{{ label }}</h3>
    </div>

    <p class="text-ink-700">
      今日{{ label }} <span class="text-base font-bold text-ink-950">{{ todayValue }}</span>
    </p>
    <p class="text-ink-500">更新於{{ updatedAt }}</p>

    <p class="mt-3 text-ink-700">
      過去一週平均{{ label }} <span class="text-base font-bold text-ink-950">{{ weekAvgValue }}</span>
    </p>
    <p class="text-ink-600">{{ changeNote }}</p>

    <p class="mt-3 text-ink-700">綜合評估</p>
    <p class="font-bold text-ink-950">{{ assessment }}</p>
  </div>
</template>
