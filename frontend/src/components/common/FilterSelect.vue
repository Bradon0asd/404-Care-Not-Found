<script setup lang="ts">
defineProps<{
  label: string
  options: { value: string; label: string }[]
}>()

const value = defineModel<string>({ required: true })
</script>

<template>
  <label class="flex items-center gap-1 text-sm text-ink-700">
    {{ label }}
    <select v-model="value" class="bg-transparent font-medium text-ink-950">
      <option value="">篩選{{ label }}</option>
      <option v-for="opt in options" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
    </select>
  </label>
</template>
