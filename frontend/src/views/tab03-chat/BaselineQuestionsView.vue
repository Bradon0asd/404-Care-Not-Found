<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import StepProgressIndicator from '@/components/tab03-chat/StepProgressIndicator.vue'
import BaselineQuestionCard from '@/components/tab03-chat/BaselineQuestionCard.vue'
import { useCareAgentStore } from '@/stores/careAgent'

const router = useRouter()
const store = useCareAgentStore()

const frequencyOptions = ['完全沒有', '很少', '有時候', '常常', '幾乎每天']
const supportOptions = ['一定找得到', '大部分可以', '不一定', '很少', '完全沒有']

const questions = [
  { question: '過去 7 天，你大部分時間的心情如何？', options: frequencyOptions },
  { question: '過去 7 天，你覺得照護工作的壓力有多大？', options: frequencyOptions },
  { question: '過去 7 天，你有得到足夠的休息，讓自己恢復精神嗎？', options: frequencyOptions },
  { question: '當你遇到照護上的困難或心情不好時，你覺得有人可以幫助你嗎？', options: supportOptions },
  { question: '過去 7 天，你有沒有覺得「我快撐不住了」或很想暫時離開照護工作？', options: frequencyOptions },
]

const currentIndex = ref(0)
const answers = ref<(number | null)[]>([null, null, null, null, null])

const current = computed(() => questions[currentIndex.value]!)
const isLast = computed(() => currentIndex.value === questions.length - 1)

function selectAnswer(value: number | null) {
  if (value === null) return
  answers.value[currentIndex.value] = value
  if (!isLast.value) {
    currentIndex.value++
  }
}

function goBack() {
  if (currentIndex.value === 0) return
  currentIndex.value--
}

function submit() {
  store.completeBaseline(answers.value as number[])
  router.push('/chat')
}
</script>

<template>
  <PageContainer>
    <AppHeader />
    <StepProgressIndicator :current="1" />

    <div class="flex-1 space-y-4 px-4 pb-4">
      <BaselineQuestionCard
        :key="currentIndex"
        :index="currentIndex + 1"
        :question="current.question"
        :options="current.options"
        :model-value="answers[currentIndex]"
        @update:model-value="selectAnswer"
      />

      <BaseButton v-if="isLast" variant="primary" :disabled="answers[4] === null" @click="submit">
        生成你的客製化 Care Agent
      </BaseButton>

      <BaseButton v-if="currentIndex > 0" variant="outline" @click="goBack">返回上一題</BaseButton>
    </div>

    <BottomTabBar />
  </PageContainer>
</template>
