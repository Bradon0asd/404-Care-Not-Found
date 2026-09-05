<script setup lang="ts">
const words = [
  { text: 'Terimakasih', size: 'text-base', color: 'text-blue-600' },
  { text: 'Depressed', size: 'text-lg', color: 'text-red-700' },
  { text: 'Apakabar?', size: 'text-sm', color: 'text-purple-600' },
  { text: 'Sad', size: 'text-sm', color: 'text-green-700' },
  { text: 'MentalHealth', size: 'text-base', color: 'text-blue-500' },
  { text: 'Indonesia', size: 'text-sm', color: 'text-orange-600' },
  { text: 'Elder', size: 'text-sm', color: 'text-lime-700' },
  { text: 'TakeCare', size: 'text-base', color: 'text-pink-700' },
  { text: 'Family', size: 'text-base', color: 'text-fuchsia-600' },
  { text: 'Lonely', size: 'text-lg', color: 'text-red-800' },
  { text: 'Money', size: 'text-sm', color: 'text-amber-700' },
  { text: 'Taiwan', size: 'text-sm', color: 'text-orange-500' },
  { text: 'Frustrated', size: 'text-base', color: 'text-pink-600' },
]
</script>

<template>
  <div class="flex flex-wrap justify-center gap-x-3 gap-y-1 px-2">
    <span v-for="w in words" :key="w.text" class="font-bold" :class="[w.size, w.color]">{{
      $t(w.text)
    }}</span>
  </div>
</template>
