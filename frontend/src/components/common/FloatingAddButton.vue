<script setup lang="ts">
defineEmits<{ click: [] }>()
</script>

<template>
  <button
    type="button"
    class="absolute right-4 bottom-24 flex h-12 w-12 items-center justify-center rounded-full bg-pink-500 text-white shadow-lg"
    aria-label="新增"
    @click="$emit('click')"
  >
    <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8l-5-5Z" stroke-linejoin="round" />
      <path d="M12 12v6M9 15h6" stroke-linecap="round" />
    </svg>
  </button>
</template>
