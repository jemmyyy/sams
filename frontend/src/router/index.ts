import { route } from 'quasar/wrappers';
import {
  createMemoryHistory,
  createRouter,
  createWebHashHistory,
  createWebHistory,
} from 'vue-router';

import routes from './routes';
import { useAuthStore } from '../stores/auth';

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory);

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(process.env.VUE_ROUTER_BASE),
  });

  // Strict SAMS Security Protocol
  Router.beforeEach(async (to, from) => {
    const authStore = useAuthStore();
    
    // 1. Session Bootstrap: Fetch user profile if token exists but state is empty
    if (authStore.isAuthenticated && !authStore.isInitialized) {
      await authStore.init();
    }

    const isLoggedIn = !!authStore.user;
    const isAuthRoute = to.name === 'login' || to.name === 'register'; // Home is NOT a guest-only route, it's public
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const requiredRole = to.matched.find(record => record.meta.role)?.meta.role as string | undefined;

    // 2. Prevent logged-in users from hitting Auth routes (Login/Register)
    if (isLoggedIn && isAuthRoute) {
      const portal = authStore.primaryPortal;
      if (to.name !== portal) {
        return { name: portal };
      }
    }

    // 3. Handle Guest access to protected routes
    if (requiresAuth && !isLoggedIn) {
      // Preserve the intended destination and requested role
      return {
        name: 'login',
        query: {
          redirect: to.fullPath,
          role: requiredRole || 'customer'
        }
      };
    }

    // 4. Role Enforcement
    if (isLoggedIn && requiredRole) {
      const accessGranted = authStore.hasRole(requiredRole);

      if (!accessGranted) {
        console.error(`SECURITY_VIOLATION: ${authStore.user?.username} attempted access to ${to.path} without role ${requiredRole}`);
        const portal = authStore.primaryPortal;
        if (to.name !== portal) {
          return { name: portal };
        }
      }
    }

    // Allow navigation — no return value needed
  });

  return Router;
});
