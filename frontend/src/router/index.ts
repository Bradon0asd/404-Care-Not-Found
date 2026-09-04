import { createRouter, createWebHistory } from 'vue-router'
import RoleSelectView from '@/views/auth/RoleSelectView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/auth/role',
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
      component: () => import('@/components/common/PlaceholderView.vue'),
      props: { title: '秘密日記' },
    },
    {
      path: '/chat',
      name: 'tab03-chat',
      component: () => import('@/components/common/PlaceholderView.vue'),
      props: { title: '跟我聊聊' },
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
