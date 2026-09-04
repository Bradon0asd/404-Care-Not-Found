<script setup lang="ts">
import { useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import NewsAwarenessBanner from '@/components/tab03-chat/NewsAwarenessBanner.vue'
import FamilyIllustration from '@/components/auth/FamilyIllustration.vue'
import IntroStepCard from '@/components/tab03-chat/IntroStepCard.vue'

const router = useRouter()
</script>

<template>
  <PageContainer>
    <AppHeader />
    <NewsAwarenessBanner />

    <div class="flex-1 space-y-5 px-5 py-5">
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

    <BottomTabBar />
  </PageContainer>
</template>
