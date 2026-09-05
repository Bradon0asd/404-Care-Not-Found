<script setup lang="ts">
const value = defineModel<number>({ required: true })
</script>

<template>
  <div class="rounded-xl bg-ink-200 p-4">
    <h3 class="mb-1 text-sm font-bold text-ink-950">Temperature</h3>
    <p class="mb-3 text-xs text-ink-600">{{ $t('數值越低，AI 隨意生成比例越低（Min: 0）') }}</p>
    <div class="flex h-32 items-center justify-center">
      <input
        v-model.number="value"
        type="range"
        min="0"
        max="1"
        step="0.1"
        class="h-32 w-32 accent-pink-500"
        style="writing-mode: vertical-lr; direction: rtl"
      />
    </div>
    <p class="text-center text-sm font-bold text-ink-950">{{ $t(value) }}</p>
  </div>
</template>
