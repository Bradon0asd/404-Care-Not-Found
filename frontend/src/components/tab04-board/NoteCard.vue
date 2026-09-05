<script setup lang="ts">
import { computed } from 'vue'
import NoteStackIcon from './NoteStackIcon.vue'
import NoteMetaIcon from './NoteMetaIcon.vue'
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

const levelLabel = computed(
  () => ({ urgent: '緊急', normal: '普通', minor: '不重要' })[props.note.level],
)
</script>

<template>
  <button
    type="button"
    class="flex min-w-0 flex-col items-start gap-2 rounded-xl bg-ink-100 p-3 text-left"
    @click="$emit('click')"
  >
    <NoteStackIcon :level="note.level" class="mx-auto">
      <span class="px-2 text-center text-xs font-bold text-white">{{
        note.demo ? $t(note.tag) : note.tag
      }}</span>
    </NoteStackIcon>
    <p class="text-[11px] text-ink-600">{{ $t('目前狀態：') }}{{ $t(statusLabel) }}</p>
    <p class="flex w-full items-center gap-2 text-xs leading-5 text-ink-700">
      <NoteMetaIcon kind="title" />
      <span class="min-w-0 truncate"
        >{{ $t('標題：') }}{{ note.demo ? $t(note.title) : note.title }}</span
      >
    </p>
    <p class="flex items-center gap-2 text-xs leading-5 text-ink-700">
      <NoteMetaIcon kind="permission" />
      <span
        >{{ $t('權限：') }}{{ $t(note.visibility === 'employer' ? '你、雇主' : '只有你') }}</span
      >
    </p>
    <p class="flex items-center gap-2 text-xs leading-5 text-ink-700">
      <NoteMetaIcon kind="level" />
      <span>{{ $t('層級：') }}{{ $t(levelLabel) }}</span>
      <span v-if="note.level === 'urgent'">⚠</span>
    </p>
  </button>
</template>
