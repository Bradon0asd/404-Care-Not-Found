<script setup lang="ts">
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
</script>

<template>
  <div class="bg-ink-200 px-3 py-3 text-center">
    <p class="text-xs font-bold text-ink-950">看看這些新聞...不要把所有責任往自己身上打</p>
    <p class="text-xs font-bold text-ink-950">Your mental health, we care.</p>

    <Carousel class="mt-3" :items-to-show="1.4" :wrap-around="true" :gap="8">
      <Slide v-for="video in videos" :key="video.youtubeId">
        <a
          :href="`https://youtu.be/${video.youtubeId}`"
          target="_blank"
          rel="noopener noreferrer"
          class="relative block h-24 w-full overflow-hidden bg-ink-300"
        >
          <img
            :src="`https://img.youtube.com/vi/${video.youtubeId}/hqdefault.jpg`"
            :alt="video.title"
            class="h-full w-full object-cover"
          />
          <span class="absolute inset-0 flex items-center justify-center bg-black/10">
            <span class="flex h-8 w-8 items-center justify-center rounded-full bg-pink-500/90 text-white shadow">
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
</template>
