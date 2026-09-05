import { createRouter, createWebHistory } from 'vue-router'
import RoleSelectView from '@/views/auth/RoleSelectView.vue'
import { useAuthStore } from '@/stores/auth'

const onboardingPathByRole = {
  owner: '/auth/employer/setup',
  nurse: '/auth/caregiver/onboarding',
} as const

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
      path: '/auth/callback',
      name: 'auth-line-callback',
      component: () => import('@/views/auth/LineCallbackView.vue'),
    },
    {
      path: '/auth/caregiver/onboarding',
      name: 'auth-caregiver-onboarding',
      component: () => import('@/views/auth/CaregiverOnboardingView.vue'),
      meta: { requiresAuth: true, requiresOnboarding: true },
    },
    {
      path: '/auth/employer/setup',
      name: 'auth-employer-setup',
      component: () => import('@/views/auth/EmployerSetupView.vue'),
      meta: { requiresAuth: true, requiresOnboarding: true },
    },
    {
      path: '/dashboard',
      name: 'tab01-dashboard',
      component: () => import('@/views/tab01-dashboard/DashboardView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/dashboard/add-schedule',
      name: 'tab01-add-schedule',
      component: () => import('@/views/tab01-dashboard/AddScheduleView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/diary',
      name: 'tab02-diary',
      component: () => import('@/views/tab02-diary/DiaryMapView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/diary/:day',
      name: 'tab02-diary-entry',
      component: () => import('@/views/tab02-diary/DiaryEntryView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/chat',
      name: 'tab03-chat',
      component: () => import('@/views/tab03-chat/IntroView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/chat/setup',
      name: 'tab03-chat-setup',
      component: () => import('@/views/tab03-chat/AgentSetupView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/chat/baseline',
      name: 'tab03-chat-baseline-intro',
      component: () => import('@/views/tab03-chat/BaselineIntroView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/chat/baseline/questions',
      name: 'tab03-chat-baseline-questions',
      component: () => import('@/views/tab03-chat/BaselineQuestionsView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/chat/room/:id',
      name: 'tab03-chat-room',
      component: () => import('@/views/tab03-chat/ChatRoomView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/board',
      name: 'tab04-board',
      component: () => import('@/views/tab04-board/BoardListView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/board/new',
      name: 'tab04-board-new',
      component: () => import('@/views/tab04-board/AddNoteView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/account',
      name: 'tab05-account',
      component: () => import('@/views/tab05-account/AccountView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/account/plans',
      name: 'tab05-account-plans',
      component: () => import('@/views/tab05-account/PlansView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()

  if (!auth.sessionLoaded) {
    try {
      await auth.loadSession()
    } catch {
      if (to.meta.requiresAuth) {
        return { path: '/auth/role', query: { redirect: to.fullPath, error: 'NETWORK_ERROR' } }
      }
    }
  }

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return { path: '/auth/role', query: { redirect: to.fullPath } }
  }

  if (auth.isLoggedIn && auth.needsOnboarding) {
    const onboardingPath = onboardingPathByRole[auth.user!.role]
    if (!to.meta.requiresOnboarding && to.path !== onboardingPath) {
      return onboardingPath
    }
  }

  if (to.meta.requiresOnboarding && auth.isLoggedIn && !auth.needsOnboarding) {
    return '/dashboard'
  }

  if (to.path === '/auth/role' && auth.isLoggedIn) {
    return auth.needsOnboarding ? onboardingPathByRole[auth.user!.role] : '/dashboard'
  }
})

export default router
