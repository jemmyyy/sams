import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
    ],
  },
  {
    path: '/auth',
    component: () => import('layouts/AuthLayout.vue'),
    children: [
      { path: '/login', component: () => import('pages/LoginPage.vue'), name: 'login' },
      { path: '/register', component: () => import('pages/RegisterPage.vue'), name: 'register' },
    ],
  },
  {
    path: '/customer',
    component: () => import('layouts/CustomerLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: 'timetable', component: () => import('pages/customer/TimetablePage.vue') },
      { path: 'profile', component: () => import('pages/customer/ProfilePage.vue') },
    ],
  },
  {
    path: '/coach',
    component: () => import('layouts/CoachLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: 'timetable', component: () => import('pages/coach/TimetablePage.vue') },
      { path: 'attendance', component: () => import('pages/coach/AttendancePage.vue') },
      { path: 'reports', component: () => import('pages/coach/SessionReportPage.vue') },
      { path: 'ratings', component: () => import('pages/coach/RatingPage.vue') },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
