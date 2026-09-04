<script setup lang="ts">
import { computed } from 'vue'
import NoteStackIcon from './NoteStackIcon.vue'
import type { StickyNote } from '@/stores/board'

const props = defineProps<{ note: StickyNote }>()
defineEmits<{ click: [] }>()

const statusLabel = computed(
  () =>
    ({
      read: '{雇主}已讀取',
      unread: '{雇主}尚未讀取',
      'no-access': '{雇主}未獲得瀏覽權限',
    })[props.note.employerStatus],
)

const levelLabel = computed(() => ({ urgent: '緊急', normal: '普通', minor: '不重要' })[props.note.level])
</script>

<template>
  <button type="button" class="flex flex-col items-start gap-2 rounded-xl bg-ink-100 p-3 text-left" @click="$emit('click')">
    <NoteStackIcon :level="note.level" class="mx-auto">
      <span class="px-2 text-center text-xs font-bold text-white">{{ note.tag }}</span>
    </NoteStackIcon>
    <p class="text-[11px] text-ink-600">目前狀態：{{ statusLabel }}</p>
    <p class="w-full truncate text-xs text-ink-700">🏷 標題：{{ note.title }}</p>
    <p class="text-xs text-ink-700">👤 權限：{{ note.visibility === 'employer' ? '你、雇主' : '只有你' }}</p>
    <p class="flex items-center gap-1 text-xs text-ink-700">
      ☰ 層級：{{ levelLabel }}
      <span v-if="note.level === 'urgent'">⚠</span>
    </p>
  </button>
</template>
