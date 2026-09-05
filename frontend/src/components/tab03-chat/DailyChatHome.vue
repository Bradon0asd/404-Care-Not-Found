<script setup lang="ts">
import { computed } from 'vue'
import { useNoticeStore } from '@/stores/notice'
import { useRouter } from 'vue-router'
import WeatherMoodPicker from './WeatherMoodPicker.vue'
import ChatOrbButton from './ChatOrbButton.vue'
import ChatTopicBubble from './ChatTopicBubble.vue'
import { useCareAgentStore, type Weather } from '@/stores/careAgent'

const router = useRouter()
const store = useCareAgentStore()
const notice = useNoticeStore()

const aboveCount = computed(() => Math.ceil(store.chatRooms.length / 2))
const aboveRooms = computed(() => store.chatRooms.slice(0, aboveCount.value))
const belowRooms = computed(() => store.chatRooms.slice(aboveCount.value))

function logMood(weather: Weather) {
  store.logMood(weather)
  notice.show('心情已送出，謝謝你分享今天的感受！')
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
