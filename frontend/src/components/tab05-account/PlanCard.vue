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
    class="relative overflow-hidden rounded-xl p-4"
    :class="{ 'bg-ink-200': tier === 'free', 'bg-pink-200': tier === 'basic', 'bg-pink-400': tier === 'premium' }"
  >
    <span
      v-if="current"
      class="absolute top-3 -right-8 w-32 rotate-45 bg-pink-500 py-1 text-center text-[10px] font-bold text-white"
    >
      目前方案
    </span>

    <div class="flex items-start justify-between">
      <div>
        <h3 class="mb-2 text-sm font-bold text-ink-950">{{ name }}</h3>
        <ul class="space-y-1 text-xs text-ink-700">
          <li v-for="f in features" :key="f">• {{ f }}</li>
        </ul>
      </div>
      <div v-if="price" class="shrink-0 pl-3 text-right">
        <p class="text-[11px] text-ink-700">費用</p>
        <p class="text-lg font-bold text-ink-950">{{ price }}</p>
        <p class="text-[11px] text-ink-700">{{ period }}</p>
      </div>
    </div>
  </div>
</template>
