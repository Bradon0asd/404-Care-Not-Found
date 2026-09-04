<script setup lang="ts">
import IconPencil from './icons/IconPencil.vue'

defineProps<{
  day: number
  highlighted: boolean
  align: 'left' | 'center' | 'right'
}>()

defineEmits<{ open: [] }>()
</script>

<template>
  <div
    class="flex flex-col items-center gap-1"
    :class="align === 'left' ? 'self-start' : align === 'right' ? 'self-end' : 'self-center'"
  >
    <button
      type="button"
      class="relative flex h-12 w-12 flex-col items-center justify-center rounded-full border text-[10px] leading-tight font-bold shadow-[inset_0_0_0_2px_white] after:absolute after:inset-[3px] after:rounded-full after:border after:border-ink-700"
      :class="highlighted ? 'border-ink-800 bg-accent text-ink-950' : 'border-ink-700 bg-white text-ink-700'"
      @click="$emit('open')"
    >
      <span class="text-[9px] font-normal">Day</span>
      {{ day }}
    </button>
    <button
      type="button"
      class="flex h-5 items-center gap-1 rounded-full border border-ink-400 bg-ink-100 px-2 text-[8px] font-medium text-ink-800"
      @click="$emit('open')"
    >
      <IconPencil class="h-2 w-2" />
      撰寫日記
    </button>
  </div>
</template>
