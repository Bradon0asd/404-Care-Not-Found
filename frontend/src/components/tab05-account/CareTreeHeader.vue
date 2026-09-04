<script setup lang="ts">
defineProps<{
  userName: string
  role: string
}>()

defineEmits<{ language: []; logout: []; plans: [] }>()

const TRUNK = '#a9847a'
const BRANCH = '#5c3a30'
</script>

<template>
  <div class="relative mx-auto" style="width: 300px; height: 480px">
    <svg width="300" height="480" viewBox="0 0 300 480" class="absolute inset-0">
      <!-- canopy: cluster of overlapping circles forms a fluffy, scalloped crown -->
      <g :fill="TRUNK">
        <circle cx="150" cy="30" r="34" />
        <circle cx="150" cy="52" r="46" />
        <circle cx="98" cy="80" r="36" />
        <circle cx="202" cy="80" r="36" />
        <circle cx="122" cy="98" r="32" />
        <circle cx="178" cy="98" r="32" />
        <circle cx="150" cy="92" r="42" />
      </g>

      <!-- trunk -->
      <path d="M128,138 L172,138 L192,410 Q150,428 108,410 Z" :fill="TRUNK" />

      <!-- heart where canopy meets trunk (same glyph as AppHeader's logo) -->
      <g transform="translate(134,136) scale(1.3)" fill="white">
        <path
          d="M12 21s-6.716-4.35-9.428-8.28C.86 10.02 1.2 6.6 3.6 4.8c2.1-1.58 4.86-1.1 6.4.9L12 7.8l2-2.1c1.54-2 4.3-2.48 6.4-.9 2.4 1.8 2.74 5.22 1.03 7.92C18.72 16.65 12 21 12 21z"
        />
      </g>

      <!-- left branch: 變更語言 -->
      <g :stroke="BRANCH" stroke-width="3" stroke-linecap="round" fill="none">
        <path d="M120,235 Q70,205 40,195" />
        <path d="M40,195 Q28,182 15,178" />
        <path d="M40,195 Q45,178 50,168" />
      </g>

      <!-- left branch: 登出 -->
      <g :stroke="BRANCH" stroke-width="3" stroke-linecap="round" fill="none">
        <path d="M112,330 Q70,305 35,300" />
        <path d="M35,300 Q20,290 8,285" />
        <path d="M35,300 Q38,282 42,272" />
      </g>

      <!-- right branch: 訂閱方案, ends in a small cluster of leaves -->
      <g>
        <path d="M185,280 Q225,255 250,245" :stroke="BRANCH" stroke-width="3" stroke-linecap="round" fill="none" />
        <g fill="#fcd856">
          <ellipse cx="250" cy="245" rx="15" ry="7.5" transform="rotate(-20 250 245)" />
          <ellipse cx="267" cy="232" rx="13" ry="6.5" transform="rotate(-45 267 232)" />
          <ellipse cx="264" cy="257" rx="13" ry="6.5" transform="rotate(15 264 257)" />
        </g>
      </g>
    </svg>

    <!-- avatar + name overlay on the canopy -->
    <div class="absolute top-[24px] left-1/2 flex -translate-x-1/2 flex-col items-center text-center">
      <!-- Placeholder avatar until the real photo asset/upload flow exists -->
      <img
        src="https://i.pravatar.cc/128?img=47"
        alt=""
        class="h-16 w-16 rounded-full border-4 border-white object-cover"
      />
      <p class="mt-1 text-[11px] text-white">使用者名稱：{{ userName }}</p>
      <p class="text-[11px] text-white">身分：{{ role }}</p>
    </div>

    <!-- branch labels, positioned at each branch tip -->
    <button type="button" class="absolute top-[184px] left-0 text-xs font-bold text-ink-800" @click="$emit('language')">
      變更語言
    </button>
    <button type="button" class="absolute top-[308px] left-0 text-xs font-bold text-ink-800" @click="$emit('logout')">
      登出
    </button>
    <button type="button" class="absolute top-[226px] left-[172px] text-xs font-bold text-ink-950" @click="$emit('plans')">
      訂閱方案
    </button>
  </div>
</template>
