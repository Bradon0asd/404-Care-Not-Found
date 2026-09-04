<script setup lang="ts">
defineProps<{
  label: string
  selected: boolean
}>()

defineEmits<{ select: [] }>()
</script>

<template>
  <button
    type="button"
    class="flex w-36 flex-col items-center gap-3 rounded-2xl px-4 py-6 transition-colors"
    :class="selected ? 'bg-accent text-white' : 'bg-ink-300 text-pink-600'"
    @click="$emit('select')"
  >
    <span class="[&>svg]:h-10 [&>svg]:w-10" :class="selected ? 'text-white' : 'text-pink-600'">
      <slot name="icon" />
    </span>
    <span class="text-sm font-bold" :class="selected ? 'text-white' : 'text-ink-700'">{{ label }}</span>
  </button>
</template>
