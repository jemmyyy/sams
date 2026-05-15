import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('../pages/IndexPage.vue'), name: 'home' },
    ],
  },
  {
    path: '/auth',
    component: () => import('../layouts/AuthLayout.vue'),
    children: [
      { path: 'login', component: () => import('../pages/LoginPage.vue'), name: 'login' },
      { path: 'login/customer', component: () => import('../pages/LoginPage.vue'), name: 'login-customer', meta: { targetRole: 'customer' } },
      { path: 'login/coach', component: () => import('../pages/LoginPage.vue'), name: 'login-coach', meta: { targetRole: 'coach' } },
      { path: 'login/ops', component: () => import('../pages/LoginPage.vue'), name: 'login-ops', meta: { targetRole: 'operations' } },
      { path: 'register', component: () => import('../pages/RegisterPage.vue'), name: 'register' },
    ],
  },
  {
    path: '/customer',
    component: () => import('../layouts/CustomerLayout.vue'),
    meta: { requiresAuth: true, role: 'customer' },
    children: [
      { path: 'timetable', component: () => import('../pages/customer/TimetablePage.vue'), name: 'customer-timetable' },
      { path: 'profile', component: () => import('../pages/customer/ProfilePage.vue'), name: 'customer-profile' },
      { path: 'cancellations', component: () => import('../pages/customer/CancellationsPage.vue'), name: 'customer-cancellations' },
    ],
  },
  {
    path: '/coach',
    component: () => import('../layouts/CoachLayout.vue'),
    meta: { requiresAuth: true, role: 'coach' },
    children: [
      { path: 'timetable', component: () => import('../pages/coach/TimetablePage.vue'), name: 'coach-timetable' },
      { path: 'attendance', component: () => import('../pages/coach/AttendancePage.vue'), name: 'coach-attendance' },
      { path: 'reports', component: () => import('../pages/coach/SessionReportPage.vue'), name: 'coach-reports' },
      { path: 'ratings', component: () => import('../pages/coach/RatingPage.vue'), name: 'coach-ratings' },
    ],
  },
  {
    path: '/operations',
    component: () => import('../layouts/OperationsLayout.vue'),
    meta: { requiresAuth: true, role: 'operations' },
    children: [
      { path: 'dashboard', component: () => import('../pages/operations/DashboardPage.vue'), name: 'ops-dashboard' },
      { path: 'analytics', component: () => import('../pages/operations/AnalyticsPage.vue'), name: 'ops-analytics' },
      { path: 'reports', component: () => import('../pages/operations/ReportsPage.vue'), name: 'ops-reports' },
      { path: 'players', component: () => import('../pages/operations/PlayerManagementPage.vue'), name: 'ops-players' },
      { path: 'finances', component: () => import('../pages/operations/FinancesPage.vue'), name: 'ops-finances' },
      { path: 'notifications', component: () => import('../pages/common/NotificationsPage.vue'), name: 'ops-notifications' },
    ],
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('../pages/ErrorNotFound.vue'),
  },
];

export default routes;
