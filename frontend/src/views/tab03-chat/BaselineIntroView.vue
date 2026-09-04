<script setup lang="ts">
import { useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import UpgradeLimitBanner from '@/components/common/UpgradeLimitBanner.vue'
import ExpandableSection from '@/components/common/ExpandableSection.vue'
import StepProgressIndicator from '@/components/tab03-chat/StepProgressIndicator.vue'
import WordCloud from '@/components/tab03-chat/WordCloud.vue'

const router = useRouter()
</script>

<template>
  <PageContainer>
    <AppHeader />
    <UpgradeLimitBanner message="免費版最多生成「1 個」Agent，" upgrade-text="立即升級享有更完整體驗" />
    <StepProgressIndicator :current="1" />

    <div class="flex-1 space-y-4 px-4 pb-4">
      <div class="space-y-3 rounded-xl bg-ink-200 p-4 text-center">
        <p class="text-sm text-ink-700">一起聊聊你最近的狀態吧</p>
        <WordCloud />
        <div class="mx-auto max-w-[220px]">
          <BaseButton variant="primary" @click="router.push('/chat/baseline/questions')">完成一次性小任務</BaseButton>
        </div>
      </div>

      <ExpandableSection title="說明與免責聲明">
        <p>
          這五個小問題是為了協助 Care Agent 更了解你最近的狀態，回答內容只用來建立你的專屬 Agent，不會出現在你的日常對話裡，也不會被雇主看到。
        </p>
      </ExpandableSection>
    </div>

    <BottomTabBar />
  </PageContainer>
</template>
