import type { App } from 'vue'
import { watch } from 'vue'
import { useOnboardingStore } from '@/stores/onboarding'
import { id } from './id'

export function translate(value: unknown, params: Record<string, unknown> = {}): string {
  const text = String(value ?? '')
  const key = text.trim()
  const translated =
    useOnboardingStore().language === 'id' && Object.hasOwn(id, key) ? id[key]! : text
  return translated.replace(/\{(\w+)\}/g, (match, name: string) =>
    Object.hasOwn(params, name) ? String(params[name]) : match,
  )
}

export function installI18n(app: App) {
  const settings = useOnboardingStore()
  app.config.globalProperties.$t = translate
  watch(
    () => settings.language,
    (language) => {
      document.documentElement.lang = language === 'id' ? 'id' : 'zh-Hant'
      document.title = language === 'id' ? 'Care Can Be Found' : '照見 Care Can Be Found'
      try {
        localStorage.setItem('care-ui-language', language)
      } catch {
        /* Storage may be unavailable. */
      }
    },
    { immediate: true },
  )
}

declare module 'vue' {
  interface ComponentCustomProperties {
    $t: typeof translate
  }
}
