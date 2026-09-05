<script setup lang="ts">
import { computed } from 'vue'
import type { StickyNote } from '@/stores/board'
import { useAccountStore } from '@/stores/account'

const account = useAccountStore()

const props = defineProps<{ note: StickyNote | null }>()
defineEmits<{ close: [] }>()

const colorClass = computed(
  () =>
    ({
      urgent: 'bg-red-100',
      normal: 'bg-accent',
      minor: 'bg-sky-100',
    })[props.note?.level ?? 'normal'],
)

const statusLabel = computed(
  () =>
    ({
      read: '{name}已讀取',
      unread: '{name}尚未讀取',
      'no-access': '{name}未獲得瀏覽權限',
    })[props.note?.employerStatus ?? 'no-access'],
)

const levelLabel = computed(
  () => ({ urgent: '緊急', normal: '普通', minor: '不重要' })[props.note?.level ?? 'normal'],
)
</script>

<template>
  <Teleport to="body">
    <div
      v-if="note"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-8"
      @click.self="$emit('close')"
    >
      <div class="relative w-full max-w-xs">
        <div
          class="absolute inset-0 translate-x-2 translate-y-2 rotate-3 rounded-lg opacity-60"
          :class="colorClass"
        ></div>
        <div
          class="absolute inset-0 -translate-x-1 translate-y-1 -rotate-2 rounded-lg opacity-80"
          :class="colorClass"
        ></div>
        <div
          class="relative space-y-3 rounded-lg p-5 text-sm text-ink-950 shadow-xl"
          :class="colorClass"
        >
          <p>
            <span class="font-bold">{{ $t('標題：') }}</span
            >{{ note.demo ? $t(note.title) : note.title }}
          </p>
          <p>
            <span class="font-bold">{{ $t('內容：') }}</span
            >{{ note.demo ? $t(note.content) : note.content }}
          </p>
          <p class="text-xs text-ink-700">
            {{ $t('目前狀態：') }}{{ $t(statusLabel, { name: account.employer.name }) }}
          </p>
          <p class="text-xs text-ink-700">
            {{ $t('權限：')
            }}{{
              $t(note.visibility === 'employer' ? '你、{name}' : '只有你', {
                name: account.employer.name,
              })
            }}
          </p>
          <p class="text-xs text-ink-700">{{ $t('層級：') }}{{ $t(levelLabel) }}</p>
        </div>
      </div>
    </div>
  </Teleport>
</template>
