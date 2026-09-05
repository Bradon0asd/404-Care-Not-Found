<script setup lang="ts">
defineProps<{
  name: string
  price: string | null
  period: string
  features: string[]
  current: boolean
  tier: 'free' | 'basic' | 'premium'
}>()
</script>

<template>
  <div
    class="relative overflow-hidden rounded-xl p-4 shadow-[0_6px_12px_-4px_rgba(75,45,55,0.18),0_2px_4px_rgba(75,45,55,0.08)]"
    :class="{
      'bg-ink-100 text-ink-700': tier === 'free',
      'bg-pink-100 text-ink-700': tier === 'basic',
      'bg-pink-600 text-white': tier === 'premium',
    }"
  >
    <span
      v-if="current"
      class="absolute top-3 -right-8 w-32 rotate-45 bg-pink-600 py-1 text-center text-[10px] font-bold text-white"
    >
      目前方案
    </span>

    <div class="flex items-start justify-between">
      <div>
        <h3 class="mb-2 text-sm font-bold">{{ name }}</h3>
        <ul class="space-y-1 text-xs" :class="tier === 'premium' ? 'text-white' : 'text-ink-600'">
          <li v-for="f in features" :key="f">• {{ f }}</li>
        </ul>
      </div>
      <div v-if="price" class="shrink-0 pl-3 text-right">
        <p class="text-[11px]">費用</p>
        <p class="text-lg font-bold">{{ price }}</p>
        <p class="text-[11px]">{{ period }}</p>
      </div>
    </div>
  </div>
</template>
