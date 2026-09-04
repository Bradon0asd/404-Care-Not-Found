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
    :class="variant === 'chip' ? 'gap-3' : 'rounded-full border border-ink-400 p-1'"
  >
    <button
      v-for="option in options"
      :key="option.value"
      type="button"
      class="flex-1 rounded-full py-2 text-sm font-bold transition-colors"
      :class="
        variant === 'chip'
          ? option.value === modelValue
            ? 'bg-accent text-ink-950'
            : 'border border-ink-400 bg-white text-ink-700'
          : option.value === modelValue
            ? 'bg-pink-500 text-white'
            : 'text-pink-500'
      "
      @click="$emit('update:modelValue', option.value)"
    >
      {{ option.label }}
    </button>
  </div>
</template>
