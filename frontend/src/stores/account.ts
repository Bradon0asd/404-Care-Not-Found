import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { ROLE_FROM_BACKEND } from '@/api/auth'
import { fetchCurrentUser, updateCurrentUserProfile } from '@/api/users'
import type { CurrentUser } from '@/api/users'
import type { Language } from '@/stores/onboarding'
import { useAuthStore } from '@/stores/auth'
import { useOnboardingStore } from '@/stores/onboarding'

export type Plan = 'free' | 'basic' | 'premium'

export const useAccountStore = defineStore('account', () => {
  const user = ref<CurrentUser | null>(null)
  const loading = ref(false)
  const plan = ref<Plan>('free')

  const auth = useAuthStore()
  const onboarding = useOnboardingStore()

  const userName = computed(() => user.value?.name || auth.user?.name || 'CareTree')
  const pictureUrl = computed(() => user.value?.picture_url || auth.user?.picture_url || null)
  const role = computed(() => {
    const backendRole = user.value?.role ?? auth.user?.role
    return backendRole ? ROLE_FROM_BACKEND[backendRole] : null
  })
  const roleLabel = computed(() => {
    if (role.value === 'employer') return '雇主'
    if (role.value === 'caregiver') return '照顧者'
    return ''
  })

  const employer = ref({ id: 'employer-001', name: '尚未連結雇主' })
  const careRecipient = ref({
    name: '尚未建立照護對象',
    nickname: '',
    condition: '',
  })
  const agentName = ref('Care Agent')

  async function loadAccount() {
    loading.value = true
    try {
      user.value = await fetchCurrentUser()
      auth.user = user.value
      if (user.value.language === 'id' || user.value.language === 'zh') {
        onboarding.language = user.value.language
      }
      return user.value
    } finally {
      loading.value = false
    }
  }

  async function updateLanguage(language: Language) {
    user.value = await updateCurrentUserProfile({ language })
    auth.user = user.value
    onboarding.language = language
    return user.value
  }

  async function logout() {
    await auth.logout()
    user.value = null
  }

  return {
    user,
    loading,
    userName,
    pictureUrl,
    role,
    roleLabel,
    employer,
    careRecipient,
    agentName,
    plan,
    loadAccount,
    updateLanguage,
    logout,
  }
})
