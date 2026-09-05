<script setup lang="ts">
import { computed } from 'vue'
import IconFootprint from './icons/IconFootprint.vue'

type Alignment = 'left' | 'center' | 'right'
const props = defineProps<{ from: Alignment; to: Alignment }>()
const positions = { left: 0, center: 50, right: 100 }
const midpoint = computed(() => (positions[props.from] + positions[props.to]) / 2)
const angle = computed(() => Math.sign(positions[props.to] - positions[props.from]) * 55)
</script>

<template>
  <div aria-hidden="true" class="relative mx-8 h-5 shrink-0 text-ink-800">
    <div
      class="absolute top-1/2"
      :style="{ left: `${midpoint}%`, transform: `rotate(${angle}deg)` }"
    >
      <IconFootprint class="absolute -top-1 -left-3 h-4 w-3 -rotate-6" />
      <IconFootprint class="absolute -top-3 left-0.5 h-4 w-3 scale-x-[-1] rotate-6" />
    </div>
  </div>
</template>
