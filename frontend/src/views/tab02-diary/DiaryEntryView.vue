<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
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
import { useDiaryStore, type DiaryVisibility } from '@/stores/diary'
import { toMinguoDate } from '@/utils/date'
import { useOnboardingStore } from '@/stores/onboarding'

const route = useRoute()
const router = useRouter()
const diaryStore = useDiaryStore()
const settings = useOnboardingStore()

const day = Number(route.params.day)
const entry = computed(() => diaryStore.entryForDay(day))
const fileInput = ref<HTMLInputElement | null>(null)
const selectedImageFile = ref<File | null>(null)
const selectedImagePreviewUrl = ref<string | null>(null)
const validationError = ref<string | null>(null)

const currentImageUrl = computed(() => selectedImagePreviewUrl.value ?? entry.value.imageUrl)

const dateLabel = computed(() => {
  const date = new Date(`${entry.value.date}T00:00:00`)
  return settings.language === 'id'
    ? new Intl.DateTimeFormat('id-ID', { dateStyle: 'full' }).format(date)
    : toMinguoDate(date)
})

function openDatePicker(event: MouseEvent) {
  const input = event.currentTarget as HTMLInputElement
  try {
    input.showPicker?.()
  } catch {
    input.focus()
  }
}

function updateDate(event: Event) {
  const input = event.currentTarget as HTMLInputElement
  if (input.value && input.validity.valid) entry.value.date = input.value
  else input.value = entry.value.date
}

function pickImage() {
  fileInput.value?.click()
}

function onImageSelected(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  if (selectedImagePreviewUrl.value) URL.revokeObjectURL(selectedImagePreviewUrl.value)
  selectedImageFile.value = file
  selectedImagePreviewUrl.value = URL.createObjectURL(file)
}

function removeImage() {
  if (selectedImagePreviewUrl.value) URL.revokeObjectURL(selectedImagePreviewUrl.value)
  selectedImageFile.value = null
  selectedImagePreviewUrl.value = null
  entry.value.imageUrl = null
  if (fileInput.value) fileInput.value.value = ''
}

function startVoiceInput() {
  console.info('Voice input is not connected yet.')
}

async function save(visibility: DiaryVisibility) {
  validationError.value = null
  if (!entry.value.content.trim()) {
    validationError.value = '請先輸入日記內容再儲存。'
    return
  }

  await diaryStore.saveEntry(entry.value, visibility, selectedImageFile.value)
  if (selectedImagePreviewUrl.value) URL.revokeObjectURL(selectedImagePreviewUrl.value)
  selectedImageFile.value = null
  selectedImagePreviewUrl.value = null
  router.push('/diary')
}

onMounted(() => {
  diaryStore.loadEntries().catch(() => undefined)
})

onBeforeUnmount(() => {
  if (selectedImagePreviewUrl.value) URL.revokeObjectURL(selectedImagePreviewUrl.value)
})
</script>

<template>
  <PageContainer>
    <template #header><AppHeader /></template>

    <div class="flex-1 space-y-4 px-4 py-4">
      <div class="flex justify-center">
        <div
          class="flex h-16 w-16 flex-col items-center justify-center rounded-full border-2 border-accent bg-accent text-sm font-bold text-ink-950"
        >
          <span class="text-[10px] font-normal">{{ $t('Day') }}</span>
          {{ $t(day) }}
        </div>
      </div>

      <label
        class="flex items-center gap-2 rounded-xl bg-ink-200 px-4 py-3 focus-within:ring-2 focus-within:ring-pink-500"
      >
        <span class="text-sm text-ink-700">{{ $t('標題') }}</span>
        <input
          v-model="entry.title"
          type="text"
          class="min-w-0 flex-1 bg-transparent text-sm text-ink-950 outline-none"
          :placeholder="$t('輸入日記標題')"
        />
        <IconPencil aria-hidden="true" class="h-4 w-4 shrink-0 text-ink-600" />
      </label>

      <label
        class="relative flex min-h-11 cursor-pointer items-center gap-2 rounded-xl bg-ink-200 px-4 py-3 focus-within:ring-2 focus-within:ring-pink-500"
      >
        <span class="shrink-0 text-sm text-ink-700">{{ $t('日期') }}</span>
        <IconCalendar aria-hidden="true" class="h-4 w-4 shrink-0 text-ink-600" />
        <span class="flex-1 text-sm text-ink-950">{{ $t(dateLabel) }}</span>
        <input
          type="date"
          :aria-label="$t('日期')"
          :value="entry.date"
          class="absolute inset-0 h-full w-full cursor-pointer opacity-0"
          @click="openDatePicker"
          @change="updateDate"
        />
      </label>

      <div class="rounded-xl bg-ink-200 p-4">
        <div class="mb-2 flex items-center justify-between">
          <span class="text-sm text-ink-700">{{ $t('照護紀錄') }}</span>
          <AiVoiceButton @click="startVoiceInput" />
        </div>
        <textarea
          v-model="entry.content"
          rows="5"
          :placeholder="$t('記下今天的飲食、用藥、情緒、睡眠或任何需要交接的事。')"
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
        <div v-if="currentImageUrl" class="relative w-fit">
          <img
            :src="currentImageUrl"
            :alt="$t('日記圖片')"
            class="h-24 w-24 rounded-lg object-cover"
          />
          <button
            type="button"
            class="absolute -top-2 -right-2 flex h-5 w-5 items-center justify-center rounded-full bg-ink-950 text-xs text-white"
            :aria-label="$t('移除圖片')"
            @click="removeImage"
          >
            x
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

      <div
        class="grid grid-cols-2 gap-3 pt-2 [&_button]:h-11 [&_button]:gap-1.5 [&_button]:px-2 [&_button]:py-0 [&_button]:text-xs [&_button]:whitespace-nowrap"
      >
        <BaseButton variant="primary" :disabled="diaryStore.saving" @click="save('private')">
          {{ diaryStore.saving ? $t('儲存中...') : $t('儲存日記') }}
        </BaseButton>
        <BaseButton variant="line" :disabled="diaryStore.saving" @click="save('shared')">
          <IconLine class="h-4 w-4 shrink-0" />
          <span class="text-[11px]">{{
            diaryStore.saving ? $t('儲存中...') : $t('分享給 LINE 家屬')
          }}</span>
        </BaseButton>
      </div>
      <p v-if="validationError || diaryStore.error" class="text-center text-xs text-red-600">
        {{ validationError ?? diaryStore.error }}
      </p>
      <BaseButton variant="outline" @click="router.back()">{{ $t('返回') }}</BaseButton>

      <p class="text-center text-xs text-ink-600">
        {{ $t('私密日記只會保留給自己；分享後，配對的家屬可以在後端讀取這則紀錄。') }}
      </p>
    </div>

    <template #footer><BottomTabBar /></template>
  </PageContainer>
</template>
