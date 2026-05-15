<template>
  <q-layout view="lHh Lpr lFf" class="apex-layout">
    <q-header class="bg-white text-navy border-bottom">
      <q-toolbar class="q-py-md max-w-xl">
        <q-btn flat dense round icon="menu" @click="toggleLeftDrawer" class="q-mr-sm" />
        <q-toolbar-title class="text-apex text-h5">
          SAMS<span class="text-blue-6">.</span><span class="text-weight-light text-grey-6 q-ml-sm">ARENA</span>
        </q-toolbar-title>
        <q-space />
        <div class="row items-center q-gutter-md">
          <q-btn flat round icon="notifications_none" color="grey-7">
            <q-badge floating color="blue-6" rounded>3</q-badge>
          </q-btn>
          <q-separator vertical inset class="q-mx-sm" />
          <div class="user-profile row items-center q-gutter-sm pointer" @click="toggleLeftDrawer">
            <div class="column items-end gt-xs">
              <span class="text-weight-bold text-caption text-navy">{{ authStore.user?.first_name || authStore.user?.username }}</span>
              <span class="text-grey-6 text-min uppercase">Elite Member</span>
            </div>
            <q-avatar size="40px" class="apex-avatar shadow-sm">
              <img src="https://cdn.quasar.dev/img/avatar.png">
            </q-avatar>
          </div>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered class="apex-sidebar" :width="280">
      <div class="column full-height">
        <div class="q-mt-xl q-px-xl q-mb-lg">
           <div class="text-overline text-grey-5 letter-spacing-1">Athlete Portal</div>
        </div>
        <q-list class="q-px-md q-gutter-y-xs">
          <q-item clickable v-ripple to="/customer/timetable" class="apex-menu-item" active-class="active-item-blue">
            <q-item-section avatar><q-icon name="event" size="22px" /></q-item-section>
            <q-item-section class="text-weight-medium">My Timetable</q-item-section>
          </q-item>
          <q-item clickable v-ripple to="/customer/profile" class="apex-menu-item" active-class="active-item-blue">
            <q-item-section avatar><q-icon name="person" size="22px" /></q-item-section>
            <q-item-section class="text-weight-medium">Athlete Profile</q-item-section>
          </q-item>
          <q-item clickable v-ripple to="/customer/cancellations" class="apex-menu-item" active-class="active-item-blue">
            <q-item-section avatar><q-icon name="event_busy" size="22px" /></q-item-section>
            <q-item-section class="text-weight-medium">Cancellations</q-item-section>
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

.active-item-blue {
  color: #2563eb !important;
  background: #eff6ff !important;
  font-weight: 700 !important;
  &::after {
    content: '';
    position: absolute;
    right: 8px; top: 50%; transform: translateY(-50%);
    width: 6px; height: 6px; border-radius: 50%;
    background: #2563eb;
  }
}

.logout-btn {
  border: 1px solid #fee2e2;
  &:hover { background: #fef2f2; border-color: #fecaca; }
}
</style>
