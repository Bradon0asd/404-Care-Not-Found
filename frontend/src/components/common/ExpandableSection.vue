<script setup lang="ts">
import { ref } from 'vue'

defineProps<{ title: string }>()

const open = ref(false)
</script>

<template>
  <div class="rounded-xl bg-ink-200">
    <button
      type="button"
      class="flex w-full items-center justify-between px-4 py-4 text-sm font-medium text-ink-700"
      @click="open = !open"
    >
      {{ title }}
      <svg
        class="h-4 w-4 shrink-0 text-ink-600 transition-transform"
        :class="{ 'rotate-180': open }"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <path d="m6 9 6 6 6-6" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
    </button>
    <div v-if="open" class="border-t border-ink-400 px-4 py-4 text-sm text-ink-600">
      <slot>
        <p>欄位設計中</p>
      </slot>
    </div>
  </div>
</template>
