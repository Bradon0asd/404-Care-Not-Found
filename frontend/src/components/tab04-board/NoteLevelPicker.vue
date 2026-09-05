<script setup lang="ts">
import NoteStackIcon from './NoteStackIcon.vue'
import type { NoteLevel } from '@/stores/board'

const level = defineModel<NoteLevel>({ required: true })

const options: { value: NoteLevel; label: string }[] = [
  { value: 'urgent', label: '緊急' },
  { value: 'normal', label: '普通' },
  { value: 'minor', label: '不重要' },
]
</script>

<template>
  <div class="flex justify-center gap-6">
    <button
      v-for="opt in options"
      :key="opt.value"
      type="button"
      class="flex flex-col items-center gap-1 rounded-xl p-2"
      :class="level === opt.value ? 'bg-ink-300' : ''"
      @click="level = opt.value"
    >
      <NoteStackIcon :level="opt.value" />
      <span class="text-xs font-medium text-ink-700">{{ $t(opt.label) }}</span>
    </button>
  </div>
</template>
