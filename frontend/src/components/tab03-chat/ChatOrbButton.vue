<script setup lang="ts">
defineEmits<{ click: [] }>()
</script>

<template>
  <button
    type="button"
    :aria-label="$t('新增聊天室')"
    class="relative flex h-48 w-48 flex-col items-center justify-center gap-3 rounded-full shadow-lg"
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
    <svg
      aria-hidden="true"
      class="h-16 w-20"
      viewBox="0 0 120 104"
      fill="white"
      stroke="black"
      stroke-width="1.2"
      stroke-linejoin="round"
    >
      <path
        d="M34 32H14A12 12 0 0 0 2 44V76A12 12 0 0 0 14 88H19V102L35 88H63A12 12 0 0 0 75 76V68H34Z"
      />
      <path
        d="M54 4H103A12 12 0 0 1 115 16V48A12 12 0 0 1 103 60H98V76L82 60H42V16A12 12 0 0 1 54 4Z"
      />
    </svg>
    <span class="text-sm font-medium text-black">{{ $t('新增聊天室') }}</span>
  </button>
</template>
