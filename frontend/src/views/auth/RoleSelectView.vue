<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useOnboardingStore } from '@/stores/onboarding'
import { useAuthStore } from '@/stores/auth'
import { startLineLogin } from '@/api/auth'
import { enterInvite } from '@/api/invites'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import RoleCard from '@/components/auth/RoleCard.vue'
import FamilyIllustration from '@/components/auth/FamilyIllustration.vue'
import IconCaregiver from '@/components/auth/icons/IconCaregiver.vue'
import IconEmployer from '@/components/auth/icons/IconEmployer.vue'
import IconLine from '@/components/auth/icons/IconLine.vue'

const router = useRouter()
const route = useRoute()
const store = useOnboardingStore()
const auth = useAuthStore()
const { role } = storeToRefs(store)

const submitting = ref(false)
const errorCode = ref('')

// The LINE callback bounces failures back here as ?error=CODE.
const ERROR_TEXT: Record<string, string> = {
  LINE_LOGIN_DECLINED: '你在 LINE 取消了授權',
  LINE_LOGIN_FAILED: 'LINE 登入沒有完成，請再試一次',
  LINE_LOGIN_NOT_CONFIGURED: 'LINE 登入還沒設定完成',
  ROLE_MISMATCH: '這個 LINE 帳號已經用另一個身分註冊過了',
  SESSION_NOT_FOUND: '登入沒有完成，請再試一次',
  NETWORK_ERROR: '連不到伺服器，請確認後端有啟動',
}

function errorText(code: string) {
  return ERROR_TEXT[code] ?? '登入失敗，請再試一次'
}

// Arriving via an employer's invite link means the visitor is the caregiver being invited.
onMounted(async () => {
  if (route.query.invite) {
    store.selectRole('caregiver')
    try {
      await enterInvite(String(route.query.invite))
      await auth.loadSession()
      router.push('/auth/caregiver/onboarding')
      return
    } catch (error) {
      errorCode.value = error instanceof Error && 'code' in error ? String(error.code) : ''
    }
  }
  if (route.query.error) {
    errorCode.value = String(route.query.error)
  }
})

async function handleLineRegister() {
  if (!role.value || submitting.value) return
  submitting.value = true
  errorCode.value = ''
  try {
    // Leaving the SPA entirely: LINE owns the next screen.
    window.location.href = await startLineLogin(role.value)
  } catch (error) {
    errorCode.value = error instanceof Error && 'code' in error ? String(error.code) : ''
    submitting.value = false
  }
}
</script>

<template>
  <PageContainer>
    <template #header><AppHeader /></template>

    <div class="flex flex-1 flex-col items-center gap-6 px-6 py-10">
      <div class="text-center">
        <h1
          class="flex flex-wrap items-baseline justify-center gap-x-2 gap-y-1 font-bold text-ink-950"
        >
          <span class="text-xl">{{ $t('歡迎使用') }}</span>
          <span class="text-pink-600" :class="store.language === 'id' ? 'text-3xl' : 'text-4xl'">{{
            $t('照見')
          }}</span>
        </h1>
        <p class="mt-2 text-sm text-ink-700">{{ $t('請先選擇你的身分') }}</p>
      </div>

      <FamilyIllustration />

      <div class="flex gap-4">
        <RoleCard
          :label="$t('看護')"
          :selected="role === 'caregiver'"
          @select="store.selectRole('caregiver')"
        >
          <template #icon><IconCaregiver /></template>
        </RoleCard>
        <RoleCard
          :label="$t('雇主')"
          :selected="role === 'employer'"
          @select="store.selectRole('employer')"
        >
          <template #icon><IconEmployer /></template>
        </RoleCard>
      </div>

      <div class="mt-auto flex w-full flex-col gap-3">
        <p v-if="errorCode" class="text-center text-sm text-pink-600">
          {{ $t(errorText(errorCode)) }}
        </p>
        <BaseButton variant="line" :disabled="!role || submitting" @click="handleLineRegister">
          <IconLine />{{ submitting ? $t('前往 LINE…') : $t('使用 LINE 註冊') }}</BaseButton
        >
        <BaseButton variant="outline" @click="router.back()">{{ $t('返回上一步驟') }}</BaseButton>
      </div>
    </div>
  </PageContainer>
</template>
