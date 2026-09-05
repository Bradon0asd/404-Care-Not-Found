<script setup lang="ts">
import { ref } from 'vue'
import IconSend from './icons/IconSend.vue'

const emit = defineEmits<{ send: [string] }>()

const text = ref('')

function submit() {
  if (!text.value.trim()) return
  emit('send', text.value.trim())
  text.value = ''
}

// TODO: wire up once the Indonesian ASR service is available.
function startVoiceInput() {
  console.info('聊天室語音輸入 — 待接 ASR 服務')
}
</script>

<template>
  <form
    class="flex items-center gap-2 border-t border-ink-300 bg-white px-3 py-2"
    @submit.prevent="submit"
  >
    <button
      type="button"
      class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-ink-200 text-ink-600"
      :aria-label="$t('語音輸入')"
      @click="startVoiceInput"
    >
      <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
        <rect x="9" y="3" width="6" height="11" rx="3" />
        <path d="M5 11a7 7 0 0 0 14 0M12 18v3" stroke-linecap="round" />
      </svg>
    </button>
    <input
      v-model="text"
      type="text"
      :placeholder="$t('Tulis pesanmu di sini... (印尼語輸入)')"
      class="flex-1 rounded-full bg-ink-200 px-4 py-2 text-sm text-ink-950 placeholder:text-ink-600"
    />
    <button
      type="submit"
      class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-pink-500 text-white"
      :aria-label="$t('送出')"
    >
      <IconSend class="h-4 w-4" />
    </button>
  </form>
</template>
