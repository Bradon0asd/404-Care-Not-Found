import { get, post } from './client'

export type MoodWeather = 'sunny' | 'cloudy' | 'rainy' | 'storm'

export interface CareAgentDto {
  id: number
  user_id: number
  care_recipient_id: number
  system_prompt: string
  temperature: number
  guardrail: string | null
  generated_profile: Record<string, unknown> | null
  baseline_completed_at: string | null
  created_at: string
  updated_at: string
}

export interface ChatRoomDto {
  id: number
  user_id: number
  care_agent_id: number
  title: string | null
  mood_weather: MoodWeather | null
  created_at: string
  updated_at: string
  messages?: ChatMessageDto[]
}

export interface ChatMessageDto {
  id: number
  room_id: number
  sender: 'user' | 'ai'
  text: string
  created_at: string
}

export function fetchCareAgent() {
  return get<CareAgentDto>('/api/chat/agent')
}

export function saveCareAgent(payload: {
  care_recipient_id: number
  system_prompt: string
  temperature: number
  guardrail?: string | null
}) {
  return post<CareAgentDto>('/api/chat/agent', payload)
}

export function fetchBaselineQuestions() {
  return get<{ questions: unknown[] }>('/api/chat/agent/baseline')
}

export function submitBaseline(
  answers: Array<{
    key: string
    answer: string
  }>,
) {
  return post<CareAgentDto>('/api/chat/agent/baseline', { answers })
}

export function listChatRooms() {
  return get<ChatRoomDto[]>('/api/chat/rooms')
}

export function createChatRoom(payload: { title?: string | null; mood_weather?: MoodWeather | null }) {
  return post<ChatRoomDto>('/api/chat/rooms', payload)
}

export function fetchChatRoom(id: number) {
  return get<ChatRoomDto>(`/api/chat/rooms/${id}`)
}

export function sendChatMessage(id: number, text: string) {
  return post<{ user_message: ChatMessageDto; ai_message: ChatMessageDto }>(
    `/api/chat/rooms/${id}/messages`,
    { text },
  )
}
