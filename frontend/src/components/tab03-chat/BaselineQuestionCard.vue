<script setup lang="ts">
defineProps<{
  index: number
  question: string
  options: string[]
}>()

const selected = defineModel<number | null>({ default: null })
</script>

<template>
  <div class="rounded-xl bg-ink-200 p-4">
    <p class="mb-4 text-sm text-ink-950">{{ $t('題目') }} {{ index }}：{{ $t(question) }}</p>
    <div class="space-y-3">
      <button
        v-for="(option, i) in options"
        :key="option"
        type="button"
        class="w-full rounded-full border py-2.5 text-sm font-medium transition-colors"
        :class="
          selected === i
            ? 'border-pink-500 bg-pink-500 text-white'
            : 'border-ink-500 bg-white text-ink-700'
        "
        @click="selected = i"
      >
        {{ $t(option) }}
      </button>
    </div>
  </div>
</template>
