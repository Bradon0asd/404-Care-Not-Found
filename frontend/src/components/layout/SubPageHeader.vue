<script setup lang="ts">
import { useRouter } from 'vue-router'
import IconArrowLeft from '@/components/common/icons/IconArrowLeft.vue'

defineProps<{ title: string }>()
const router = useRouter()
</script>

<template>
  <div class="relative flex items-center justify-center px-3 py-3">
    <button type="button" class="absolute left-3" :aria-label="$t('返回')" @click="router.back()">
      <IconArrowLeft class="h-5 w-5 text-ink-950" />
    </button>
    <h1 class="text-sm font-bold text-ink-950">{{ $t(title) }}</h1>
  </div>
</template>
