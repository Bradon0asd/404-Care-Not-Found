import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { ROLE_FROM_BACKEND } from '@/api/auth'
import { listCareRecipients, type CareRecipientDto } from '@/api/careRecipients'
import { fetchCurrentUser, fetchUser, updateCurrentUserProfile } from '@/api/users'
import type { CurrentUser } from '@/api/users'
import type { Language } from '@/stores/onboarding'
import { useAuthStore } from '@/stores/auth'
import { useOnboardingStore } from '@/stores/onboarding'

export type Plan = 'free' | 'basic' | 'premium'

export const useAccountStore = defineStore('account', () => {
  const user = ref<CurrentUser | null>(null)
  const recipients = ref<CareRecipientDto[]>([])
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
    if (role.value === 'caregiver') return '照服員'
    return ''
  })

  const employer = ref({ id: 'employer-001', name: '尚未連結雇主' })
  const careRecipient = ref({
    id: null as number | null,
    name: '尚未建立照護對象',
    nickname: '',
    condition: '',
  })
  const currentCareRecipientId = computed(() => careRecipient.value.id)
  const agentName = ref('Care Agent')

  async function loadAccount() {
    loading.value = true
    try {
      user.value = await fetchCurrentUser()
      auth.user = user.value
      await Promise.all([loadRecipients(), loadPairUser()])
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
    recipients.value = []
  }

  async function loadRecipients() {
    recipients.value = await listCareRecipients()
    const first = recipients.value[0]
    if (first) {
      careRecipient.value = {
        ...careRecipient.value,
        id: first.id,
        name: first.name,
      }
    }
    return recipients.value
  }

  async function loadPairUser() {
    if (!user.value?.pair_user_id) return null
    try {
      const pair = await fetchUser(user.value.pair_user_id)
      employer.value = {
        id: String(pair.id),
        name: pair.name || employer.value.name,
      }
      return pair
    } catch {
      return null
    }
  }

  return {
    user,
    recipients,
    loading,
    userName,
    pictureUrl,
    role,
    roleLabel,
    employer,
    careRecipient,
    currentCareRecipientId,
    agentName,
    plan,
    loadAccount,
    loadRecipients,
    updateLanguage,
    logout,
  }
})
