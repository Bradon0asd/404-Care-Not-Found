<script setup lang="ts">
withDefaults(
  defineProps<{
    variant?: 'primary' | 'outline' | 'line'
    type?: 'button' | 'submit'
    disabled?: boolean
  }>(),
  {
    variant: 'primary',
    type: 'button',
    disabled: false,
  },
)

defineEmits<{ click: [MouseEvent] }>()

const variantClass = {
  primary: 'bg-pink-500 text-white hover:bg-pink-600 disabled:bg-ink-400 disabled:text-ink-600',
  outline: 'border border-ink-950 bg-white text-ink-950 hover:bg-ink-200',
  line: 'bg-[#06C755] text-white hover:brightness-95',
} as const
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    class="flex w-full items-center justify-center gap-2 rounded-full px-6 py-3 text-sm font-bold transition-colors disabled:cursor-not-allowed"
    :class="variantClass[variant]"
    @click="$emit('click', $event)"
  >
    <slot />
  </button>
</template>
