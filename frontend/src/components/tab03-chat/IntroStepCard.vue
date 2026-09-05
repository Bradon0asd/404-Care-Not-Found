<script setup lang="ts">
defineProps<{ number: number }>()
</script>

<template>
  <div class="flex gap-3">
    <span
      class="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-ink-800 text-xs font-bold text-white"
    >
      {{ $t(number) }}
    </span>
    <div class="flex-1 space-y-2 text-sm text-ink-700">
      <slot />
    </div>
  </div>
</template>
