<template>
  <q-layout view="lHh Lpr lFf" class="sams-customer-layout">
    <!-- Solid Header -->
    <q-header class="bg-white text-navy shadow-sm">
      <q-toolbar class="q-py-md">
        <q-btn flat dense round icon="menu" @click="toggleLeftDrawer" class="q-mr-sm" />

        <q-toolbar-title class="text-heading text-h5">
          SAMS<span class="text-primary">.</span><span class="text-weight-light text-grey-6 q-ml-sm">Arena</span>
        </q-toolbar-title>

        <q-space />

        <div class="row items-center q-gutter-md">
          <q-btn flat round icon="notifications_none" color="grey-7">
            <q-badge floating color="primary" rounded />
          </q-btn>
          
          <q-separator vertical inset class="q-mx-sm" />

          <div class="user-pill row items-center q-pl-md q-pr-sm q-py-xs pointer" @click="toggleLeftDrawer">
            <div class="column items-end q-mr-md gt-xs">
              <span class="text-weight-bold text-caption">{{ authStore.user?.first_name || authStore.user?.username }}</span>
              <span class="text-grey-6 text-min uppercase letter-spacing-1">Athlete/Parent</span>
            </div>
            <q-avatar size="36px" class="shadow-sm">
              <img src="https://cdn.quasar.dev/img/avatar.png">
            </q-avatar>
          </div>
        </div>
      </q-toolbar>
    </q-header>

    <!-- Solid Sidebar -->
    <q-drawer v-model="leftDrawerOpen" show-if-above bordered class="bg-white" :width="280">
      <div class="column full-height">
        <div class="q-mt-xl q-px-xl q-mb-lg">
           <div class="text-overline text-grey-4 letter-spacing-2">My Portal</div>
        </div>

        <q-list class="q-px-md q-gutter-y-xs">
          <q-item clickable v-ripple to="/customer/timetable" class="menu-link" active-class="active-link-blue">
            <q-item-section avatar><q-icon name="calendar_month" size="20px" /></q-item-section>
            <q-item-section class="text-weight-medium">Timetable</q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/customer/profile" class="menu-link" active-class="active-link-blue">
            <q-item-section avatar><q-icon name="person_outline" size="20px" /></q-item-section>
            <q-item-section class="text-weight-medium">Profile</q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/customer/cancellations" class="menu-link" active-class="active-link-blue">
            <q-item-section avatar><q-icon name="event_busy" size="20px" /></q-item-section>
            <q-item-section class="text-weight-medium">Cancellations</q-item-section>
          </q-item>
        </q-list>

        <q-space />

        <div class="q-pa-md">
          <q-item clickable v-ripple @click="logout" class="menu-link logout-item">
            <q-item-section avatar><q-icon name="logout" color="negative" size="20px" /></q-item-section>
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

function toggleLeftDrawer () {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}

function logout() {
  authStore.logout();
}
</script>

<style lang="scss" scoped>
.sams-customer-layout { background-color: #f8fafc; }
.text-min { font-size: 11px; }
.letter-spacing-1 { letter-spacing: 1px; }
.letter-spacing-2 { letter-spacing: 2px; }

.user-pill {
  background: #f1f5f9;
  border-radius: 50px;
  border: 1px solid #e2e8f0;
  &:hover { background: #e2e8f0; }
}

.menu-link {
  border-radius: 12px;
  color: #64748b;
  padding: 12px 20px;
  transition: all 0.3s ease;
  &:hover { color: var(--sams-navy); background: #f1f5f9; }
}

.active-link-blue {
  color: var(--sams-primary) !important;
  background: #eff6ff !important;
  font-weight: 700 !important;
  &::after {
    content: '';
    position: absolute;
    right: 8px; top: 50%; transform: translateY(-50%);
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--sams-primary);
  }
}

.logout-item {
  border: 1px solid #fee2e2;
  &:hover { background: #fef2f2; border-color: #fecaca; }
}
</style>
