<script setup lang="ts">
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useOnboardingStore } from '@/stores/onboarding'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import FamilyIllustration from '@/components/auth/FamilyIllustration.vue'

const router = useRouter()
const store = useOnboardingStore()
const { language, arrivalDate, careRecipientOrdinal } = storeToRefs(store)

function startUsing() {
  router.push('/')
}
</script>

<template>
  <PageContainer>
    <AppHeader />

    <div class="flex flex-1 flex-col items-center gap-6 px-6 py-8">
      <FamilyIllustration />

      <div class="w-full space-y-6">
        <fieldset>
          <legend class="mb-2 text-sm text-ink-700">選擇語言</legend>
          <div class="flex rounded-full border border-ink-400 p-1">
            <label
              class="flex flex-1 cursor-pointer items-center justify-center gap-2 rounded-full py-2 text-sm"
              :class="language === 'id' ? 'bg-white font-bold text-ink-950 shadow' : 'text-ink-600'"
            >
              <input type="radio" value="id" v-model="language" class="accent-accent" />
              印尼文
            </label>
            <label
              class="flex flex-1 cursor-pointer items-center justify-center gap-2 rounded-full py-2 text-sm"
              :class="language === 'zh' ? 'bg-white font-bold text-ink-950 shadow' : 'text-ink-600'"
            >
              <input type="radio" value="zh" v-model="language" class="accent-accent" />
              中文
            </label>
          </div>
        </fieldset>

        <label class="block">
          <span class="mb-2 block text-sm text-ink-700">入境臺灣日期</span>
          <input
            v-model="arrivalDate"
            type="date"
            class="w-full rounded-full border border-ink-400 px-4 py-3 text-sm text-ink-950"
          />
        </label>

        <label class="block">
          <span class="mb-2 block text-sm text-ink-700">這是我的第幾位照顧者</span>
          <select
            v-model.number="careRecipientOrdinal"
            class="w-full rounded-full border border-ink-400 px-4 py-3 text-sm text-ink-950"
          >
            <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
          </select>
        </label>
      </div>

      <div class="mt-auto flex w-full flex-col gap-3">
        <BaseButton variant="primary" @click="startUsing">開始使用</BaseButton>
        <BaseButton variant="outline" @click="router.back()">返回上一步驟</BaseButton>
      </div>
    </div>
  </PageContainer>
</template>
