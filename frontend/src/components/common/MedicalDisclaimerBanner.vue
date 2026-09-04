<script setup lang="ts">
import { ref } from 'vue'

withDefaults(
  defineProps<{
    before?: string
    highlight?: string
    after?: string
  }>(),
  {
    before: '此功能',
    highlight: '不',
    after: '涉及任何醫療診斷，僅供照護日常紀錄',
  },
)

const dismissed = ref(false)
</script>

<template>
  <div v-if="!dismissed" class="mx-3 mt-3 flex items-center gap-2 rounded-xl bg-ink-200 px-3 py-2.5 text-xs">
    <span class="flex h-4 w-4 shrink-0 items-center justify-center rounded-full bg-red-600 text-[10px] font-bold text-white">
      i
    </span>
    <p class="flex-1 font-bold text-ink-950">
      {{ before }}「<span class="text-red-600">{{ highlight }}</span
      >」{{ after }}
    </p>
    <button
      type="button"
      class="flex h-6 w-6 shrink-0 items-center justify-center rounded-md bg-ink-400 text-ink-700"
      aria-label="關閉提示"
      @click="dismissed = true"
    >
      <svg class="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <path d="M6 6l12 12M18 6 6 18" stroke-linecap="round" />
      </svg>
    </button>
  </div>
</template>
