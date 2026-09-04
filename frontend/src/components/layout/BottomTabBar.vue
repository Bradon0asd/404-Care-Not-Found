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
  <div class="shrink-0 bg-white px-3 pt-1 pb-3">
    <nav class="flex items-center justify-between rounded-full bg-pink-300 px-3 py-2.5">
      <RouterLink v-for="tab in tabs" :key="tab.name" :to="tab.to" class="flex flex-1 flex-col items-center gap-1">
        <span
          class="flex items-center justify-center rounded-full bg-white transition-all"
          :class="[tab.raised ? 'h-14 w-14' : 'h-11 w-11', isActive(tab.to) ? 'ring-[3px] ring-pink-500' : '']"
        >
          <component :is="tab.icon" class="h-5 w-5" :class="isActive(tab.to) ? 'text-pink-600' : 'text-ink-500'" />
        </span>
        <span class="text-[11px]" :class="isActive(tab.to) ? 'font-bold text-ink-950' : 'text-ink-700'">{{
          tab.label
        }}</span>
      </RouterLink>
    </nav>
  </div>
</template>
