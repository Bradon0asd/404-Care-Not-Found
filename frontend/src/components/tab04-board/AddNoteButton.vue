<script setup lang="ts">
defineEmits<{ click: [] }>()
</script>

<template>
  <button
    type="button"
    aria-label="新增便利貼"
    class="absolute right-4 bottom-4 flex h-[72px] w-[72px] items-center justify-center rounded-full border border-ink-600 bg-white shadow-[0_2px_3px_#00000030] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-ink-800"
    @click="$emit('click')"
  >
    <svg aria-hidden="true" class="h-12 w-12" viewBox="0 0 64 64" fill="none">
      <path d="M13 17L57 23L53 60L10 52L5 43Z" fill="#d7c51b" />
      <path d="M11 14L58 20L49 53L6 46Z" fill="#f2df00" />
      <path d="M9 11L56 18L47 48L3 39Z" fill="#dbcb19" />
      <path d="M16 5L58 13L47 43Q46 46 41 45L5 36Z" fill="#fff000" />
      <path d="M32 21V35M25 28H39" stroke="black" stroke-width="1.8" stroke-linecap="round" />
    </svg>
  </button>
</template>
