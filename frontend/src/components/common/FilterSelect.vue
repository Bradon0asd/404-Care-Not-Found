<script setup lang="ts">
defineProps<{
  label: string
  options: { value: string; label: string }[]
}>()

const value = defineModel<string>({ required: true })
</script>

<template>
  <label class="flex items-center gap-1 text-sm text-ink-700">
    {{ $t(label) }}
    <select v-model="value" class="bg-transparent font-medium text-ink-950">
      <option value="">{{ $t('篩選') }}{{ $t(label) }}</option>
      <option v-for="opt in options" :key="opt.value" :value="opt.value">
        {{ $t(opt.label) }}
      </option>
    </select>
  </label>
</template>
