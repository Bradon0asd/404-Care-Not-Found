<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useOnboardingStore } from '@/stores/onboarding'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import ExpandableSection from '@/components/common/ExpandableSection.vue'
import FamilyIllustration from '@/components/auth/FamilyIllustration.vue'
import InviteCodeModal from '@/components/auth/InviteCodeModal.vue'

const router = useRouter()
const store = useOnboardingStore()

const modalOpen = ref(false)

function generateInviteCode() {
  const code = crypto.randomUUID().slice(0, 8)
  store.setInviteCode(code)
  modalOpen.value = true
}

const inviteLink = () => `${window.location.origin}/auth/role?invite=${store.inviteCode}`
</script>

<template>
  <PageContainer>
    <template #header><AppHeader /></template>

    <div class="flex flex-1 flex-col items-center gap-6 px-6 py-8">
      <FamilyIllustration />

      <div class="w-full space-y-4">
        <ExpandableSection title="設定看護基本資訊" />
        <ExpandableSection title="設定行事曆資訊" />
      </div>

      <div class="mt-auto flex w-full flex-col gap-3">
        <BaseButton variant="primary" @click="generateInviteCode">生成動態邀請碼</BaseButton>
        <BaseButton variant="outline" @click="router.back()">返回上一步驟</BaseButton>
      </div>
    </div>

    <InviteCodeModal :open="modalOpen" :invite-link="inviteLink()" @close="modalOpen = false" />
  </PageContainer>
</template>
