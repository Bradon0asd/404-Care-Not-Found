<script setup lang="ts">
defineProps<{
  label: string
  todayValue: string
  updatedAt: string
  weekAvgValue: string
  changeNote: string
  assessment: string
  trendTone?: 'positive' | 'negative' | 'neutral'
}>()
</script>

<template>
  <article
    class="rounded-[20px] border border-pink-300 bg-pink-100/15 px-3.5 py-3 text-xs shadow-[0_2px_8px_rgba(45,45,45,0.08)]"
  >
    <div class="mb-2 flex justify-center">
      <h3 class="border-b border-ink-800 px-3 pb-0.5 text-sm font-bold text-ink-950">
        {{ label }}
      </h3>
    </div>

    <p class="flex items-baseline gap-1.5 text-ink-600">
      <span>今日{{ label }}</span>
      <strong class="text-lg leading-none text-ink-950">{{ todayValue }}</strong>
    </p>
    <p class="mt-1 text-[9px] text-ink-500">更新於 {{ updatedAt }}</p>

    <p class="mt-2.5 flex items-baseline gap-1.5 text-ink-600">
      <span>過去一週平均</span> <strong class="text-base text-ink-950">{{ weekAvgValue }}</strong>
    </p>
    <p
      class="mt-1 text-[10px] font-medium"
      :class="
        trendTone === 'negative'
          ? 'text-red-500'
          : trendTone === 'neutral'
            ? 'text-ink-600'
            : 'text-green-600'
      "
    >
      {{ changeNote }}
    </p>

    <div class="mt-2.5 border-t border-ink-300/80 pt-2">
      <p class="text-ink-600">綜合評估</p>
      <p class="mt-0.5 font-medium leading-relaxed text-ink-900">{{ assessment }}</p>
    </div>
  </article>
</template>
