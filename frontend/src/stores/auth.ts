import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import {
  completeOnboarding as completeOnboardingRequest,
  fetchSession,
  logout as logoutRequest,
  ROLE_FROM_BACKEND,
} from '@/api/auth'
import type { SessionUser } from '@/api/auth'
import { ApiError } from '@/api/client'
import { useOnboardingStore } from '@/stores/onboarding'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<SessionUser | null>(null)
  const loading = ref(false)

  const isLoggedIn = computed(() => user.value !== null)
  // Whose call this is belongs to the backend: a LINE signup already carries a
  // display name, so nothing the frontend can see says "new account".
  const needsOnboarding = computed(() => user.value?.needs_onboarding ?? false)

  /** Read the session cookie's user. Returns null when nobody is logged in. */
  async function loadSession() {
    loading.value = true
    try {
      user.value = await fetchSession()
      // Keep the role the rest of the app already reads in sync with the real session.
      useOnboardingStore().selectRole(ROLE_FROM_BACKEND[user.value.role])
      return user.value
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        user.value = null
        return null
      }
      throw error
    } finally {
      loading.value = false
    }
  }

  async function completeOnboarding(payload: { name?: string; language?: string }) {
    user.value = await completeOnboardingRequest(payload)
    return user.value
  }

  async function logout() {
    await logoutRequest()
    user.value = null
  }

  return { user, loading, isLoggedIn, needsOnboarding, loadSession, completeOnboarding, logout }
})
