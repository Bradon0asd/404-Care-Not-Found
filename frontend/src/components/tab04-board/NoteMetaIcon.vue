<script setup lang="ts">
defineProps<{ kind: 'title' | 'permission' | 'level' }>()
</script>

<template>
  <svg
    aria-hidden="true"
    class="h-4 w-4 shrink-0 text-[#b8798b]"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="1.7"
    stroke-linecap="round"
    stroke-linejoin="round"
  >
    <template v-if="kind === 'title'">
      <path d="M7 3.5h10a1.5 1.5 0 0 1 1.5 1.5v15.5L12 16.5l-6.5 4V5A1.5 1.5 0 0 1 7 3.5Z" />
      <path d="M9.5 7.5h5" />
    </template>
    <template v-else-if="kind === 'permission'">
      <circle cx="9" cy="8" r="3.5" />
      <path
        d="M2.5 20v-1.5a6.5 6.5 0 0 1 13 0V20M16 4.7a3.5 3.5 0 0 1 0 6.6M18 14a5.5 5.5 0 0 1 3.5 5v1"
      />
    </template>
    <template v-else>
      <path d="m12 3-9 5 9 5 9-5-9-5ZM3 12l9 5 9-5M3 16l9 5 9-5" />
    </template>
  </svg>
</template>
