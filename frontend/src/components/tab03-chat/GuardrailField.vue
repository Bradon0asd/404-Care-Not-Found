<script setup lang="ts">
import { ref } from 'vue'
import { translate } from '@/i18n'

const value = defineModel<string>({ required: true })
const showExplanation = ref(false)

const TEMPLATE =
  '不提供醫療診斷或用藥建議，遇到醫療判斷情境一律回覆「建議聯繫家屬／就醫」；不評論家庭或雇傭關係的對錯；不主動提及壓力值或風險評估。'

function applyTemplate() {
  value.value = translate(TEMPLATE)
}
</script>

<template>
  <div class="rounded-xl bg-ink-200 p-4">
    <h3 class="mb-1 text-sm font-bold text-ink-950">Guardrail</h3>
    <p class="mb-3 text-xs text-ink-600">
      {{ $t('此處可以明確定義 Care Agent 不能做什麼') }}<br />{{ $t('如果不確定可以套用範本內容') }}
    </p>

    <textarea
      v-model="value"
      rows="3"
      class="mb-3 w-full rounded-lg bg-white px-3 py-2 text-sm text-ink-950"
    ></textarea>

    <div class="flex gap-2">
      <button
        type="button"
        class="flex-1 rounded-full border border-ink-500 bg-white py-2 text-xs font-bold text-ink-700"
        @click="showExplanation = !showExplanation"
      >
        {{ $t('功能詳細說明') }}
      </button>
      <button
        type="button"
        class="flex-1 rounded-full bg-accent py-2 text-xs font-bold text-ink-950"
        @click="applyTemplate"
      >
        {{ $t('範本內容') }}
      </button>
    </div>

    <p v-if="showExplanation" class="mt-3 text-xs text-ink-600">
      {{
        $t(
          'Guardrail 是給 Care Agent 的安全邊界，例如不能做醫療診斷、不能評論家庭關係等。設定後 AI 回覆會避開這些內容。',
        )
      }}
    </p>
  </div>
</template>
