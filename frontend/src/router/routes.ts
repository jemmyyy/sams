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
    path: '/customer',
    component: () => import('layouts/CustomerLayout.vue'),
    children: [
      { path: 'timetable', component: () => import('pages/customer/TimetablePage.vue') },
      { path: 'profile', component: () => import('pages/customer/ProfilePage.vue') },
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
