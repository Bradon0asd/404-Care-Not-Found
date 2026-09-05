<script setup lang="ts">
import { ref } from 'vue'
import BaseButton from '@/components/common/BaseButton.vue'

const props = defineProps<{
  open: boolean
  inviteLink: string
}>()

defineEmits<{ close: [] }>()

const copied = ref(false)

async function copyLink() {
  await navigator.clipboard.writeText(props.inviteLink)
  copied.value = true
  setTimeout(() => (copied.value = false), 2000)
}
</script>

<template>
  <Teleport to="body">
    <div
      v-if="open"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-6"
      @click.self="$emit('close')"
    >
      <div class="w-full max-w-xs rounded-2xl bg-white p-5 shadow-lg">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-sm font-bold text-ink-950">{{ $t('動態邀請碼') }}</h2>
          <button
            type="button"
            class="text-ink-600"
            @click="$emit('close')"
            :aria-label="$t('關閉')"
          >
            <svg
              class="h-5 w-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M6 6l12 12M18 6 6 18" stroke-linecap="round" />
            </svg>
          </button>
        </div>

        <div class="mb-4 flex items-center gap-2 rounded-full border border-ink-400 px-4 py-3">
          <svg
            class="h-4 w-4 shrink-0 text-ink-600"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M10 13a5 5 0 0 0 7 0l2-2a5 5 0 0 0-7-7l-1 1M14 11a5 5 0 0 0-7 0l-2 2a5 5 0 0 0 7 7l1-1"
            />
          </svg>
          <span class="truncate text-xs text-ink-700">{{ $t(inviteLink) }}</span>
        </div>

        <BaseButton variant="primary" @click="copyLink">{{
          $t(copied ? '已複製' : '複製邀請碼')
        }}</BaseButton>
      </div>
    </div>
  </Teleport>
</template>
