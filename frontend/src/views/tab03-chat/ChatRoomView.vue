<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PageContainer from '@/components/layout/PageContainer.vue'
import ChatRoomHeader from '@/components/tab03-chat/ChatRoomHeader.vue'
import ChatMessageBubble from '@/components/tab03-chat/ChatMessageBubble.vue'
import ChatInputBar from '@/components/tab03-chat/ChatInputBar.vue'
import { useCareAgentStore } from '@/stores/careAgent'

const route = useRoute()
const router = useRouter()
const store = useCareAgentStore()

const room = computed(() => store.roomById(route.params.id as string))

if (!room.value) {
  router.replace('/chat')
}

function send(text: string) {
  if (!room.value) return
  store.sendMessage(room.value.id, text)
}
</script>

<template>
  <PageContainer v-if="room">
    <template #header>
      <ChatRoomHeader
        :title="room.demo ? $t(room.title) : room.title"
        @update:title="
          (title) => {
            if (room) {
              room.title = title
              room.demo = false
            }
          }
        "
      />
    </template>

    <div class="flex flex-1 flex-col gap-3 px-4 py-4">
      <ChatMessageBubble v-for="(message, i) in room.messages" :key="i" :message="message" />
    </div>

    <template #footer><ChatInputBar @send="send" /></template>
  </PageContainer>
</template>
