<script setup lang="ts">
withDefaults(defineProps<{ filled?: boolean }>(), { filled: false })
</script>

<template>
  <svg viewBox="0 0 24 24" :fill="filled ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="1.6">
    <path
      d="M6 15h12a4 4 0 0 0 .6-7.95A5.5 5.5 0 0 0 8 5.6 3.5 3.5 0 0 0 6 15Z"
      stroke-linejoin="round"
    />
    <path d="M8 18.5 7 21M12.5 18.5l-1 2.5M17 18.5l-1 2.5" stroke-linecap="round" />
  </svg>
</template>
