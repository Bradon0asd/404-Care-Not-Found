import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAccountStore } from './account'
import { useOnboardingStore } from './onboarding'
import { translate } from '@/i18n'

export interface CareAgent {
  systemPrompt: string
  temperature: number
  guardrail: string
  baselineAnswers: number[]
}

export interface ChatMessage {
  demo?: boolean
  kind?: 'welcome'
  sender: 'user' | 'ai'
  text: string
}

export interface ChatRoom {
  demo?: boolean
  id: string
  title: string
  messages: ChatMessage[]
}

export type Weather = 'sunny' | 'partly-cloudy' | 'cloudy' | 'rainy' | 'thunderstorm'

export interface MoodLog {
  date: string
  weather: Weather
}

export function welcomeMessage(): ChatMessage {
  const account = useAccountStore()
  const indonesian = useOnboardingStore().language === 'id'
  return {
    kind: 'welcome',
    sender: 'ai',
    text: indonesian
      ? `Selamat datang, ${account.userName}!\nSaya Care Agent-mu, ${account.agentName}.\nOrang yang dirawat: ${account.careRecipient.name} (${account.careRecipient.nickname})\nKondisi: ${translate(account.careRecipient.condition)}`
      : `${account.userName}，歡迎使用【404: Care Can Be Found】\n我是你的 Care Agent ${account.agentName}\n照護對象：${account.careRecipient.name}（${account.careRecipient.nickname}）\n身體狀況：${account.careRecipient.condition}`,
  }
}

export const useCareAgentStore = defineStore('careAgent', () => {
  // Seeded so /chat shows the daily view by default during dev; use
  // the "模擬首次使用畫面" link on that page to null this out and see
  // the build flow instead.
  const agent = ref<CareAgent | null>({
    systemPrompt: '你是一位來自印尼的專業照護員，正在照顧一位 90 歲、有阿茲海默症的女性病患。',
    temperature: 0.3,
    guardrail: '不提供醫療診斷或用藥建議，遇到醫療判斷情境一律回覆「建議聯繫家屬／就醫」。',
    baselineAnswers: [2, 3, 1, 1, 1],
  })

  const chatRooms = ref<ChatRoom[]>([
    {
      id: 'seed-fall',
      title: '阿嬤早上跌倒我很擔心',
      messages: [
        welcomeMessage(),
        {
          sender: 'user',
          text: '阿嬤今天早上9:00跌倒了\n雖然有馬上送醫院、醫生也確認過沒問題\n但我還是有點自責\n總覺得是我沒有盡好盡的義務',
        },
        {
          sender: 'ai',
          text: '他怎麼會跌倒呢？\n你也辛苦了\n阿嬤現在沒事真是太好了\n你吃飯了嗎？',
        },
        {
          sender: 'user',
          text: '阿嬤趁我去上廁所的時候自己偷偷跑下床\n結果意外就發生了……我真的好自責\n現在心情不好\n另外就是我現在有點吃不下\n不過還是謝謝你',
        },
        { sender: 'ai', text: '聽起來今天很累，你已經做得很好了…' },
      ],
    },
    { id: 'seed-bath', title: '阿嬤不洗澡', messages: [welcomeMessage()] },
    { id: 'seed-breakfast', title: '阿嬤早餐吃不下', messages: [welcomeMessage()] },
  ])

  const moodLogs = ref<MoodLog[]>([])

  chatRooms.value.forEach((room) => {
    room.demo = true
    room.messages.forEach((message) => {
      message.demo = true
    })
  })

  function createAgent(data: Omit<CareAgent, 'baselineAnswers'>) {
    agent.value = { ...data, baselineAnswers: [] }
  }

  function completeBaseline(answers: number[]) {
    if (!agent.value) return
    agent.value.baselineAnswers = answers
  }

  function logMood(weather: Weather) {
    moodLogs.value.push({ date: new Date().toISOString().slice(0, 10), weather })
  }

  function createRoom(title = '新的聊天'): string {
    const id = crypto.randomUUID()
    chatRooms.value.push({ id, title, demo: title === '新的聊天', messages: [welcomeMessage()] })
    return id
  }

  function roomById(id: string) {
    return chatRooms.value.find((r) => r.id === id)
  }

  function sendMessage(roomId: string, text: string) {
    const room = roomById(roomId)
    if (!room) return
    room.messages.push({ sender: 'user', text })
    // TODO: call the real Care Agent API once the backend/NLP pipeline exists.
  }

  return {
    agent,
    chatRooms,
    moodLogs,
    createAgent,
    completeBaseline,
    logMood,
    createRoom,
    roomById,
    sendMessage,
  }
})
