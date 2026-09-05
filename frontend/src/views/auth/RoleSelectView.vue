<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useOnboardingStore } from '@/stores/onboarding'
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
const { role } = storeToRefs(store)

// Arriving via an employer's invite link means the visitor is the caregiver being invited.
onMounted(() => {
  if (route.query.invite) {
    store.selectRole('caregiver')
  }
})

function handleLineRegister() {
  if (!role.value) return
  if (role.value === 'caregiver') {
    router.push('/auth/caregiver/onboarding')
  } else {
    router.push('/auth/employer/setup')
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
        <BaseButton variant="line" :disabled="!role" @click="handleLineRegister">
          <IconLine />{{ $t('使用 LINE 註冊') }}</BaseButton
        >
        <BaseButton variant="outline" @click="router.back()">{{ $t('返回上一步驟') }}</BaseButton>
      </div>
    </div>
  </PageContainer>
</template>
