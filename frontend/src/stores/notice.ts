import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useNoticeStore = defineStore('notice', () => {
  const message = ref('')
  let timer: ReturnType<typeof setTimeout> | undefined

  function dismiss() {
    clearTimeout(timer)
    message.value = ''
  }

  function show(text: string) {
    clearTimeout(timer)
    message.value = text
    timer = setTimeout(dismiss, 3000)
  }

  return { message, show, dismiss }
})
