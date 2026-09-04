<script setup lang="ts">
defineProps<{
  userName: string
  role: string
}>()

defineEmits<{ language: []; logout: []; plans: [] }>()

const TRUNK = '#b78f83'
const BRANCH = '#6b302d'
const LEAF = '#fcd856'
</script>

<template>
  <section class="relative mx-auto h-full min-h-[640px] w-full max-w-[402px] overflow-hidden" aria-label="帳戶設定樹">
    <svg class="absolute inset-0 h-full w-full" viewBox="0 0 402 740" preserveAspectRatio="none" aria-hidden="true">
      <!-- The wide, low canopy and curved trunk follow the original Tab 05 composition. -->
      <g :fill="TRUNK">
        <circle cx="210" cy="104" r="66" />
        <circle cx="147" cy="142" r="64" />
        <circle cx="273" cy="142" r="64" />
        <circle cx="119" cy="194" r="50" />
        <circle cx="301" cy="194" r="50" />
        <circle cx="210" cy="177" r="84" />
      </g>

      <path
        d="M144 210 C154 296 168 390 166 480 C164 571 135 658 68 740 L352 740 C285 658 256 571 254 480 C252 390 266 296 276 210 Z"
        :fill="TRUNK"
      />

      <path
        d="M210 353 C192 340 188 329 194 321 C200 313 210 317 210 325 C210 317 220 313 226 321 C232 329 228 340 210 353 Z"
        fill="white"
      />

      <g :stroke="BRANCH" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" fill="none">
        <path d="M252 446 C279 429 301 416 327 407" />
      </g>
      <g :fill="LEAF">
        <path d="M269 439 C276 419 289 408 307 403 C306 421 295 433 269 439 Z" />
        <path d="M290 419 C290 397 298 385 314 379 C316 397 309 410 290 419 Z" />
        <path d="M310 407 C318 388 330 381 347 384 C342 400 330 408 310 407 Z" />
        <path d="M300 437 C315 423 329 420 345 426 C335 440 322 444 300 437 Z" />
        <path d="M322 451 C338 438 352 438 367 446 C355 459 341 461 322 451 Z" />
        <path d="M286 458 C301 445 315 443 331 450 C320 464 306 467 286 458 Z" />
        <path d="M278 475 C293 460 307 458 323 465 C313 480 298 483 278 475 Z" />
      </g>

      <g :stroke="BRANCH" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" fill="none">
        <path d="M167 526 C143 501 116 482 94 467" />
        <path d="M146 510 L146 478" />
        <path d="M124 494 L124 463" />
        <path d="M101 473 L101 445" />
      </g>

      <g :stroke="BRANCH" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" fill="none">
        <path d="M137 653 C111 624 89 606 61 589" />
        <path d="M115 631 L115 601" />
        <path d="M91 611 L91 582" />
        <path d="M67 593 L67 565" />
      </g>
    </svg>

    <div class="absolute top-[9.5%] left-1/2 flex -translate-x-1/2 flex-col items-center text-center">
      <img
        src="https://i.pravatar.cc/256?img=47"
        alt="使用者頭像"
        class="h-32 w-32 rounded-full border-4 border-white object-cover"
      />
      <p class="mt-2 whitespace-nowrap text-sm font-medium text-white">使用者名稱：{{ userName }}</p>
      <p class="whitespace-nowrap text-sm font-medium text-white">身分：{{ role }}</p>
    </div>

    <button
      type="button"
      class="absolute top-[51%] right-[5%] min-h-11 min-w-20 text-sm font-bold text-ink-950"
      @click="$emit('plans')"
    >
      訂閱方案
    </button>
    <button
      type="button"
      class="absolute top-[65%] left-[12%] min-h-11 min-w-20 text-sm font-bold text-ink-950"
      @click="$emit('language')"
    >
      變更語言
    </button>
    <button
      type="button"
      class="absolute top-[82%] left-[9%] min-h-11 min-w-16 text-sm font-bold text-ink-950"
      @click="$emit('logout')"
    >
      登出
    </button>
  </section>
</template>
