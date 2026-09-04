<script setup lang="ts">
defineProps<{
  arrivalDay: number
  careRecipientCount: number
}>()
</script>

<template>
  <div class="mx-4 mt-2 flex items-center justify-center gap-3 rounded-xl border border-ink-400 bg-white px-3 py-1.5 text-center text-[11px] text-ink-700 shadow-sm">
    <p>
      這是我來臺灣的第 <span class="text-base font-bold text-ink-950">{{ arrivalDay }}</span> 天
    </p>
    <span class="h-4 w-px bg-ink-400"></span>
    <p>
      這是我照顧的第 <span class="text-base font-bold text-ink-950">{{ careRecipientCount }}</span> 個人
    </p>
  </div>
</template>
