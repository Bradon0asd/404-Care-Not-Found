<script setup lang="ts">
withDefaults(defineProps<{ filled?: boolean }>(), { filled: false })
</script>

<template>
  <svg viewBox="0 0 24 24" :fill="filled ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="1.6">
    <circle cx="12" cy="12" r="4.5" />
    <path
      d="M12 2v2.5M12 19.5V22M4.2 4.2l1.8 1.8M18 18l1.8 1.8M2 12h2.5M19.5 12H22M4.2 19.8 6 18M18 6l1.8-1.8"
      stroke-linecap="round"
    />
  </svg>
</template>
