<script setup lang="ts">
import { computed } from 'vue'
import type { NoteLevel } from '@/stores/board'

const props = defineProps<{ level: NoteLevel }>()

const colorClass = computed(
  () =>
    ({
      urgent: 'bg-red-500',
      normal: 'bg-accent',
      minor: 'bg-sky-400',
    })[props.level],
)
</script>

<template>
  <div class="relative h-16 w-16">
    <div class="absolute inset-0 rotate-6 rounded-md opacity-40" :class="colorClass"></div>
    <div class="absolute inset-0 -rotate-3 rounded-md opacity-70" :class="colorClass"></div>
    <div class="absolute inset-0 flex items-center justify-center rounded-md shadow-sm" :class="colorClass">
      <slot />
    </div>
  </div>
</template>
