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
  <nav class="flex items-end justify-between bg-pink-200 px-2 pt-3 pb-2">
    <RouterLink
      v-for="tab in tabs"
      :key="tab.name"
      :to="tab.to"
      class="flex flex-1 flex-col items-center gap-1 text-[11px]"
      :class="tab.raised ? '-mt-6' : ''"
    >
      <span
        class="flex items-center justify-center rounded-full"
        :class="[
          tab.raised ? 'h-14 w-14 bg-white shadow-md' : 'h-9 w-9',
          !tab.raised && isActive(tab.to) ? 'bg-pink-500' : '',
        ]"
      >
        <component
          :is="tab.icon"
          class="h-5 w-5"
          :class="tab.raised ? 'text-pink-500' : isActive(tab.to) ? 'text-white' : 'text-ink-600'"
        />
      </span>
      <span :class="isActive(tab.to) ? 'font-bold text-ink-950' : 'text-ink-600'">{{ tab.label }}</span>
    </RouterLink>
  </nav>
</template>
