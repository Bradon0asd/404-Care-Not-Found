<script setup lang="ts">
import { onMounted, ref } from 'vue'
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
const savingLanguage = ref(false)

onMounted(() => {
  void account.loadAccount()
})

async function updateLanguage(value: typeof language.value) {
  if (savingLanguage.value) return
  savingLanguage.value = true
  try {
    await account.updateLanguage(value)
    languageModalOpen.value = false
  } finally {
    savingLanguage.value = false
  }
}

async function logout() {
  await account.logout()
  router.push('/auth/role')
}
</script>

<template>
  <PageContainer>
    <template #header><AppHeader /></template>

    <div class="account-tree-space flex min-h-0 flex-1 items-center justify-center">
      <CareTreeHeader
        :user-name="account.userName"
        :picture-url="account.pictureUrl"
        :role="account.roleLabel"
        @language="languageModalOpen = true"
        @logout="logout"
        @plans="router.push('/account/plans')"
      />
    </div>

    <LanguageModal
      :open="languageModalOpen"
      :language="language"
      @close="languageModalOpen = false"
      @update:language="updateLanguage"
    />
    <template #footer><BottomTabBar /></template>
  </PageContainer>
</template>

<style scoped>
.account-tree-space {
  container-type: size;
}
</style>
