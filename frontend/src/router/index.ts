import { createRouter, createWebHistory } from 'vue-router'
import RoleSelectView from '@/views/auth/RoleSelectView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard',
    },
    {
      path: '/auth/role',
      name: 'auth-role-select',
      component: RoleSelectView,
    },
    {
      path: '/auth/caregiver/onboarding',
      name: 'auth-caregiver-onboarding',
      component: () => import('@/views/auth/CaregiverOnboardingView.vue'),
    },
    {
      path: '/auth/employer/setup',
      name: 'auth-employer-setup',
      component: () => import('@/views/auth/EmployerSetupView.vue'),
    },
    {
      path: '/dashboard',
      name: 'tab01-dashboard',
      component: () => import('@/views/tab01-dashboard/DashboardView.vue'),
    },
    {
      path: '/dashboard/add-schedule',
      name: 'tab01-add-schedule',
      component: () => import('@/views/tab01-dashboard/AddScheduleView.vue'),
    },
    {
      path: '/diary',
      name: 'tab02-diary',
      component: () => import('@/views/tab02-diary/DiaryMapView.vue'),
    },
    {
      path: '/diary/:day',
      name: 'tab02-diary-entry',
      component: () => import('@/views/tab02-diary/DiaryEntryView.vue'),
    },
    {
      path: '/chat',
      name: 'tab03-chat',
      component: () => import('@/views/tab03-chat/ChatHomeView.vue'),
    },
    {
      path: '/chat/intro',
      name: 'tab03-chat-intro',
      component: () => import('@/views/tab03-chat/IntroView.vue'),
    },
    {
      path: '/chat/setup',
      name: 'tab03-chat-setup',
      component: () => import('@/views/tab03-chat/AgentSetupView.vue'),
    },
    {
      path: '/chat/baseline',
      name: 'tab03-chat-baseline-intro',
      component: () => import('@/views/tab03-chat/BaselineIntroView.vue'),
    },
    {
      path: '/chat/baseline/questions',
      name: 'tab03-chat-baseline-questions',
      component: () => import('@/views/tab03-chat/BaselineQuestionsView.vue'),
    },
    {
      path: '/chat/room/:id',
      name: 'tab03-chat-room',
      component: () => import('@/views/tab03-chat/ChatRoomView.vue'),
    },
    {
      path: '/board',
      name: 'tab04-board',
      component: () => import('@/components/common/PlaceholderView.vue'),
      props: { title: '便利貼牆' },
    },
    {
      path: '/account',
      name: 'tab05-account',
      component: () => import('@/components/common/PlaceholderView.vue'),
      props: { title: '我的帳戶' },
    },
  ],
})

export default router
