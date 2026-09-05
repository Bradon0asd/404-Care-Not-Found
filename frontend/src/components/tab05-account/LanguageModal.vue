<script setup lang="ts">
import SegmentedToggle from '@/components/common/SegmentedToggle.vue'
import type { Language } from '@/stores/onboarding'

defineProps<{ open: boolean; language: Language }>()
defineEmits<{ close: []; 'update:language': [Language] }>()
</script>

<template>
  <Teleport to="body">
    <div
      v-if="open"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-6"
      @click.self="$emit('close')"
    >
      <div class="w-full max-w-xs space-y-4 rounded-2xl bg-white p-5">
        <h2 class="text-sm font-bold text-ink-950">{{ $t('變更語言') }}</h2>
        <SegmentedToggle
          variant="tab"
          :model-value="language"
          :options="[
            { value: 'id', label: '印尼文' },
            { value: 'zh', label: '中文' },
          ]"
          @update:model-value="(v) => $emit('update:language', v as Language)"
        />
      </div>
    </div>
  </Teleport>
</template>
