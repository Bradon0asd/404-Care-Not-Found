<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import UpgradeLimitBanner from '@/components/common/UpgradeLimitBanner.vue'
import AiVoiceButton from '@/components/common/AiVoiceButton.vue'
import StepProgressIndicator from '@/components/tab03-chat/StepProgressIndicator.vue'
import TemperatureSlider from '@/components/tab03-chat/TemperatureSlider.vue'
import GuardrailField from '@/components/tab03-chat/GuardrailField.vue'
import { useCareAgentStore } from '@/stores/careAgent'
import { useAccountStore } from '@/stores/account'

const router = useRouter()
const store = useCareAgentStore()
const account = useAccountStore()

const systemPrompt = ref('')
const temperature = ref(0)
const guardrail = ref('')

// TODO: wire up once the Indonesian ASR service is available.
function startVoiceInput() {
  console.info('System Prompt 語音輸入 — 待接 ASR 服務')
}

async function next() {
  if (!account.currentCareRecipientId) {
    await account.loadAccount()
  }
  if (!account.currentCareRecipientId) return
  await store.createAgent({
    careRecipientId: account.currentCareRecipientId,
    systemPrompt: systemPrompt.value,
    temperature: temperature.value,
    guardrail: guardrail.value,
  })
  router.push('/chat/baseline')
}
</script>

<template>
  <PageContainer>
    <template #header>
      <AppHeader />
      <UpgradeLimitBanner
        :message="$t('免費版最多生成「1 個」Agent，')"
        :upgrade-text="$t('立即升級享有更完整體驗')"
      />
    </template>

    <StepProgressIndicator :current="1" />
    <div class="flex-1 space-y-4 px-4 pb-4">
      <h1 class="text-base font-bold text-ink-950">{{ $t('建置你的客製化 Care Agent') }}</h1>

      <div class="rounded-xl bg-ink-200 p-4">
        <div class="mb-2 flex items-center justify-between">
          <h3 class="text-sm font-bold text-ink-950">System Prompt</h3>
          <AiVoiceButton @click="startVoiceInput" />
        </div>
        <textarea
          v-model="systemPrompt"
          rows="5"
          :placeholder="
            $t(
              '輸入病患照護情境\n例：「你是一位來自印尼的專屬照護員，正在照顧一位90歲，有阿茲海默症、蜂窩性組織炎、四肢無力的女性病患，她每天需要固定做的事情是⋯」\n備註：除了文字輸入外，也可點選右上方「AI 語音辨識」新增 System Prompt 內容！',
            )
          "
          class="w-full bg-transparent text-sm text-ink-950 placeholder:text-ink-600"
        ></textarea>
      </div>

      <TemperatureSlider v-model="temperature" />
      <GuardrailField v-model="guardrail" />

      <BaseButton variant="primary" @click="next">{{
        $t('下一步：協助 Agent 建立心理基準線')
      }}</BaseButton>
    </div>

    <template #footer><BottomTabBar /></template>
  </PageContainer>
</template>
