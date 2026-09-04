<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'
import IconClipboard from './icons/IconClipboard.vue'
import IconDiary from './icons/IconDiary.vue'
import IconChat from './icons/IconChat.vue'
import IconBoard from './icons/IconBoard.vue'
import IconAccount from './icons/IconAccount.vue'

const route = useRoute()

const tabs = [
  { name: 'dashboard', to: '/dashboard', label: '照護紀錄', icon: IconClipboard },
  { name: 'diary', to: '/diary', label: '秘密日記', icon: IconDiary },
  { name: 'chat', to: '/chat', label: '跟我聊聊', icon: IconChat, raised: true },
  { name: 'board', to: '/board', label: '便利貼牆', icon: IconBoard },
  { name: 'account', to: '/account', label: '我的帳戶', icon: IconAccount },
]

function isActive(to: string) {
  return route.path.startsWith(to)
}
</script>

<template>
  <div class="shrink-0 bg-white px-3 pt-4 pb-2">
    <nav class="flex items-end justify-between rounded-full bg-pink-300 px-2 pt-1.5 pb-2">
      <RouterLink v-for="tab in tabs" :key="tab.name" :to="tab.to" class="relative flex flex-1 flex-col items-center">
        <!-- active highlight: one capsule covering icon + label -->
        <span
          v-if="isActive(tab.to)"
          class="absolute inset-x-1 bottom-0 rounded-2xl bg-pink-400"
          :style="{ top: tab.raised ? '-22px' : '-2px' }"
        ></span>

        <span
          class="relative z-10 flex items-center justify-center rounded-full bg-white"
          :class="tab.raised ? '-mt-6 h-14 w-14 shadow-md' : 'h-8 w-8'"
        >
          <component :is="tab.icon" class="h-4 w-4" :class="isActive(tab.to) ? 'text-pink-600' : 'text-ink-500'" />
        </span>
        <span class="relative z-10 mt-0.5 text-[10px]" :class="isActive(tab.to) ? 'font-bold text-ink-950' : 'text-ink-700'">{{
          tab.label
        }}</span>
      </RouterLink>
    </nav>
  </div>
</template>
