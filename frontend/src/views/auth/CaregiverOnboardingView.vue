<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useOnboardingStore } from '@/stores/onboarding'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import FamilyIllustration from '@/components/auth/FamilyIllustration.vue'

const router = useRouter()
const store = useOnboardingStore()
const auth = useAuthStore()
const { language, arrivalDate, careRecipientOrdinal } = storeToRefs(store)

const saving = ref(false)
const failed = ref(false)

async function startUsing() {
  if (saving.value) return
  saving.value = true
  failed.value = false
  try {
    // Only the language has a home in the backend today; the rest stays local.
    await auth.completeOnboarding({ language: language.value })
    router.push('/dashboard')
  } catch {
    // Without the stamp the next login would ask for this form again, so stay put.
    failed.value = true
    saving.value = false
  }
}
</script>

<template>
  <PageContainer>
    <template #header><AppHeader /></template>

    <div class="flex flex-1 flex-col items-center gap-6 px-6 py-8">
      <FamilyIllustration />

      <div class="w-full space-y-6">
        <fieldset>
          <legend class="mb-2 text-sm text-ink-700">{{ $t('選擇語言') }}</legend>
          <div class="flex rounded-full border border-ink-400 p-1">
            <label
              class="flex flex-1 cursor-pointer items-center justify-center gap-2 rounded-full py-2 text-sm"
              :class="language === 'id' ? 'bg-white font-bold text-ink-950 shadow' : 'text-ink-600'"
            >
              <input type="radio" value="id" v-model="language" class="accent-accent" />{{
                $t('印尼文')
              }}</label
            >
            <label
              class="flex flex-1 cursor-pointer items-center justify-center gap-2 rounded-full py-2 text-sm"
              :class="language === 'zh' ? 'bg-white font-bold text-ink-950 shadow' : 'text-ink-600'"
            >
              <input type="radio" value="zh" v-model="language" class="accent-accent" />{{
                $t('中文')
              }}</label
            >
          </div>
        </fieldset>

        <label class="block">
          <span class="mb-2 block text-sm text-ink-700">{{ $t('入境臺灣日期') }}</span>
          <input
            v-model="arrivalDate"
            type="date"
            class="w-full rounded-full border border-ink-400 px-4 py-3 text-sm text-ink-950"
          />
        </label>

        <label class="block">
          <span class="mb-2 block text-sm text-ink-700">{{ $t('這是我的第幾位照顧者') }}</span>
          <select
            v-model.number="careRecipientOrdinal"
            class="w-full rounded-full border border-ink-400 px-4 py-3 text-sm text-ink-950"
          >
            <option v-for="n in 10" :key="n" :value="n">{{ $t(n) }}</option>
          </select>
        </label>
      </div>

      <div class="mt-auto flex w-full flex-col gap-3">
        <p v-if="failed" class="text-center text-sm text-pink-600">
          {{ $t('沒有存起來，請再試一次') }}
        </p>
        <BaseButton variant="primary" :disabled="saving" @click="startUsing">{{
          $t('開始使用')
        }}</BaseButton>
        <BaseButton variant="outline" @click="router.back()">{{ $t('返回上一步驟') }}</BaseButton>
      </div>
    </div>
  </PageContainer>
</template>
