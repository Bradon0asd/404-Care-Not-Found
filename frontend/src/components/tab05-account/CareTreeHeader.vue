<script setup lang="ts">
defineProps<{
  userName: string
  role: string
}>()
</script>

<template>
  <div class="flex flex-col items-center">
    <div class="relative flex h-44 w-52 flex-col items-center justify-center rounded-[50%] bg-[#a9847a] pt-2 text-center">
      <!-- Placeholder avatar until the real photo asset is exported from Figma -->
      <div class="flex h-20 w-20 items-center justify-center overflow-hidden rounded-full border-4 border-white bg-pink-100 text-3xl">
        🧑🏻
      </div>
      <p class="mt-2 text-xs text-white">使用者名稱：{{ userName }}</p>
      <p class="text-xs text-white">身分：{{ role }}</p>
    </div>
    <div
      class="relative -mt-3 flex h-16 w-16 items-start justify-center bg-[#a9847a] pt-2"
      style="clip-path: polygon(35% 0, 65% 0, 100% 100%, 0 100%)"
    >
      <svg class="h-5 w-5 text-white" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 21s-6.716-4.35-9.428-8.28C.86 10.02 1.2 6.6 3.6 4.8c2.1-1.58 4.86-1.1 6.4.9L12 7.8l2-2.1c1.54-2 4.3-2.48 6.4-.9 2.4 1.8 2.74 5.22 1.03 7.92C18.72 16.65 12 21 12 21z" />
      </svg>
    </div>
    <div class="h-40 w-24 bg-[#a9847a]" style="clip-path: polygon(38% 0, 62% 0, 80% 100%, 20% 100%)"></div>
  </div>
</template>
