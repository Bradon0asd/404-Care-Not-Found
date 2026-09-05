<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'
import { useRouter } from 'vue-router'
import WeatherMoodPicker from './WeatherMoodPicker.vue'
import ChatOrbButton from './ChatOrbButton.vue'
import ChatTopicBubble from './ChatTopicBubble.vue'
import { useCareAgentStore, type Weather } from '@/stores/careAgent'

const router = useRouter()
const store = useCareAgentStore()
const showMoodNotice = ref(false)
let noticeTimer: ReturnType<typeof setTimeout> | undefined

onBeforeUnmount(() => clearTimeout(noticeTimer))

const aboveCount = computed(() => Math.ceil(store.chatRooms.length / 2))
const aboveRooms = computed(() => store.chatRooms.slice(0, aboveCount.value))
const belowRooms = computed(() => store.chatRooms.slice(aboveCount.value))

function logMood(weather: Weather) {
  store.logMood(weather)
  clearTimeout(noticeTimer)
  showMoodNotice.value = true
  noticeTimer = setTimeout(() => {
    showMoodNotice.value = false
  }, 3000)
}

function openRoom(id: string) {
  router.push(`/chat/room/${id}`)
}

function startNewChat() {
  const id = store.createRoom()
  router.push(`/chat/room/${id}`)
}
</script>

<template>
  <Teleport to="body">
    <div
      class="pointer-events-none fixed top-16 right-4 left-4 z-[60] flex justify-center"
      role="status"
      aria-live="polite"
      aria-atomic="true"
    >
      <Transition name="mood-notice">
        <div
          v-if="showMoodNotice"
          class="flex max-w-sm items-center gap-3 rounded-2xl border border-pink-200 bg-white px-5 py-4 text-sm font-bold text-ink-800 shadow-lg"
        >
          <svg
            aria-hidden="true"
            class="h-7 w-7 shrink-0 text-pink-600"
            viewBox="0 0 24 24"
            fill="none"
          >
            <circle cx="12" cy="12" r="10" fill="currentColor" fill-opacity=".15" />
            <path
              d="m7 12 3 3 7-7"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          <span>{{ $t('心情已送出，謝謝你分享今天的感受！') }}</span>
        </div>
      </Transition>
    </div>
  </Teleport>
  <div class="pt-4">
    <WeatherMoodPicker @submit="logMood" />
  </div>

  <div class="flex flex-1 flex-col justify-center gap-3 px-6 py-6">
    <div class="flex flex-col gap-3">
      <ChatTopicBubble
        v-for="(room, i) in aboveRooms"
        :key="room.id"
        :title="room.demo ? $t(room.title) : room.title"
        :align="i % 2 === 0 ? 'right' : 'left'"
        @click="openRoom(room.id)"
      />
    </div>

    <div class="flex justify-center py-2">
      <ChatOrbButton @click="startNewChat" />
    </div>

    <div class="flex flex-col gap-3">
      <ChatTopicBubble
        v-for="(room, i) in belowRooms"
        :key="room.id"
        :title="room.demo ? $t(room.title) : room.title"
        :align="i % 2 === 0 ? 'left' : 'right'"
        @click="openRoom(room.id)"
      />
    </div>
  </div>
</template>

<style scoped>
.mood-notice-enter-active,
.mood-notice-leave-active {
  transition:
    opacity 220ms ease,
    transform 220ms ease;
}
.mood-notice-enter-from,
.mood-notice-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}
@media (prefers-reduced-motion: reduce) {
  .mood-notice-enter-active,
  .mood-notice-leave-active {
    transition: none;
  }
}
</style>
