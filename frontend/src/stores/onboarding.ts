import { defineStore } from 'pinia'
import { ref } from 'vue'

export type UserRole = 'caregiver' | 'employer'
export type Language = 'id' | 'zh'

function initialLanguage(): Language {
  try {
    return localStorage.getItem('care-ui-language') === 'id' ? 'id' : 'zh'
  } catch {
    return 'zh'
  }
}

export const useOnboardingStore = defineStore('onboarding', () => {
  const role = ref<UserRole | null>(null)
  const language = ref<Language>(initialLanguage())
  const arrivalDate = ref<string>(new Date().toISOString().slice(0, 10))
  const careRecipientOrdinal = ref(1)
  const inviteCode = ref<string | null>(null)

  function selectRole(next: UserRole) {
    role.value = next
  }

  function setInviteCode(code: string) {
    inviteCode.value = code
  }

  return {
    role,
    language,
    arrivalDate,
    careRecipientOrdinal,
    inviteCode,
    selectRole,
    setInviteCode,
  }
})
