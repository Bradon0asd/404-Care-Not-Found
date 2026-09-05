<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import NewsAwarenessBanner from '@/components/tab03-chat/NewsAwarenessBanner.vue'
import FamilyIllustration from '@/components/auth/FamilyIllustration.vue'
import IntroStepCard from '@/components/tab03-chat/IntroStepCard.vue'
import DailyChatHome from '@/components/tab03-chat/DailyChatHome.vue'
import { useCareAgentStore } from '@/stores/careAgent'

const router = useRouter()
const store = useCareAgentStore()

const showReadyNotice = ref(true)

// Dev-only: lets you preview the first-time build flow without a real
// reset/logout feature. Only clears the agent, not chat rooms/moods.
function simulateFirstLogin() {
  store.agent = null
}
</script>

<template>
  <PageContainer>
    <template #header>
      <AppHeader />
      <NewsAwarenessBanner />
    </template>

    <div v-if="!store.agent" class="flex-1 space-y-5 px-5 py-5">
      <div class="flex justify-center">
        <FamilyIllustration />
      </div>

      <IntroStepCard :number="1">
        <p>從 0 開始生成你的專屬 Care Agent 陪你一起認識、認知自己的情緒與壓力</p>
        <div class="max-w-[220px]">
          <BaseButton variant="primary" @click="router.push('/chat/setup')">建置你的第一個 Care Agent</BaseButton>
        </div>
      </IntroStepCard>

      <IntroStepCard :number="2">
        <p>完成簡單幾個問題，協助 Agent 建立心理基準線<br />你的日常 Care Agent 就完成啦！</p>
      </IntroStepCard>

      <div class="flex items-center gap-2 text-xs text-ink-500">
        <span class="h-px flex-1 bg-ink-400"></span>
        Care Agent 建置完成後
        <span class="h-px flex-1 bg-ink-400"></span>
      </div>

      <IntroStepCard :number="3"><p>對話模式</p></IntroStepCard>
      <IntroStepCard :number="4"><p>查看 Care Agent 回應與紀錄</p></IntroStepCard>
      <IntroStepCard :number="5"><p>歷程回顧</p></IntroStepCard>
    </div>

    <template v-else>
      <div v-if="showReadyNotice" class="mx-3 mt-3 flex items-center gap-2 rounded-xl bg-pink-100 px-3 py-2 text-xs">
        <p class="flex-1 text-ink-700">你的 Care Agent 已經準備好了，陪你一起聊聊今天的心情</p>
        <button
          type="button"
          class="flex h-5 w-5 shrink-0 items-center justify-center rounded-md bg-ink-400 text-ink-700"
          aria-label="關閉提示"
          @click="showReadyNotice = false"
        >
          <svg class="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M6 6l12 12M18 6 6 18" stroke-linecap="round" />
          </svg>
        </button>
      </div>

      <div class="px-5 pt-2 text-right">
        <button type="button" class="text-[11px] text-ink-500 underline" @click="simulateFirstLogin">
          模擬首次使用畫面
        </button>
      </div>

      <DailyChatHome />
    </template>

    <template #footer><BottomTabBar /></template>
  </PageContainer>
</template>
