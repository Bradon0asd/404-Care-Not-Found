<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import BottomTabBar from '@/components/layout/BottomTabBar.vue'

defineProps<{ title: string }>()
</script>

<template>
  <PageContainer>
    <AppHeader />
    <div class="flex flex-1 items-center justify-center px-6 text-center">
      <p class="text-sm text-ink-600">{{ title }} 開發中</p>
    </div>
    <BottomTabBar />
  </PageContainer>
</template>
