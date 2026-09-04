<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'
import CareTreeHeader from '@/components/tab05-account/CareTreeHeader.vue'
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
    <template #header><AppHeader /></template>

    <div class="flex-1 py-6">
      <CareTreeHeader
        :user-name="account.userName"
        role="看護端"
        @language="languageModalOpen = true"
        @logout="logout"
        @plans="router.push('/account/plans')"
      />
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
    <template #footer><BottomTabBar /></template>
  </PageContainer>
</template>
