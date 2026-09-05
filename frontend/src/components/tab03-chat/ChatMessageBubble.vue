<script setup lang="ts">
import type { ChatMessage } from '@/stores/careAgent'
import { welcomeMessage } from '@/stores/careAgent'

defineProps<{ message: ChatMessage }>()
</script>

<template>
  <div
    class="max-w-[75%] rounded-2xl px-4 py-2.5 text-sm whitespace-pre-line"
    :class="
      message.sender === 'user'
        ? 'self-end rounded-br-sm bg-pink-300 text-ink-950'
        : 'self-start rounded-bl-sm bg-ink-200 text-ink-950'
    "
  >
    {{
      message.kind === 'welcome'
        ? welcomeMessage().text
        : message.demo
          ? $t(message.text)
          : message.text
    }}
  </div>
</template>
