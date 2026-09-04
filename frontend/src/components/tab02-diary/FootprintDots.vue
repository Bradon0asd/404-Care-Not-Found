<script setup lang="ts">
defineProps<{ align: 'left' | 'right' }>()
</script>

<template>
  <div
    class="flex items-center gap-2 py-1 text-ink-500"
    :class="align === 'left' ? 'self-end pr-6' : 'self-start pl-6'"
  >
    <span v-for="i in 3" :key="i" class="h-1.5 w-1.5 rounded-full bg-ink-400" :style="{ opacity: 0.4 + i * 0.2 }" />
  </div>
</template>
