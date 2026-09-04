<script setup lang="ts">
import { ref } from 'vue'
import BaseButton from '@/components/common/BaseButton.vue'
import IconWeatherSunny from './icons/IconWeatherSunny.vue'
import IconWeatherPartlyCloudy from './icons/IconWeatherPartlyCloudy.vue'
import IconWeatherCloudy from './icons/IconWeatherCloudy.vue'
import IconWeatherRainy from './icons/IconWeatherRainy.vue'
import IconWeatherStorm from './icons/IconWeatherStorm.vue'
import type { Weather } from '@/stores/careAgent'

const emit = defineEmits<{ submit: [Weather] }>()

const options: { value: Weather; icon: unknown }[] = [
  { value: 'sunny', icon: IconWeatherSunny },
  { value: 'partly-cloudy', icon: IconWeatherPartlyCloudy },
  { value: 'cloudy', icon: IconWeatherCloudy },
  { value: 'rainy', icon: IconWeatherRainy },
  { value: 'thunderstorm', icon: IconWeatherStorm },
]

const selected = ref<Weather | null>(null)

function submit() {
  if (!selected.value) return
  emit('submit', selected.value)
}
</script>

<template>
  <div class="px-4">
    <p class="mb-3 text-center text-sm text-ink-700">每日心情（下列哪個 icon 最能表達你現在的心情？）</p>
    <div class="mb-3 flex justify-center gap-4">
      <button
        v-for="opt in options"
        :key="opt.value"
        type="button"
        class="flex h-9 w-9 items-center justify-center"
        :class="selected === opt.value ? 'text-pink-600' : 'text-pink-300'"
        @click="selected = opt.value"
      >
        <component :is="opt.icon" class="h-full w-full" />
      </button>
    </div>
    <div class="mx-auto max-w-[160px]">
      <BaseButton variant="primary" :disabled="!selected" @click="submit">送出</BaseButton>
    </div>
  </div>
</template>
