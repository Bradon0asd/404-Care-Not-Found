import { get, post } from './client'

export type VitalSignType =
  | 'blood_pressure'
  | 'blood_glucose'
  | 'heart_rate'
  | 'oxygen_saturation'
  | 'temperature'
  | 'respiratory_rate'

export interface VitalSignDto {
  id: number
  care_recipient_id: number
  creator_id: number
  vital_type: VitalSignType
  value: number
  secondary_value: number | null
  unit: string
  measured_at: string
  note: string | null
  created_at: string
}

export interface VitalSignPayload {
  vital_type: VitalSignType
  value: number
  secondary_value?: number | null
  measured_at: string
  note?: string | null
}

export interface DashboardMetricDto {
  unit: string
  latest: { value: number; secondary_value: number | null; measured_at: string } | null
  current_average: { value: number | null; secondary_value: number | null } | null
  previous_average: { value: number | null; secondary_value: number | null } | null
  difference: { value: number | null; secondary_value: number | null } | null
  change_text: string | null
}

export type DashboardDto = Record<VitalSignType, DashboardMetricDto> & {
  period: {
    current_start: string
    current_end: string
    previous_start: string
    previous_end: string
  }
}

export function fetchVitalDashboard(recipientId: number) {
  return get<DashboardDto>(`/api/care-recipients/${recipientId}/dashboard`)
}

export function listVitalSigns(recipientId: number, vitalType?: VitalSignType) {
  const query = vitalType ? `?vital_type=${vitalType}` : ''
  return get<VitalSignDto[]>(`/api/care-recipients/${recipientId}/vital-signs${query}`)
}

export function createVitalSign(recipientId: number, payload: VitalSignPayload) {
  return post<VitalSignDto>(`/api/care-recipients/${recipientId}/vital-signs`, payload)
}
