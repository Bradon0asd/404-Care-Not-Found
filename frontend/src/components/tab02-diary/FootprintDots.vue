<script setup lang="ts">
import IconFootprint from './icons/IconFootprint.vue'

defineProps<{ align: 'left' | 'center' | 'right' }>()
</script>

<template>
  <div
    class="flex items-center gap-1 text-ink-950"
    :class="align === 'left' ? 'self-start pl-14' : align === 'right' ? '-scale-x-100 self-end pr-14' : 'self-center'"
  >
    <IconFootprint class="h-3 w-3 -translate-y-0.5 rotate-12" />
    <IconFootprint class="h-3 w-3 translate-y-0.5 rotate-12" />
  </div>
</template>
