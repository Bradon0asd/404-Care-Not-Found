<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import AiVoiceButton from '@/components/common/AiVoiceButton.vue'
import IconPencil from '@/components/tab02-diary/icons/IconPencil.vue'
import IconImage from '@/components/tab02-diary/icons/IconImage.vue'
import NoteLevelPicker from '@/components/tab04-board/NoteLevelPicker.vue'
import NotePermissionModal from '@/components/tab04-board/NotePermissionModal.vue'
import { useBoardStore, type NoteLevel, type NoteVisibility } from '@/stores/board'

const router = useRouter()
const store = useBoardStore()

const level = ref<NoteLevel>('normal')
const title = ref('')
const tag = ref('')
const content = ref('')
const imageUrl = ref<string | null>(null)
const permissionModalOpen = ref(false)

const fileInput = ref<HTMLInputElement | null>(null)

function pickImage() {
  fileInput.value?.click()
}

function onImageSelected(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  imageUrl.value = URL.createObjectURL(file)
}

// TODO: wire up once the Indonesian ASR service is available.
function startVoiceInput() {
  console.info('便利貼語音輸入 — 待接 ASR 服務')
}

function openPermissionModal() {
  if (!content.value.trim()) return
  permissionModalOpen.value = true
}

function publish(visibility: NoteVisibility) {
  store.addNote({
    level: level.value,
    title: title.value,
    tag: tag.value,
    content: content.value,
    imageUrl: imageUrl.value,
    visibility,
  })
  permissionModalOpen.value = false
  router.push('/board')
}
</script>

<template>
  <PageContainer>
    <template #header><AppHeader /></template>

    <div class="flex-1 space-y-4 px-4 py-4">
      <NoteLevelPicker v-model="level" />

      <div class="space-y-3 rounded-xl bg-ink-200 p-4">
        <label
          class="flex items-center gap-2 rounded-md focus-within:ring-2 focus-within:ring-pink-500"
        >
          <span class="text-sm text-ink-700">{{ $t('便利貼標題') }}</span>
          <input
            v-model="title"
            type="text"
            :placeholder="$t('輸入標題')"
            class="min-w-0 flex-1 bg-transparent text-sm text-ink-950 outline-none"
          />
          <IconPencil aria-hidden="true" class="h-4 w-4 shrink-0 text-ink-600" />
        </label>
        <label
          class="flex items-center gap-2 rounded-md focus-within:ring-2 focus-within:ring-pink-500"
        >
          <span class="text-sm text-ink-700">{{ $t('設定標籤類別') }}</span>
          <input
            v-model="tag"
            type="text"
            :placeholder="$t('例如：請假／照護／費用')"
            class="min-w-0 flex-1 bg-transparent text-sm text-ink-950 outline-none placeholder:text-ink-600"
          />
          <IconPencil aria-hidden="true" class="h-4 w-4 shrink-0 text-ink-600" />
        </label>
      </div>

      <div class="rounded-xl bg-ink-200 p-4">
        <div class="mb-2 flex items-center justify-between">
          <span class="text-sm text-ink-700">{{ $t('便利貼內容') }}</span>
          <AiVoiceButton @click="startVoiceInput" />
        </div>
        <textarea
          v-model="content"
          rows="5"
          :placeholder="
            $t(
              '今天想和雇主分享什麼呢？\n例如：阿嬤今天9:00開始就一直吵著要下床，一路吵到下午15:00自己累了睡著。\n備註：除了文字輸入外，也可點選右上方「AI 語音辨識」新增便利貼內容！',
            )
          "
          class="w-full bg-transparent text-sm text-ink-950 placeholder:text-ink-600"
        ></textarea>
      </div>

      <div>
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          class="hidden"
          @change="onImageSelected"
        />
        <div v-if="imageUrl" class="relative w-fit">
          <img :src="imageUrl" :alt="$t('便利貼附圖')" class="h-24 w-24 rounded-lg object-cover" />
          <button
            type="button"
            class="absolute -top-2 -right-2 flex h-5 w-5 items-center justify-center rounded-full bg-ink-950 text-xs text-white"
            :aria-label="$t('移除圖片')"
            @click="imageUrl = null"
          >
            ×
          </button>
        </div>
        <div v-else class="flex items-center gap-3">
          <button
            type="button"
            class="flex h-10 w-10 items-center justify-center rounded-lg bg-ink-200 text-ink-600"
            :aria-label="$t('新增圖片')"
            @click="pickImage"
          >
            +
          </button>
          <button
            type="button"
            class="flex h-10 w-10 items-center justify-center rounded-lg bg-ink-200 text-ink-600"
            :aria-label="$t('選擇圖片')"
            @click="pickImage"
          >
            <IconImage class="h-5 w-5" />
          </button>
        </div>
      </div>

      <BaseButton variant="primary" :disabled="!content.trim()" @click="openPermissionModal">{{
        $t('設定便利貼權限 ➨ 發布便利貼')
      }}</BaseButton>
      <BaseButton variant="outline" class="cancel-note" @click="router.back()">{{
        $t('取消')
      }}</BaseButton>
    </div>

    <NotePermissionModal
      :open="permissionModalOpen"
      @close="permissionModalOpen = false"
      @publish="publish"
    />
    <template #footer><BottomTabBar /></template>
  </PageContainer>
</template>

<style scoped>
.cancel-note {
  border-width: 0.5px;
  border-color: var(--color-ink-500);
}
</style>
