import { get, patch, post } from './client'

export interface CareRecipientDto {
  id: number
  name: string
  owner_id: number
  nurse_id: number | null
  created_at: string
}

export function listCareRecipients() {
  return get<CareRecipientDto[]>('/api/care-recipients')
}

export function createCareRecipient(payload: { name: string }) {
  return post<CareRecipientDto>('/api/care-recipients', payload)
}

export function updateCareRecipient(id: number, payload: { name?: string }) {
  return patch<CareRecipientDto>(`/api/care-recipients/${id}`, payload)
}
