import { post } from './client'

export interface InviteDto {
  id: number
  owner_id: number
  nurse_id: number | null
  code: string
  is_revoked: boolean
  invite_url: string
  created_at: string
}

export interface InviteEntryDto {
  id: number
  line_id: string
  name: string | null
  language: string | null
  role: 'nurse'
  pair_user_id: number | null
  needs_onboarding: boolean
  needs_profile: boolean
}

export function createInvite() {
  return post<InviteDto>('/api/invites')
}

export function enterInvite(code: string) {
  return post<InviteEntryDto>(`/api/invites/${code}/enter`)
}

export function completeInviteProfile(code: string, payload: { name?: string; language?: string }) {
  return post<InviteEntryDto>(`/api/invites/${code}/profile`, payload)
}
