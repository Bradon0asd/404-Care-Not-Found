<script setup lang="ts">
defineProps<{
  arrivalDay: number
  careRecipientCount: number
}>()
</script>

<template>
  <div class="mx-4 mt-4 flex items-center justify-center gap-4 rounded-xl bg-ink-200 px-4 py-3 text-center text-xs text-ink-700">
    <p>
      這是我來臺灣的第 <span class="text-lg font-bold text-ink-950">{{ arrivalDay }}</span> 天
    </p>
    <span class="h-6 w-px bg-ink-400"></span>
    <p>
      這是我照顧的第 <span class="text-lg font-bold text-ink-950">{{ careRecipientCount }}</span> 個人
    </p>
  </div>
</template>
