<script setup lang="ts">
import { computed } from 'vue'
import type { StickyNote } from '@/stores/board'

const props = defineProps<{ note: StickyNote | null }>()
defineEmits<{ close: [] }>()

const colorClass = computed(
  () =>
    ({
      urgent: 'bg-red-100',
      normal: 'bg-accent/30',
      minor: 'bg-sky-100',
    })[props.note?.level ?? 'normal'],
)

const statusLabel = computed(
  () =>
    ({
      read: '{雇主}已讀取',
      unread: '{雇主}尚未讀取',
      'no-access': '{雇主}未獲得瀏覽權限',
    })[props.note?.employerStatus ?? 'no-access'],
)

const levelLabel = computed(() => ({ urgent: '緊急', normal: '普通', minor: '不重要' })[props.note?.level ?? 'normal'])
</script>

<template>
  <Teleport to="body">
    <div v-if="note" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-8" @click.self="$emit('close')">
      <div class="relative w-full max-w-xs">
        <div class="absolute inset-0 translate-x-2 translate-y-2 rotate-3 rounded-lg opacity-60" :class="colorClass"></div>
        <div class="absolute inset-0 -translate-x-1 translate-y-1 -rotate-2 rounded-lg opacity-80" :class="colorClass"></div>
        <div class="relative space-y-3 rounded-lg p-5 text-sm text-ink-950 shadow-xl" :class="colorClass">
          <p><span class="font-bold">標題：</span>{{ note.title }}</p>
          <p><span class="font-bold">內容：</span>{{ note.content }}</p>
          <p class="text-xs text-ink-700">目前狀態：{{ statusLabel }}</p>
          <p class="text-xs text-ink-700">權限：{{ note.visibility === 'employer' ? '你、雇主' : '只有你' }}</p>
          <p class="text-xs text-ink-700">層級：{{ levelLabel }}</p>
        </div>
      </div>
    </div>
  </Teleport>
</template>
