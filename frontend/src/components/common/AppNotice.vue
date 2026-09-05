<script setup lang="ts">
import { onBeforeUnmount } from 'vue'
import { useNoticeStore } from '@/stores/notice'
const notice = useNoticeStore()
onBeforeUnmount(notice.dismiss)
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
          v-if="notice.message"
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
          <span>{{ $t(notice.message) }}</span>
        </div>
      </Transition>
    </div>
  </Teleport>
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
