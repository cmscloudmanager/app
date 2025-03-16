import { createRouter, createWebHistory } from 'vue-router'
import {useAuthStore} from "@/stores/userStore.js";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/projects',
      name: 'projects',
      component: () => import('@/views/ProjectsView.vue'),
    },
    {
      path: '/projects/add',
      name: 'new-project',
      component: () => import('@/views/ProjectAddView.vue'),
    },
    {
      path: '/projects/:id',
      name: 'project',
      component: () => import('@/views/ProjectView.vue'),
    },
    {
      path: '/providers',
      name: 'providers',
      component: () => import('@/views/ProvidersView.vue'),
    },
    {
      path: '/providers/add',
      name: 'new-provider',
      component: () => import('@/views/ProviderAddView.vue'),
    },
    {
      path: '/providers/:id',
      name: 'provider',
      component: () => import('@/views/ProviderView.vue'),
    },
    {
      path: '/users',
      name: 'users',
      component: () => import('@/views/UsersView.vue'),
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/SettingsView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'Not Found',
      component: () => import("@/views/404View.vue"),
      meta: {requiresAuth: true, showSpinner: false}
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated
  const requiresAuth = to.meta.requiresAuth !== false

  if (requiresAuth && !isAuthenticated) {
    next({ name: 'login' })
  }
  else if (to.path === '/' && isAuthenticated) {
    next({ name: 'projects' })
  }
  else {
    next()
  }
})

export default router
