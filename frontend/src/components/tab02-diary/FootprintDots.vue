<script setup lang="ts">
import IconFootprint from './icons/IconFootprint.vue'

defineProps<{ align: 'left' | 'right' }>()
</script>

<template>
  <div
    class="flex items-center gap-0.5 text-ink-800"
    :class="align === 'left' ? '-scale-x-100 self-end pr-8' : 'self-start pl-8'"
  >
    <IconFootprint class="h-2.5 w-2.5 -translate-y-0.5" />
    <IconFootprint class="h-2.5 w-2.5 translate-y-0.5" />
  </div>
</template>
