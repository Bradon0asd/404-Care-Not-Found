<script setup lang="ts">
defineProps<{
  arrivalDay: number
  careRecipientCount: number
}>()
</script>

<template>
  <div
    class="mx-6 mt-3 flex h-12 shrink-0 items-center justify-center gap-3 rounded-lg border border-ink-500 bg-white px-3 text-center text-[10px] text-ink-600 shadow-[0_2px_2px_rgba(0,0,0,0.18)]"
  >
    <p>
      {{ $t('這是我來臺灣的第') }}
      <span class="text-xl font-medium text-ink-950">{{ arrivalDay }}</span> {{ $t('天') }}
    </p>
    <span class="h-7 w-px bg-ink-400"></span>
    <p>
      {{ $t('這是我照顧的第') }}
      <span class="text-xl font-medium text-ink-950">{{ careRecipientCount }}</span>
      {{ $t('個人') }}
    </p>
  </div>
</template>
