<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import IconArrowLeft from './icons/IconArrowLeft.vue'
import IconPencil from '@/components/tab02-diary/icons/IconPencil.vue'

const title = defineModel<string>('title', { required: true })
const router = useRouter()

const editing = ref(false)
</script>

<template>
  <header class="flex items-center gap-2 border-b border-ink-300 px-3 py-3">
    <button type="button" aria-label="返回" @click="router.back()">
      <IconArrowLeft class="h-5 w-5 text-ink-950" />
    </button>
    <input
      v-if="editing"
      v-model="title"
      type="text"
      class="flex-1 border-b border-ink-400 bg-transparent text-sm font-bold text-ink-950 outline-none"
      @blur="editing = false"
    />
    <span v-else class="flex-1 truncate text-sm font-bold text-ink-950">{{ title }}</span>
    <button type="button" aria-label="編輯標題" @click="editing = true">
      <IconPencil class="h-4 w-4 text-ink-600" />
    </button>
  </header>
</template>
