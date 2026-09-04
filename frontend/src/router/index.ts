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
  ],
})

export default router
