<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'
import SubPageHeader from '@/components/layout/SubPageHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import PlanCard from '@/components/tab05-account/PlanCard.vue'
import { useAccountStore, type Plan } from '@/stores/account'

const account = useAccountStore()

// TODO: wire up once billing/payment is decided; for now this doesn't
// let the caregiver pick a specific plan, just flags the button is unwired.
function changePlan() {
  console.info('變更方案 — 待接付款流程')
}

const plans: {
  tier: Plan
  name: string
  price: string | null
  period: string
  features: string[]
}[] = [
  {
    tier: 'free',
    name: '免費方案',
    price: null,
    period: '',
    features: ['AI 語音辨識一天免費使用 1 次', '最多建立 1 個 Care Agents', '一天最多只能開「一個」聊天室', '便利貼上限 20 個'],
  },
  {
    tier: 'basic',
    name: '小資方案',
    price: '$199',
    period: '/月',
    features: ['AI 語音辨識一天使用 5 次', '當月最多建立 3 個 Care Agents', '一天最多只能開「五個」聊天室', '便利貼上限 50 個'],
  },
  {
    tier: 'premium',
    name: '進階方案',
    price: '$399',
    period: '/月',
    features: ['AI 語音辨識一天使用 30 次', '當月最多建立 10 個 Care Agents', '不限制聊天室開啟數量', '不限制便利貼數量'],
  },
]
</script>

<template>
  <PageContainer>
    <AppHeader />
    <SubPageHeader title="訂閱方案一覽表" />

    <div class="flex-1 space-y-4 px-4 pb-4">
      <PlanCard
        v-for="plan in plans"
        :key="plan.tier"
        :tier="plan.tier"
        :name="plan.name"
        :price="plan.price"
        :period="plan.period"
        :features="plan.features"
        :current="account.plan === plan.tier"
      />

      <BaseButton variant="outline" @click="changePlan">變更方案</BaseButton>
    </div>

    <BottomTabBar />
  </PageContainer>
</template>
