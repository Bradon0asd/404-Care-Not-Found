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
  <div class="rounded-xl bg-ink-200 p-3 text-xs">
    <h3 class="mb-2 text-sm font-bold text-ink-950">{{ label }}</h3>

    <p class="text-ink-700">
      今日{{ label }} <span class="text-sm font-bold text-ink-950">{{ todayValue }}</span>
    </p>
    <p class="text-ink-600">更新於{{ updatedAt }}</p>

    <p class="mt-2 text-ink-700">
      過去一週平均{{ label }} <span class="font-bold text-ink-950">{{ weekAvgValue }}</span>
    </p>
    <p class="text-ink-600">{{ changeNote }}</p>

    <p class="mt-2 font-bold text-ink-700">綜合評估</p>
    <p class="text-ink-600">{{ assessment }}</p>
  </div>
</template>
