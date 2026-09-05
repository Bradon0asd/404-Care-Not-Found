<script setup lang="ts">
withDefaults(defineProps<{ filled?: boolean }>(), { filled: false })
</script>

<template>
  <svg viewBox="0 0 24 24" :fill="filled ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="1.6">
    <circle cx="8" cy="8" r="3.5" />
    <path d="M8 2.5v1.5M13.5 8H12M3.6 4.6l1 1M12.4 4.6l-1 1" stroke-linecap="round" />
    <path
      d="M7 19h9.5a3.5 3.5 0 0 0 .5-6.96A5 5 0 0 0 7.5 13.2 3 3 0 0 0 7 19Z"
      stroke-linejoin="round"
    />
  </svg>
</template>
