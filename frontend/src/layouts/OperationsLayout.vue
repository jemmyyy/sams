<template>
  <q-layout view="lHh Lpr lFf" class="apex-layout">
    <!-- Clean Header -->
    <q-header class="bg-white text-navy border-bottom">
      <q-toolbar class="q-py-md max-w-xl">
        <q-btn flat dense round icon="menu" @click="toggleLeftDrawer" class="q-mr-sm" />

        <q-toolbar-title class="text-apex text-h5">
          SAMS<span class="text-victory">.</span><span class="text-weight-light text-grey-6 q-ml-sm">OPS</span>
        </q-toolbar-title>

        <q-space />

        <div class="row items-center q-gutter-md">
          <q-btn flat round icon="notifications_none" color="grey-7">
            <q-badge floating color="victory" rounded>4</q-badge>
          </q-btn>
          
          <q-separator vertical inset class="q-mx-sm" />

          <div class="user-profile row items-center q-gutter-sm pointer" @click="toggleLeftDrawer">
            <div class="column items-end gt-xs">
              <span class="text-weight-bold text-caption text-navy">{{ authStore.user?.username }}</span>
              <span class="text-grey-6 text-min uppercase">Operations HQ</span>
            </div>
            <q-avatar size="40px" class="apex-avatar shadow-sm">
              <img src="https://cdn.quasar.dev/img/avatar.png">
            </q-avatar>
          </div>
        </div>
      </q-toolbar>
    </q-header>

    <!-- Professional Sidebar -->
    <q-drawer v-model="leftDrawerOpen" show-if-above bordered class="apex-sidebar" :width="280">
      <div class="column full-height">
        <div class="q-mt-xl q-px-xl q-mb-lg">
           <div class="text-overline text-grey-5 letter-spacing-1">Academy Management</div>
        </div>

        <q-list class="q-px-md q-gutter-y-xs">
          <q-item clickable v-ripple to="/operations/dashboard" class="apex-menu-item" active-class="active-item">
            <q-item-section avatar><q-icon name="dashboard" size="22px" /></q-item-section>
            <q-item-section class="text-weight-medium">Dashboard</q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/operations/analytics" class="apex-menu-item" active-class="active-item">
            <q-item-section avatar><q-icon name="analytics" size="22px" /></q-item-section>
            <q-item-section class="text-weight-medium">Insights</q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/operations/reports" class="apex-menu-item" active-class="active-item">
            <q-item-section avatar><q-icon name="assessment" size="22px" /></q-item-section>
            <q-item-section class="text-weight-medium">Reports</q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/operations/players" class="apex-menu-item" active-class="active-item">
            <q-item-section avatar><q-icon name="people_alt" size="22px" /></q-item-section>
            <q-item-section class="text-weight-medium">Athletes</q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/operations/finances" class="apex-menu-item" active-class="active-item">
            <q-item-section avatar><q-icon name="account_balance_wallet" size="22px" /></q-item-section>
            <q-item-section class="text-weight-medium">Financials</q-item-section>
          </q-item>
        </q-list>

        <q-space />

        <div class="q-pa-md">
          <q-item clickable v-ripple @click="logout" class="apex-menu-item logout-btn">
            <q-item-section avatar><q-icon name="logout" color="negative" size="22px" /></q-item-section>
            <q-item-section class="text-weight-bold text-negative">Sign Out</q-item-section>
          </q-item>
        </div>
      </div>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';

const leftDrawerOpen = ref(false);
const authStore = useAuthStore();

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}

function logout() {
  authStore.logout();
}
</script>

<style lang="scss" scoped>
.text-navy { color: var(--sams-navy); }
.text-victory { color: var(--sams-victory-red); }
.border-bottom { border-bottom: 1px solid var(--sams-border); }
.text-min { font-size: 11px; }

.apex-layout {
  background-color: var(--sams-slate-bg);
}

.apex-avatar {
  border: 2px solid white;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.apex-sidebar {
  background-color: white;
  border-right: 1px solid var(--sams-border);
}

.apex-menu-item {
  border-radius: 12px;
  color: #64748b;
  padding: 12px 20px;
  transition: all 0.3s ease;
  
  &:hover {
    color: var(--sams-navy);
    background: #f1f5f9;
  }
}

.active-item {
  color: var(--sams-victory-red) !important;
  background: #fff1f2 !important;
  font-weight: 700 !important;
  &::after {
    content: '';
    position: absolute;
    right: 8px; top: 50%; transform: translateY(-50%);
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--sams-victory-red);
  }
}

.logout-btn {
  border: 1px solid #fee2e2;
  &:hover { background: #fef2f2; border-color: #fecaca; }
}
</style>
