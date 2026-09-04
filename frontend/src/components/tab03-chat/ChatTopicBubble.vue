<script setup lang="ts">
defineProps<{ title: string; align: 'left' | 'right' }>()
defineEmits<{ click: [] }>()
</script>

<template>
  <button
    type="button"
    class="relative max-w-[65%] rounded-2xl bg-blue-600 px-4 py-2.5 text-left text-sm font-medium text-white shadow"
    :class="align === 'left' ? 'self-start rounded-bl-sm' : 'self-end rounded-br-sm'"
    @click="$emit('click')"
  >
    {{ title }}
  </button>
</template>
