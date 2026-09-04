<script setup lang="ts">
defineProps<{ label: string; accent?: boolean }>()
defineEmits<{ click: [] }>()
</script>

<template>
  <button type="button" class="flex items-center gap-2" @click="$emit('click')">
    <svg
      class="h-6 w-6"
      :class="accent ? 'text-accent' : 'text-ink-800'"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="1.8"
    >
      <path d="M3 21c6-1 8-4 8-9V3M11 12l7-7" stroke-linecap="round" stroke-linejoin="round" />
    </svg>
    <span class="text-sm font-bold" :class="accent ? 'text-ink-950' : 'text-ink-800'">{{ label }}</span>
  </button>
</template>
