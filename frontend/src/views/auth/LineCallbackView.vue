<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const failed = ref(false)

// The backend finishes LINE Login on its own domain and sends the browser here,
// so the only thing left to do is read back the session it just opened.
onMounted(async () => {
  if (route.query.error) {
    router.replace({ path: '/auth/role', query: { error: String(route.query.error) } })
    return
  }

  try {
    const user = await auth.loadSession()
    if (!user) {
      router.replace({ path: '/auth/role', query: { error: 'SESSION_NOT_FOUND' } })
      return
    }
    // Already registered means straight to the app; the backend owns that call.
    if (!user.needs_onboarding) {
      router.replace('/dashboard')
    } else if (user.role === 'owner') {
      router.replace('/auth/employer/setup')
    } else {
      router.replace('/auth/caregiver/onboarding')
    }
  } catch {
    failed.value = true
  }
})
</script>

<template>
  <PageContainer>
    <template #header><AppHeader /></template>

    <div class="flex flex-1 flex-col items-center justify-center gap-3 px-6 text-center">
      <p v-if="!failed" class="text-sm text-ink-700">{{ $t('正在為你登入…') }}</p>
      <template v-else>
        <p class="text-sm text-ink-700">{{ $t('連不到伺服器，請稍後再試一次') }}</p>
        <button
          class="text-sm font-bold text-pink-600 underline"
          @click="router.replace('/auth/role')"
        >
          {{ $t('返回上一步驟') }}
        </button>
      </template>
    </div>
  </PageContainer>
</template>
