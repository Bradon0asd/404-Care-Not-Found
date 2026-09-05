<script setup lang="ts">
defineProps<{ current: 1 | 2 }>()
</script>

<template>
  <div class="flex items-center justify-center gap-2 py-4">
    <span
      class="flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold text-white"
      :class="current >= 1 ? 'bg-green-600' : 'bg-ink-400'"
      >1</span
    >
    <span class="h-px w-16 border-t-2 border-dashed border-ink-400"></span>
    <span
      class="flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold text-white"
      :class="current >= 2 ? 'bg-green-600' : 'bg-ink-400'"
      >2</span
    >
  </div>
</template>
