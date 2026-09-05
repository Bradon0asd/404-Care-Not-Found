<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useOnboardingStore } from '@/stores/onboarding'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import ExpandableSection from '@/components/common/ExpandableSection.vue'
import FamilyIllustration from '@/components/auth/FamilyIllustration.vue'
import InviteCodeModal from '@/components/auth/InviteCodeModal.vue'
import { createInvite } from '@/api/invites'

const router = useRouter()
const store = useOnboardingStore()
const auth = useAuthStore()

const modalOpen = ref(false)
const saving = ref(false)
const failed = ref(false)
const inviteLink = ref('')

async function generateInviteCode() {
  if (saving.value) return
  saving.value = true
  failed.value = false
  try {
    // Handing out the invite is all an employer sets up here, so it is the moment
    // the account counts as registered and later logins skip this page.
    await auth.completeOnboarding({})
    const invite = await createInvite()
    store.setInviteCode(invite.code)
    inviteLink.value = invite.invite_url
    modalOpen.value = true
  } catch {
    failed.value = true
  } finally {
    saving.value = false
  }
}

function fallbackInviteLink() {
  return `${window.location.origin}/auth/role?invite=${store.inviteCode}`
}
</script>

<template>
  <PageContainer>
    <template #header><AppHeader /></template>

    <div class="flex flex-1 flex-col items-center gap-6 px-6 py-8">
      <FamilyIllustration />

      <div class="w-full space-y-4">
        <ExpandableSection :title="$t('設定看護基本資訊')" />
        <ExpandableSection :title="$t('設定行事曆資訊')" />
      </div>

      <div class="mt-auto flex w-full flex-col gap-3">
        <p v-if="failed" class="text-center text-sm text-pink-600">
          {{ $t('沒有存起來，請再試一次') }}
        </p>
        <BaseButton variant="primary" :disabled="saving" @click="generateInviteCode">{{
          $t('生成動態邀請碼')
        }}</BaseButton>
        <BaseButton variant="outline" @click="router.back()">{{ $t('返回上一步驟') }}</BaseButton>
      </div>
    </div>

    <InviteCodeModal
      :open="modalOpen"
      :invite-link="inviteLink || fallbackInviteLink()"
      @close="modalOpen = false"
    />
  </PageContainer>
</template>
