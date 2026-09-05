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
  <header class="flex shrink-0 items-center gap-2 bg-pink-500 px-4 py-3">
    <svg class="h-6 w-6 shrink-0" viewBox="0 0 28 28" fill="none" aria-hidden="true">
      <path d="m16 9 8-6 1 11Z" fill="#fff3c4" />
      <g transform="rotate(40 14 14)" stroke="#594b48" stroke-width="1.5" stroke-linejoin="round">
        <path d="M9 6h10v5l-2 3v10h-6V14l-2-3Z" fill="#fffaf2" />
        <path d="M9 9h10M13 16h2v3h-2Z" />
      </g>
    </svg>
    <span class="shrink-0 text-xs font-bold whitespace-nowrap text-ink-950 min-[380px]:text-sm"
      >404: Care Can Be Found</span
    >
    <span class="min-w-0 text-[10px] leading-tight text-white min-[380px]:text-xs">{{
      subtitle
    }}</span>
  </header>
</template>
