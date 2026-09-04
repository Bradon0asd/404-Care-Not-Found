<script setup lang="ts">
withDefaults(
  defineProps<{
    subtitle?: string
  }>(),
  {
    subtitle: '照見：照護被看見',
  },
)
</script>

<template>
  <header class="flex items-center gap-2 bg-pink-300 px-4 py-3">
    <svg class="h-5 w-5 shrink-0 text-ink-950" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path
        d="M12 21s-6.716-4.35-9.428-8.28C.86 10.02 1.2 6.6 3.6 4.8c2.1-1.58 4.86-1.1 6.4.9L12 7.8l2-2.1c1.54-2 4.3-2.48 6.4-.9 2.4 1.8 2.74 5.22 1.03 7.92C18.72 16.65 12 21 12 21z"
      />
    </svg>
    <span class="text-sm font-bold text-ink-950">404: Care Can Be Found</span>
    <span class="text-xs text-ink-700">{{ subtitle }}</span>
  </header>
</template>
