<template>
  <q-layout view="lHh Lpr lFf" class="bg-grey-1">
    <q-header elevated class="bg-dark text-white">
      <q-toolbar class="q-py-sm">
        <q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" />

        <q-toolbar-title class="text-weight-bold letter-spacing-1">
          SAMS<span class="text-info">.</span> OPERATIONS
        </q-toolbar-title>

        <div class="row items-center q-gutter-sm">
          <q-btn flat round dense icon="notifications" to="/operations/notifications">
            <q-badge floating color="info" rounded>2</q-badge>
          </q-btn>
          <q-avatar size="32px" class="cursor-pointer">
            <img src="https://cdn.quasar.dev/img/avatar.png">
          </q-avatar>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered class="bg-white" :width="280">
      <q-list class="q-mt-md">
        <q-item-label header class="text-overline text-grey-6 q-pb-md">HQ DASHBOARD</q-item-label>

        <q-item clickable v-ripple to="/operations/dashboard" class="menu-item q-mx-md q-mb-sm" active-class="active-ops-item">
          <q-item-section avatar><q-icon name="dashboard" /></q-item-section>
          <q-item-section class="text-weight-medium">Dashboard</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/operations/analytics" class="menu-item q-mx-md q-mb-sm" active-class="active-ops-item">
          <q-item-section avatar><q-icon name="insights" /></q-item-section>
          <q-item-section class="text-weight-medium">Analytics</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/operations/reports" class="menu-item q-mx-md q-mb-sm" active-class="active-ops-item">
          <q-item-section avatar><q-icon name="description" /></q-item-section>
          <q-item-section class="text-weight-medium">Reports</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/operations/players" class="menu-item q-mx-md q-mb-sm" active-class="active-ops-item">
          <q-item-section avatar><q-icon name="groups" /></q-item-section>
          <q-item-section class="text-weight-medium">Player Management</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/operations/finances" class="menu-item q-mx-md q-mb-sm" active-class="active-ops-item">
          <q-item-section avatar><q-icon name="account_balance_wallet" /></q-item-section>
          <q-item-section class="text-weight-medium">Financials</q-item-section>
        </q-item>
        
        <q-separator class="q-my-lg" />
        
        <q-item clickable v-ripple @click="logout" class="menu-item q-mx-md text-negative">
          <q-item-section avatar><q-icon name="logout" /></q-item-section>
          <q-item-section class="text-weight-medium">Logout</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const leftDrawerOpen = ref(false);
const authStore = useAuthStore();
const router = useRouter();

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}

function logout() {
  authStore.logout();
  router.push('/auth/login');
}
</script>

<style lang="scss" scoped>
.letter-spacing-1 { letter-spacing: 1px; }

.menu-item {
  border-radius: 12px;
  color: $dark;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba($info, 0.05);
  }
}

.active-ops-item {
  background: $dark !important;
  color: white !important;
  box-shadow: 0 4px 15px rgba($dark, 0.3);
}
</style>
