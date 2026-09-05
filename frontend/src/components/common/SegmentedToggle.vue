<script setup lang="ts">
defineProps<{
  options: { value: string; label: string }[]
  modelValue: string
  variant?: 'tab' | 'chip'
}>()

defineEmits<{ 'update:modelValue': [string] }>()
</script>

<template>
  <div
    class="flex gap-1"
    :class="variant === 'chip' ? 'gap-0 rounded-full bg-accent p-1' : 'rounded-xl bg-pink-200 p-1'"
  >
    <button
      v-for="option in options"
      :key="option.value"
      type="button"
      class="flex-1 rounded-full py-2 text-sm font-bold transition-colors"
      :class="
        variant === 'chip'
          ? option.value === modelValue
            ? 'bg-white text-ink-950 shadow-sm'
            : 'text-ink-950'
          : option.value === modelValue
            ? 'bg-pink-500 text-white'
            : 'text-ink-950'
      "
      @click="$emit('update:modelValue', option.value)"
    >
      {{ $t(option.label) }}
    </button>
  </div>
</template>
