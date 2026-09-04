<script setup lang="ts">
defineEmits<{ click: [] }>()
</script>

<template>
  <button
    type="button"
    class="flex shrink-0 items-center gap-1 rounded-full bg-pink-500 px-3 py-1.5 text-xs font-bold text-white"
    @click="$emit('click')"
  >
    <svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
      <rect x="9" y="3" width="6" height="11" rx="3" />
      <path d="M5 11a7 7 0 0 0 14 0M12 18v3" stroke-linecap="round" />
    </svg>
    AI 語音辨識
    <svg class="h-3 w-3" viewBox="0 0 24 24" fill="currentColor">
      <path d="m12 2 2.4 7.4H22l-6.2 4.5 2.4 7.4L12 16.8l-6.2 4.5 2.4-7.4L2 9.4h7.6z" />
    </svg>
  </button>
</template>
