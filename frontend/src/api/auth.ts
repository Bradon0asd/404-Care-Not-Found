import { get, post } from './client'
import type { UserRole } from '@/stores/onboarding'

// The UI speaks caregiver/employer; the backend speaks nurse/owner.
export type BackendRole = 'nurse' | 'owner'

const ROLE_TO_BACKEND: Record<UserRole, BackendRole> = {
  caregiver: 'nurse',
  employer: 'owner',
}

export const ROLE_FROM_BACKEND: Record<BackendRole, UserRole> = {
  nurse: 'caregiver',
  owner: 'employer',
}

export interface SessionUser {
  id: number
  line_id: string
  name: string | null
  role: BackendRole
  pair_user_id: number | null
  // The backend decides whether this account has finished its one-off setup.
  needs_onboarding: boolean
}

/** Ask the backend for the LINE consent URL to send the browser to. */
export async function startLineLogin(role: UserRole) {
  const data = await post<{ authorization_url: string }>('/api/auth/line/start', {
    role: ROLE_TO_BACKEND[role],
  })
  return data.authorization_url
}

export function fetchSession() {
  return get<SessionUser>('/api/auth/session')
}

/** Mark the one-off setup form as done and save what it collected. */
export function completeOnboarding(payload: { name?: string; language?: string }) {
  return post<SessionUser>('/api/users/me/onboarding', payload)
}

export function logout() {
  return post<null>('/api/auth/logout')
}
