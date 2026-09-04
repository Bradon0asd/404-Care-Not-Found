<script setup lang="ts">
import IconPencil from './icons/IconPencil.vue'

defineProps<{
  day: number
  highlighted: boolean
  align: 'left' | 'right'
}>()

defineEmits<{ open: [] }>()
</script>

<template>
  <div class="flex flex-col items-center gap-1" :class="align === 'left' ? 'self-start' : 'self-end'">
    <button
      type="button"
      class="flex h-16 w-16 flex-col items-center justify-center rounded-full border-2 text-sm font-bold"
      :class="highlighted ? 'border-accent bg-accent text-ink-950' : 'border-ink-500 bg-white text-ink-700'"
      @click="$emit('open')"
    >
      <span class="text-[10px] font-normal">Day</span>
      {{ day }}
    </button>
    <button
      type="button"
      class="flex items-center gap-1 rounded-full border border-ink-400 bg-white px-3 py-1 text-[11px] text-ink-700"
      @click="$emit('open')"
    >
      <IconPencil class="h-3 w-3" />
      撰寫日記
    </button>
  </div>
</template>
