<script setup lang="ts">
defineEmits<{ click: [] }>()
</script>

<template>
  <button
    type="button"
    aria-label="開新聊天"
    class="relative flex h-48 w-48 items-center justify-center rounded-full shadow-lg"
    style="
      background: radial-gradient(
        circle at 35% 30%,
        #fff 0%,
        #ffe3ec 25%,
        #dff2ff 50%,
        #fff6d9 75%,
        #ffe3ec 100%
      );
    "
    @click="$emit('click')"
  >
    <svg class="h-10 w-10 text-ink-700" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
      <path d="M4 5h13a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H9l-5 4V5Z" stroke-linejoin="round" />
    </svg>
  </button>
</template>
