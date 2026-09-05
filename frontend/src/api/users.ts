import { get, post } from './client'
import type { SessionUser } from '@/api/auth'

export interface CurrentUser extends SessionUser {
  language: string | null
  created_at: string
}

export function fetchCurrentUser() {
  return get<CurrentUser>('/api/users/me')
}

export function updateCurrentUserProfile(payload: { name?: string; language?: string }) {
  return post<CurrentUser>('/api/users/me/onboarding', payload)
}
