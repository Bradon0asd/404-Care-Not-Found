<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'
import NoteCard from '@/components/tab04-board/NoteCard.vue'
import NoteDetailModal from '@/components/tab04-board/NoteDetailModal.vue'
import AddNoteButton from '@/components/tab04-board/AddNoteButton.vue'
import { useBoardStore, type StickyNote } from '@/stores/board'

const router = useRouter()
const store = useBoardStore()

const statusFilter = ref('')
const levelFilter = ref('')
const activeNote = ref<StickyNote | null>(null)

const statusOptions = [
  { value: 'read', label: '已讀取' },
  { value: 'unread', label: '尚未讀取' },
  { value: 'no-access', label: '未獲得瀏覽權限' },
]
const levelOptions = [
  { value: 'urgent', label: '緊急' },
  { value: 'normal', label: '普通' },
  { value: 'minor', label: '不重要' },
]

const filteredNotes = computed(() =>
  store.notes.filter(
    (n) =>
      (!statusFilter.value || n.employerStatus === statusFilter.value) &&
      (!levelFilter.value || n.level === levelFilter.value),
  ),
)
</script>

<template>
  <PageContainer>
    <template #header>
      <AppHeader />
      <div class="flex items-center justify-between bg-ink-200 px-4 py-3">
        <FilterSelect v-model="statusFilter" label="狀態" :options="statusOptions" />
        <FilterSelect v-model="levelFilter" label="層級" :options="levelOptions" />
      </div>
    </template>

    <div class="grid flex-1 grid-cols-2 gap-3 px-4 pt-4 pb-24">
      <NoteCard
        v-for="note in filteredNotes"
        :key="note.id"
        :note="note"
        @click="activeNote = note"
      />
    </div>

    <NoteDetailModal :note="activeNote" @close="activeNote = null" />
    <template #fab><AddNoteButton @click="router.push('/board/new')" /></template>
    <template #footer><BottomTabBar /></template>
  </PageContainer>
</template>
