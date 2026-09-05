<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { NoteLevel, NoteVisibility, StickyNote } from '@/stores/board'
import { useAccountStore } from '@/stores/account'

const account = useAccountStore()

const props = defineProps<{ note: StickyNote | null }>()
const emit = defineEmits<{
  close: []
  save: [StickyNote]
  delete: [StickyNote]
}>()

const editing = ref(false)
const title = ref('')
const tag = ref('')
const content = ref('')
const level = ref<NoteLevel>('normal')
const visibility = ref<NoteVisibility>('private')

watch(
  () => props.note,
  (note) => {
    editing.value = false
    title.value = note?.title ?? ''
    tag.value = note?.tag ?? ''
    content.value = note?.content ?? ''
    level.value = note?.level ?? 'normal'
    visibility.value = note?.visibility ?? 'private'
  },
  { immediate: true },
)

const colorClass = computed(
  () =>
    ({
      urgent: 'bg-red-100',
      normal: 'bg-accent',
      minor: 'bg-sky-100',
    })[props.note?.level ?? 'normal'],
)

const levelLabel = computed(
  () => ({ urgent: '緊急', normal: '普通', minor: '低' })[props.note?.level ?? 'normal'],
)

const statusLabel = computed(() => {
  if (!props.note) return ''
  if (props.note.employerStatus === 'read') return `${account.employer.name}已讀`
  if (props.note.employerStatus === 'unread') return `${account.employer.name}未讀`
  return `${account.employer.name}無權限`
})

function save() {
  if (!props.note || !content.value.trim()) return
  emit('save', {
    ...props.note,
    title: title.value.trim(),
    tag: tag.value.trim(),
    content: content.value.trim(),
    level: level.value,
    visibility: visibility.value,
    employerStatus:
      visibility.value === 'private'
        ? 'no-access'
        : props.note.employerStatus === 'no-access'
          ? 'unread'
          : props.note.employerStatus,
  })
  editing.value = false
}

function deleteCurrentNote() {
  if (!props.note || !window.confirm('確定要刪除這張便利貼嗎？')) return
  emit('delete', props.note)
}
</script>

<template>
  <Teleport to="body">
    <div
      v-if="note"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-8"
      @click.self="$emit('close')"
    >
      <div class="relative w-full max-w-xs">
        <div
          class="absolute inset-0 translate-x-2 translate-y-2 rotate-3 rounded-lg opacity-60"
          :class="colorClass"
        ></div>
        <div
          class="absolute inset-0 -translate-x-1 translate-y-1 -rotate-2 rounded-lg opacity-80"
          :class="colorClass"
        ></div>
        <div
          class="relative max-h-[82vh] space-y-3 overflow-y-auto rounded-lg p-5 text-sm text-ink-950 shadow-xl"
          :class="colorClass"
        >
          <template v-if="editing">
            <label class="block text-xs font-bold text-ink-700">
              {{ $t('標題') }}
              <input
                v-model="title"
                class="mt-1 w-full rounded-lg border border-ink-400 bg-white/80 px-3 py-2 text-sm font-normal text-ink-950 outline-none focus:border-pink-500"
              />
            </label>

            <label class="block text-xs font-bold text-ink-700">
              {{ $t('標籤') }}
              <input
                v-model="tag"
                class="mt-1 w-full rounded-lg border border-ink-400 bg-white/80 px-3 py-2 text-sm font-normal text-ink-950 outline-none focus:border-pink-500"
              />
            </label>

            <label class="block text-xs font-bold text-ink-700">
              {{ $t('內容') }}
              <textarea
                v-model="content"
                rows="5"
                class="mt-1 w-full resize-none rounded-lg border border-ink-400 bg-white/80 px-3 py-2 text-sm font-normal text-ink-950 outline-none focus:border-pink-500"
              ></textarea>
            </label>

            <div class="grid grid-cols-3 gap-1 text-xs">
              <button
                v-for="option in [
                  { value: 'urgent', label: '緊急' },
                  { value: 'normal', label: '普通' },
                  { value: 'minor', label: '低' },
                ]"
                :key="option.value"
                type="button"
                class="rounded-full border px-2 py-1"
                :class="
                  level === option.value ? 'border-pink-500 bg-white font-bold' : 'border-ink-400'
                "
                @click="level = option.value as NoteLevel"
              >
                {{ $t(option.label) }}
              </button>
            </div>

            <div class="grid grid-cols-2 gap-1 text-xs">
              <button
                type="button"
                class="rounded-full border px-2 py-1"
                :class="
                  visibility === 'private' ? 'border-pink-500 bg-white font-bold' : 'border-ink-400'
                "
                @click="visibility = 'private'"
              >
                {{ $t('私人') }}
              </button>
              <button
                type="button"
                class="rounded-full border px-2 py-1"
                :class="
                  visibility === 'employer'
                    ? 'border-pink-500 bg-white font-bold'
                    : 'border-ink-400'
                "
                @click="visibility = 'employer'"
              >
                {{ $t('給雇主') }}
              </button>
            </div>
          </template>

          <template v-else>
            <p>
              <span class="font-bold">{{ $t('標題：') }}</span
              >{{ note.demo ? $t(note.title) : note.title }}
            </p>
            <p>
              <span class="font-bold">{{ $t('內容：') }}</span
              >{{ note.demo ? $t(note.content) : note.content }}
            </p>
            <p class="text-xs text-ink-700">{{ statusLabel }}</p>
            <p class="text-xs text-ink-700">
              {{ $t('權限：') }}{{ note.visibility === 'employer' ? account.employer.name : $t('私人') }}
            </p>
            <p class="text-xs text-ink-700">{{ $t('等級：') }}{{ $t(levelLabel) }}</p>
          </template>

          <div class="grid grid-cols-2 gap-2 pt-2">
            <button
              type="button"
              class="rounded-full border border-red-200 bg-white/70 px-3 py-2 text-xs font-bold text-red-600"
              @click="deleteCurrentNote"
            >
              {{ $t('刪除') }}
            </button>
            <button
              v-if="editing"
              type="button"
              class="rounded-full bg-pink-500 px-3 py-2 text-xs font-bold text-white disabled:bg-ink-400"
              :disabled="!content.trim()"
              @click="save"
            >
              {{ $t('儲存') }}
            </button>
            <button
              v-else
              type="button"
              class="rounded-full bg-pink-500 px-3 py-2 text-xs font-bold text-white"
              @click="editing = true"
            >
              {{ $t('編輯') }}
            </button>
          </div>

          <button
            type="button"
            class="w-full rounded-full border border-ink-500 bg-white/70 px-3 py-2 text-xs font-bold text-ink-800"
            @click="editing ? (editing = false) : $emit('close')"
          >
            {{ editing ? $t('取消') : $t('關閉') }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
