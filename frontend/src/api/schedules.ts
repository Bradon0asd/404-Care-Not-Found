import { del, get, patch, post } from './client'

export type ScheduleType = 'weekday' | 'weekend'

export interface CareScheduleDto {
  id: number
  care_recipient_id: number
  creator_id: number
  schedule_type: ScheduleType
  weekday: number | null
  start_time: string
  title: string
  description: string | null
  created_at: string
  updated_at: string
}

export interface CareSchedulePayload {
  schedule_type: ScheduleType
  weekday: number
  start_time: string
  title: string
  description?: string | null
}

export function listSchedules(recipientId: number, scheduleType?: ScheduleType) {
  const query = scheduleType ? `?schedule_type=${scheduleType}` : ''
  return get<CareScheduleDto[]>(`/api/care-recipients/${recipientId}/schedules${query}`)
}

export function createSchedule(recipientId: number, payload: CareSchedulePayload) {
  return post<CareScheduleDto>(`/api/care-recipients/${recipientId}/schedules`, payload)
}

export function updateSchedule(id: number, payload: Partial<CareSchedulePayload>) {
  return patch<CareScheduleDto>(`/api/schedules/${id}`, payload)
}

export function deleteSchedule(id: number) {
  return del<null>(`/api/schedules/${id}`)
}
