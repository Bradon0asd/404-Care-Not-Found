<script setup lang="ts">
import { ref } from 'vue'

withDefaults(
  defineProps<{
    message: string
    upgradeText?: string
    dismissible?: boolean
  }>(),
  { upgradeText: '', dismissible: true },
)

const dismissed = ref(false)
</script>

<template>
  <div
    v-if="!dismissed"
    class="mx-3 mt-3 flex items-center gap-2 rounded-xl bg-ink-200 px-3 py-2.5 text-xs text-ink-700"
  >
    <svg class="mt-0.5 h-3.5 w-3.5 shrink-0 text-pink-600" viewBox="0 0 24 24" fill="currentColor">
      <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.6" />
      <rect x="11" y="10" width="2" height="6" />
      <rect x="11" y="6.5" width="2" height="2" />
    </svg>
    <p class="flex-1">
      {{ message }}
      <RouterLink v-if="upgradeText" to="/account" class="font-bold text-blue-600 underline">{{
        upgradeText
      }}</RouterLink>
    </p>
    <button
      v-if="dismissible"
      type="button"
      class="flex h-6 w-6 shrink-0 items-center justify-center rounded-md bg-ink-400 text-ink-700"
      aria-label="關閉提示"
      @click="dismissed = true"
    >
      <svg
        class="h-3.5 w-3.5"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <path d="M6 6l12 12M18 6 6 18" stroke-linecap="round" />
      </svg>
    </button>
  </div>
</template>
