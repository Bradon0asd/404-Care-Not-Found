import { defineStore } from 'pinia'
import { ref } from 'vue'

export type Plan = 'free' | 'basic' | 'premium'

export const useAccountStore = defineStore('account', () => {
  const userName = ref('Mia')
  const plan = ref<Plan>('free')

  return { userName, plan }
})
