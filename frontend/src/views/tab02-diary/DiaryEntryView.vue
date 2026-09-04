<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import IconPencil from '@/components/tab02-diary/icons/IconPencil.vue'
import IconCalendar from '@/components/tab02-diary/icons/IconCalendar.vue'
import IconImage from '@/components/tab02-diary/icons/IconImage.vue'
import AiVoiceButton from '@/components/common/AiVoiceButton.vue'
import IconLine from '@/components/auth/icons/IconLine.vue'
import { useDiaryStore } from '@/stores/diary'
import { toMinguoDate } from '@/utils/date'

const route = useRoute()
const router = useRouter()
const diaryStore = useDiaryStore()

const day = Number(route.params.day)
const entry = diaryStore.entryForDay(day)

const editingTitle = ref(false)
const dateLabel = computed(() => toMinguoDate(new Date(entry.date)))

const fileInput = ref<HTMLInputElement | null>(null)

function pickImage() {
  fileInput.value?.click()
}

function onImageSelected(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  entry.imageUrl = URL.createObjectURL(file)
}

function removeImage() {
  entry.imageUrl = null
  if (fileInput.value) fileInput.value.value = ''
}

// TODO: wire up once the Indonesian ASR service is available.
function startVoiceInput() {
  console.info('AI 語音辨識 — 待接 ASR 服務')
}

function save(visibility: 'private' | 'shared') {
  entry.visibility = visibility
  router.push('/diary')
}
</script>

<template>
  <PageContainer>
    <template #header><AppHeader /></template>

    <div class="flex-1 space-y-4 px-4 py-4">
      <div class="flex justify-center">
        <div class="flex h-16 w-16 flex-col items-center justify-center rounded-full border-2 border-accent bg-accent text-sm font-bold text-ink-950">
          <span class="text-[10px] font-normal">Day</span>
          {{ day }}
        </div>
      </div>

      <div class="flex items-center gap-2 rounded-xl bg-ink-200 px-4 py-3">
        <span class="text-sm text-ink-700">日記主題</span>
        <input
          v-if="editingTitle"
          v-model="entry.title"
          type="text"
          class="flex-1 bg-transparent text-sm text-ink-950 outline-none"
          placeholder="輸入主題"
          @blur="editingTitle = false"
        />
        <span v-else class="flex-1 text-sm text-ink-950">{{ entry.title }}</span>
        <button type="button" aria-label="編輯主題" @click="editingTitle = true">
          <IconPencil class="h-4 w-4 text-ink-600" />
        </button>
      </div>

      <div class="flex items-center gap-2 rounded-xl bg-ink-200 px-4 py-3">
        <span class="text-sm text-ink-700">日記日期</span>
        <IconCalendar class="h-4 w-4 text-ink-600" />
        <span class="flex-1 text-sm text-ink-950">{{ dateLabel }}</span>
      </div>

      <div class="rounded-xl bg-ink-200 p-4">
        <div class="mb-2 flex items-center justify-between">
          <span class="text-sm text-ink-700">日記內容</span>
          <AiVoiceButton @click="startVoiceInput" />
        </div>
        <textarea
          v-model="entry.content"
          rows="5"
          placeholder="今天想分享什麼呢？&#10;阿嬤今天有乖乖吃飯嗎？&#10;印尼家人的健康狀況還好嗎？小孩今天學校發生什麼有趣的事情？&#10;備註：除了文字輸入外，也可點選右上方「AI 語音辨識」新增日記內容！"
          class="w-full bg-transparent text-sm text-ink-950 placeholder:text-ink-600"
        ></textarea>
      </div>

      <div>
        <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onImageSelected" />
        <div v-if="entry.imageUrl" class="relative w-fit">
          <img :src="entry.imageUrl" alt="日記附圖" class="h-24 w-24 rounded-lg object-cover" />
          <button
            type="button"
            class="absolute -top-2 -right-2 flex h-5 w-5 items-center justify-center rounded-full bg-ink-950 text-xs text-white"
            aria-label="移除圖片"
            @click="removeImage"
          >
            ×
          </button>
        </div>
        <div v-else class="flex items-center gap-3">
          <button
            type="button"
            class="flex h-10 w-10 items-center justify-center rounded-lg bg-ink-200 text-ink-600"
            aria-label="新增圖片"
            @click="pickImage"
          >
            +
          </button>
          <button
            type="button"
            class="flex h-10 w-10 items-center justify-center rounded-lg bg-ink-200 text-ink-600"
            aria-label="選擇圖片"
            @click="pickImage"
          >
            <IconImage class="h-5 w-5" />
          </button>
          <span class="rounded-full bg-red-600 px-3 py-1 text-xs text-white">最多支援一張圖片</span>
        </div>
      </div>

      <div class="flex gap-3 pt-2">
        <div class="flex-1"><BaseButton variant="primary" @click="save('private')">新增日記（僅自己）</BaseButton></div>
        <div class="flex-1">
          <BaseButton variant="line" @click="save('shared')">
            <IconLine />
            分享給 Line 朋友
          </BaseButton>
        </div>
      </div>
      <BaseButton variant="outline" @click="router.back()">取消</BaseButton>

      <p class="text-center text-xs text-ink-600">提醒：平台絕不會擅自分享你的日記內容，請放心抒發</p>
    </div>

    <template #footer><BottomTabBar /></template>
  </PageContainer>
</template>
