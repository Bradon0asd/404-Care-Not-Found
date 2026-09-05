import { defineStore } from 'pinia'
import { ref } from 'vue'

export type Plan = 'free' | 'basic' | 'premium'

export const useAccountStore = defineStore('account', () => {
  const userName = ref('Mia')
  const employer = ref({ id: 'employer-001', name: '林小姐' })
  const careRecipient = ref({
    name: '林奶奶',
    nickname: '阿嬤',
    condition: '90 歲，患有阿茲海默症，日常起居需要協助。',
  })
  const agentName = ref('小暖')
  const plan = ref<Plan>('free')

  return { userName, employer, careRecipient, agentName, plan }
})
