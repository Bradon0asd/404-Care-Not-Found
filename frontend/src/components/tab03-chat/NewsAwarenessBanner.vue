<script setup lang="ts">
import { ref } from 'vue'
import { Carousel, Slide, Pagination } from 'vue3-carousel'
import 'vue3-carousel/dist/carousel.css'
import IconPlay from './icons/IconPlay.vue'

interface NewsVideo {
  youtubeId: string
  title: string
}

// News coverage on the migrant caregiver support gap, shown to reassure
// caregivers this isn't just their personal failing.
const videos: NewsVideo[] = [
  { youtubeId: 'f7EwMYjBuIk', title: '移工撐起長照' },
  { youtubeId: 'zpAAQOc8l38', title: '照護人力大流失' },
]
const collapsed = ref(false)
</script>

<template>
  <div class="relative bg-ink-200 px-3 py-3 text-center">
    <button
      type="button"
      class="absolute top-1 right-2 flex h-9 w-9 items-center justify-center rounded-full text-ink-700 hover:bg-ink-400 focus-visible:outline-2"
      :aria-expanded="!collapsed"
      aria-controls="care-news-videos"
      :aria-label="$t(collapsed ? '展開影音' : '收合影音')"
      @click="collapsed = !collapsed"
    >
      <svg
        aria-hidden="true"
        class="h-4 w-4 transition-transform"
        :class="collapsed ? 'rotate-180' : ''"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="1.8"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="m6 15 6-6 6 6" />
      </svg>
    </button>
    <p v-if="collapsed" class="min-h-5 px-9 text-xs font-bold text-ink-700">
      {{ $t('照護新聞與影音') }}
    </p>
    <template v-else>
      <p class="px-8 text-xs font-bold text-ink-950">
        {{ $t('看看這些新聞...不要把所有責任往自己身上扛') }}
      </p>
      <p class="text-xs font-bold text-ink-950">{{ $t('Your mental health, we care.') }}</p>
    </template>

    <div id="care-news-videos" v-if="!collapsed">
      <Carousel class="mt-3" :items-to-show="1.4" :wrap-around="true" :gap="8">
        <Slide v-for="video in videos" :key="video.youtubeId">
          <a
            :href="`https://youtu.be/${video.youtubeId}`"
            target="_blank"
            rel="noopener noreferrer"
            class="relative block h-36 w-full overflow-hidden rounded-lg bg-ink-300"
          >
            <img
              :src="`https://img.youtube.com/vi/${video.youtubeId}/hqdefault.jpg`"
              :alt="$t(video.title)"
              class="h-full w-full object-cover"
            />
            <span class="absolute inset-0 flex items-center justify-center bg-black/10">
              <span
                class="flex h-8 w-8 items-center justify-center rounded-full bg-pink-500/90 text-white shadow"
              >
                <IconPlay class="h-4 w-4" />
              </span>
            </span>
          </a>
        </Slide>

        <template #addons>
          <Pagination />
        </template>
      </Carousel>
    </div>
  </div>
</template>
