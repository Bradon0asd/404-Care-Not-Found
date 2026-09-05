<script setup lang="ts">
defineProps<{
  userName: string
  pictureUrl?: string | null
  role: string
}>()

defineEmits<{ language: []; logout: []; plans: [] }>()

const leaves = [
  { x: 282, y: 399, rotate: -28 },
  { x: 313, y: 386, rotate: 18 },
  { x: 333, y: 414, rotate: 78 },
  { x: 122, y: 489, rotate: -105 },
  { x: 95, y: 470, rotate: -48 },
  { x: 143, y: 473, rotate: -14 },
  { x: 97, y: 599, rotate: -98 },
  { x: 71, y: 581, rotate: -40 },
  { x: 118, y: 583, rotate: -12 },
]
</script>

<template>
  <section
    class="care-tree relative mx-auto aspect-[402/740] shrink-0"
    :aria-label="$t('帳戶設定樹')"
  >
    <svg
      class="absolute inset-0 h-full w-full"
      viewBox="0 0 402 740"
      fill="none"
      aria-hidden="true"
    >
      <!-- Soft foliage sits behind the profile; the trunk remains a separate silhouette. -->
      <ellipse cx="201" cy="706" rx="131" ry="13" fill="#f6eeeb" />
      <!-- A broader trunk extends behind the foreground canopy. -->
      <path
        transform="translate(201 0) scale(1.3 1) translate(-201 0)"
        d="M181 230C185 316 181 367 181 410C173 396 156 379 139 369C156 390 176 420 180 445C180 478 178 501 174 522C153 509 135 495 119 487C138 507 157 526 171 542C165 582 159 608 148 635C130 625 109 614 87 607C110 622 125 638 139 651C123 679 102 696 73 706C109 706 137 689 159 677C155 691 145 704 132 712C163 709 178 692 187 680C185 695 184 706 176 718C196 712 205 697 209 681C222 698 246 710 274 710C249 697 239 685 229 671C257 688 281 699 313 699C273 683 244 658 227 625C214 598 208 563 207 528C205 492 208 459 214 432C238 424 262 414 284 399C259 408 237 413 219 414C227 362 229 313 224 230Z"
        fill="#b79c91"
      />
      <path
        d="M203 280C210 359 194 419 195 486C198 573 184 638 165 673"
        stroke="#d2bab0"
        stroke-width="5"
        stroke-linecap="round"
      />
      <path
        d="M207 656C216 677 232 690 248 696M186 648C176 668 161 681 147 689"
        stroke="#a88b80"
        stroke-width="2"
        stroke-linecap="round"
      />

      <g stroke="#a88b80" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <path
          d="M255 411C281 399 302 399 329 407M283 402C293 389 301 382 313 377M308 402C320 416 332 422 345 423"
        />
        <path
          d="M156 517C138 503 116 491 91 483M125 501C133 488 139 476 139 463M106 488C100 477 93 470 83 466"
        />
        <path
          d="M134 635C117 620 95 608 68 601M104 620C114 607 117 591 114 577M82 607C77 596 70 585 59 580"
        />
      </g>
      <g
        v-for="(leaf, i) in leaves"
        :key="i"
        :transform="`translate(${leaf.x} ${leaf.y}) rotate(${leaf.rotate})`"
      >
        <path
          d="M0 8C-14 0-13-17 0-24C13-16 14 0 0 8Z"
          :fill="i % 3 === 0 ? '#c1cbb8' : '#d4ddca'"
        />
        <path d="M0 5V-15" stroke="#a4b099" stroke-width="1" stroke-linecap="round" />
      </g>

      <path
        d="M88 206C54 193 49 155 71 130C58 99 86 67 119 69C130 35 166 25 197 43C223 17 268 34 277 64C317 56 348 88 337 121C366 145 357 186 329 199C337 232 303 258 274 253C251 280 216 270 201 260C174 279 139 266 130 250C98 257 77 234 88 206Z"
        fill="#f6dce2"
      />
      <path
        d="M79 132C70 105 96 80 121 85C138 52 171 52 192 65"
        stroke="#fff5f7"
        stroke-width="12"
        stroke-linecap="round"
      />
      <path
        d="M272 245C303 250 325 229 320 207C345 195 349 172 338 155"
        stroke="#edc8d2"
        stroke-width="10"
        stroke-linecap="round"
      />

      <path
        d="M201 349C183 337 181 328 187 323C193 318 200 322 201 327C203 321 210 318 216 323C223 330 216 340 201 349Z"
        fill="#fff5f7"
      />
      <g fill="#edc8d2">
        <ellipse cx="93" cy="682" rx="5" ry="9" transform="rotate(-48 93 682)" />
        <ellipse cx="304" cy="672" rx="4" ry="8" transform="rotate(40 304 672)" />
      </g>
    </svg>

    <div
      class="absolute top-[9.5%] left-1/2 flex w-[72%] -translate-x-1/2 flex-col items-center text-center"
    >
      <img
        :src="pictureUrl || 'https://i.pravatar.cc/256?img=47'"
        :alt="$t('使用者頭像')"
        class="aspect-square w-[40%] rounded-full border-2 border-white object-cover shadow-sm"
      />
      <p class="mt-1.5 text-xs font-medium text-[#594b48]">
        {{ $t('使用者名稱：') }}{{ userName }}
      </p>
      <p class="mt-1 text-[11px] text-[#75635e]">{{ $t('身分：') }}{{ $t(role) }}</p>
    </div>

    <button type="button" class="tree-action absolute top-[48%] right-[7%]" @click="$emit('plans')">
      {{ $t('訂閱方案') }}
    </button>
    <button
      type="button"
      class="tree-action absolute top-[62%] left-[8%]"
      @click="$emit('language')"
    >
      {{ $t('變更語言') }}
    </button>
    <button type="button" class="tree-action absolute top-[78%] left-[5%]" @click="$emit('logout')">
      {{ $t('登出') }}
    </button>
  </section>
</template>

<style scoped>
.care-tree {
  width: min(100cqw, calc(100cqh * 402 / 740), 402px);
}

.tree-action {
  min-height: 44px;
  min-width: 76px;
  padding: 8px 12px;
  border: 1px solid #e8d8d2;
  border-radius: 999px;
  background: #fffaf7;
  color: #594b48;
  font-size: clamp(12px, 2cqh, 14px);
  font-weight: 600;
  box-shadow: 0 3px 8px #795c4810;
  transition:
    background-color 150ms,
    border-color 150ms;
}

.tree-action:hover {
  background: #fcecf0;
  border-color: #d7b9b4;
}

.tree-action:focus-visible {
  outline: 2px solid #8d7066;
  outline-offset: 4px;
}
</style>
