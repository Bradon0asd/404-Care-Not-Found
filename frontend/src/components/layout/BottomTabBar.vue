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
  { name: 'chat', to: '/chat', label: '跟我\n聊聊', icon: IconChat, raised: true },
  { name: 'board', to: '/board', label: '便利貼牆', icon: IconBoard },
  { name: 'account', to: '/account', label: '我的帳戶', icon: IconAccount },
]

function isActive(to: string) {
  return route.path.startsWith(to)
}
</script>

<template>
  <div
    class="relative z-30 shrink-0 bg-white px-5 pt-4 pb-[calc(28px+env(safe-area-inset-bottom,0px))]"
  >
    <nav class="flex h-[52px] items-stretch rounded-full bg-pink-300">
      <RouterLink
        v-for="tab in tabs"
        :key="tab.name"
        :to="tab.to"
        class="relative flex flex-1 flex-col items-center justify-start"
      >
        <!-- The middle item always owns the raised Figma silhouette. -->
        <span
          v-if="tab.raised"
          class="absolute top-1/2 left-1/2 h-[72px] w-[72px] -translate-x-1/2 -translate-y-1/2 rounded-full"
          :class="isActive(tab.to) ? 'bg-pink-400' : 'bg-pink-300'"
        ></span>
        <span
          v-else-if="isActive(tab.to)"
          class="absolute inset-0.5 rounded-full bg-pink-400"
        ></span>

        <span
          class="relative z-10 flex shrink-0 items-center justify-center rounded-full bg-white"
          :class="tab.raised ? '-mt-1 h-9 w-9' : 'mt-1.5 h-6 w-6'"
        >
          <component :is="tab.icon" class="h-3.5 w-3.5 text-ink-500" />
        </span>
        <span
          class="relative z-10 mt-0.5 whitespace-pre-line text-center text-[9px] leading-[10px] text-ink-950"
          :class="isActive(tab.to) ? 'font-bold' : 'font-medium'"
          >{{ $t(tab.label) }}</span
        >
      </RouterLink>
    </nav>
  </div>
</template>
