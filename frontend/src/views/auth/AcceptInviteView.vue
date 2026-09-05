<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { enterInvite } from '@/api/invites'
import { useAuthStore } from '@/stores/auth'
import { useOnboardingStore } from '@/stores/onboarding'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import FamilyIllustration from '@/components/auth/FamilyIllustration.vue'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const onboarding = useOnboardingStore()

const loading = ref(true)
const failed = ref(false)

async function acceptInvite() {
  const code = String(route.params.code || '')
  if (!code) {
    failed.value = true
    loading.value = false
    return
  }

  loading.value = true
  failed.value = false
  onboarding.selectRole('caregiver')

  try {
    const entry = await enterInvite(code)
    const user = await auth.loadSession()
    if (entry.needs_profile || user?.needs_onboarding) {
      router.replace('/auth/caregiver/onboarding')
    } else {
      router.replace('/dashboard')
    }
  } catch {
    failed.value = true
    loading.value = false
  }
}

onMounted(acceptInvite)
</script>

<template>
  <PageContainer>
    <template #header><AppHeader /></template>

    <div class="flex flex-1 flex-col items-center gap-6 px-6 py-8 text-center">
      <FamilyIllustration />

      <div class="w-full space-y-2">
        <h1 class="text-xl font-bold text-ink-950">{{ $t('接受照護邀請') }}</h1>
        <p class="text-sm leading-6 text-ink-700">
          {{
            $t(
              loading
                ? '正在確認邀請，請稍等'
                : '邀請連結無法使用，請確認連結是否正確或請雇主重新產生',
            )
          }}
        </p>
      </div>

      <div v-if="failed" class="mt-auto flex w-full flex-col gap-3">
        <BaseButton variant="primary" @click="acceptInvite">{{ $t('重新確認邀請') }}</BaseButton>
        <BaseButton variant="outline" @click="router.replace('/auth/role')">{{
          $t('返回上一步驟')
        }}</BaseButton>
      </div>
    </div>
  </PageContainer>
</template>
