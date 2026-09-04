<script setup lang="ts">
import { ref } from 'vue'

withDefaults(defineProps<{ message?: string }>(), {
  message: '此功能「不」涉及任何醫療診斷，僅供照護日常紀錄',
})

const dismissed = ref(false)
</script>

<template>
  <div v-if="!dismissed" class="flex items-start gap-2 bg-red-600 px-4 py-2 text-xs text-white">
    <svg class="mt-0.5 h-3.5 w-3.5 shrink-0" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2 1 21h22L12 2Zm0 5 7.5 12h-15L12 7Z" />
      <rect x="11" y="10" width="2" height="5" fill="white" />
      <rect x="11" y="16" width="2" height="2" fill="white" />
    </svg>
    <p class="flex-1">{{ message }}</p>
    <button type="button" class="shrink-0" aria-label="關閉提示" @click="dismissed = true">
      <svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M6 6l12 12M18 6 6 18" stroke-linecap="round" />
      </svg>
    </button>
  </div>
</template>
