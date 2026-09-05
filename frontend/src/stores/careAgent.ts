import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  createChatRoom,
  fetchCareAgent,
  fetchChatRoom,
  listChatRooms,
  saveCareAgent,
  sendChatMessage,
  submitBaseline,
  type CareAgentDto,
  type ChatMessageDto,
  type ChatRoomDto,
  type MoodWeather,
} from '@/api/chat'

export interface CareAgent {
  id: number
  careRecipientId: number
  systemPrompt: string
  temperature: number
  guardrail: string
  baselineCompletedAt: string | null
  generatedProfile: Record<string, unknown> | null
}

export interface ChatMessage {
  demo?: boolean
  kind?: 'welcome'
  id?: number
  sender: 'user' | 'ai'
  text: string
  createdAt?: string
}

export interface ChatRoom {
  demo?: boolean
  id: string
  title: string
  moodWeather?: MoodWeather | null
  messages: ChatMessage[]
}

export type Weather = 'sunny' | 'partly-cloudy' | 'cloudy' | 'rainy' | 'thunderstorm'

export interface MoodLog {
  date: string
  weather: Weather
}

export function welcomeMessage(): ChatMessage {
  return {
    kind: 'welcome',
    sender: 'ai',
    text: '歡迎回來，我在這裡陪你整理今天的照護紀錄。',
  }
}

function toAgent(agent: CareAgentDto): CareAgent {
  return {
    id: agent.id,
    careRecipientId: agent.care_recipient_id,
    systemPrompt: agent.system_prompt,
    temperature: agent.temperature,
    guardrail: agent.guardrail ?? '',
    baselineCompletedAt: agent.baseline_completed_at,
    generatedProfile: agent.generated_profile,
  }
}

function toMessage(message: ChatMessageDto): ChatMessage {
  return {
    id: message.id,
    sender: message.sender,
    text: message.text,
    createdAt: message.created_at,
  }
}

function toRoom(room: ChatRoomDto): ChatRoom {
  return {
    id: String(room.id),
    title: room.title || '新的聊天',
    moodWeather: room.mood_weather,
    messages: room.messages?.map(toMessage) ?? [],
  }
}

function toMoodWeather(weather: Weather): MoodWeather {
  if (weather === 'thunderstorm') return 'storm'
  if (weather === 'partly-cloudy') return 'cloudy'
  return weather
}

export const useCareAgentStore = defineStore('careAgent', () => {
  const agent = ref<CareAgent | null>(null)
  const chatRooms = ref<ChatRoom[]>([])
  const moodLogs = ref<MoodLog[]>([])
  const loading = ref(false)
  const sending = ref(false)
  const error = ref<string | null>(null)

  async function loadAgent() {
    loading.value = true
    error.value = null
    try {
      agent.value = toAgent(await fetchCareAgent())
      return agent.value
    } catch {
      agent.value = null
      return null
    } finally {
      loading.value = false
    }
  }

  async function loadRooms() {
    loading.value = true
    error.value = null
    try {
      chatRooms.value = (await listChatRooms()).map(toRoom)
      return chatRooms.value
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load chat rooms'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function loadRoom(id: string) {
    const room = toRoom(await fetchChatRoom(Number(id)))
    const index = chatRooms.value.findIndex((item) => item.id === room.id)
    if (index >= 0) chatRooms.value[index] = room
    else chatRooms.value.push(room)
    return room
  }

  async function createAgent(data: Omit<CareAgent, 'id' | 'baselineCompletedAt' | 'generatedProfile'>) {
    agent.value = toAgent(
      await saveCareAgent({
        care_recipient_id: data.careRecipientId,
        system_prompt: data.systemPrompt,
        temperature: data.temperature,
        guardrail: data.guardrail || null,
      }),
    )
    return agent.value
  }

  async function completeBaseline(answers: Array<{ key: string; answer: string }>) {
    agent.value = toAgent(await submitBaseline(answers))
    return agent.value
  }

  async function logMood(weather: Weather) {
    moodLogs.value.push({ date: new Date().toISOString().slice(0, 10), weather })
    const room = await createRoom(undefined, toMoodWeather(weather))
    return room
  }

  async function createRoom(title = '新的聊天', moodWeather?: MoodWeather | null) {
    const room = toRoom(await createChatRoom({ title, mood_weather: moodWeather ?? null }))
    chatRooms.value.push(room)
    return room.id
  }

  function roomById(id: string) {
    return chatRooms.value.find((r) => r.id === id)
  }

  async function sendMessage(roomId: string, text: string) {
    const room = roomById(roomId) ?? (await loadRoom(roomId))
    if (!room) return
    sending.value = true
    try {
      const turn = await sendChatMessage(Number(roomId), text)
      room.messages.push(toMessage(turn.user_message), toMessage(turn.ai_message))
    } finally {
      sending.value = false
    }
  }

  return {
    agent,
    chatRooms,
    moodLogs,
    loading,
    sending,
    error,
    loadAgent,
    loadRooms,
    loadRoom,
    createAgent,
    completeBaseline,
    logMood,
    createRoom,
    roomById,
    sendMessage,
  }
})
