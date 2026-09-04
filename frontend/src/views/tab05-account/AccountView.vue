<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'
import CareTreeHeader from '@/components/tab05-account/CareTreeHeader.vue'
import AccountBranchLink from '@/components/tab05-account/AccountBranchLink.vue'
import LanguageModal from '@/components/tab05-account/LanguageModal.vue'
import { useAccountStore } from '@/stores/account'
import { useOnboardingStore } from '@/stores/onboarding'

const router = useRouter()
const account = useAccountStore()
const onboarding = useOnboardingStore()
const { language } = storeToRefs(onboarding)

const languageModalOpen = ref(false)

function logout() {
  router.push('/auth/role')
}
</script>

<template>
  <PageContainer>
    <AppHeader />

    <div class="flex-1 px-6 py-6">
      <CareTreeHeader :user-name="account.userName" role="看護端" />

      <div class="mt-2 flex flex-col items-start gap-6 pl-6">
        <AccountBranchLink label="變更語言" @click="languageModalOpen = true" />
        <AccountBranchLink label="登出" @click="logout" />
        <AccountBranchLink label="訂閱方案" accent @click="router.push('/account/plans')" />
      </div>
    </div>

    <LanguageModal
      :open="languageModalOpen"
      :language="language"
      @close="languageModalOpen = false"
      @update:language="
        (v) => {
          language = v
          languageModalOpen = false
        }
      "
    />
    <BottomTabBar />
  </PageContainer>
</template>
