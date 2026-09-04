<script setup lang="ts">
import { ref } from 'vue'
import BaseButton from '@/components/common/BaseButton.vue'
import type { NoteVisibility } from '@/stores/board'

defineProps<{ open: boolean }>()
const emit = defineEmits<{ close: []; publish: [NoteVisibility] }>()

const visibility = ref<NoteVisibility>('private')

function publish() {
  emit('publish', visibility.value)
}
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-6" @click.self="$emit('close')">
      <div class="w-full max-w-xs space-y-4 rounded-2xl bg-white p-5">
        <h2 class="text-sm font-bold text-ink-950">誰可以看到這張便利貼？</h2>

        <label class="flex items-center gap-2 rounded-xl border border-ink-400 px-4 py-3 text-sm text-ink-950">
          <input v-model="visibility" type="radio" value="private" class="accent-pink-500" />
          只有自己
        </label>
        <label class="flex items-center gap-2 rounded-xl border border-ink-400 px-4 py-3 text-sm text-ink-950">
          <input v-model="visibility" type="radio" value="employer" class="accent-pink-500" />
          雇主
        </label>

        <BaseButton variant="primary" @click="publish">發布便利貼</BaseButton>
      </div>
    </div>
  </Teleport>
</template>
