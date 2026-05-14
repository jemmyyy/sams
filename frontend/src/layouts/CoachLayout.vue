<template>
  <q-layout view="lHh Lpr lFf" class="bg-grey-1">
    <q-header elevated class="bg-secondary text-white">
      <q-toolbar class="q-py-sm">
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title class="text-weight-bold letter-spacing-1">
          SAMS<span class="text-primary">.</span> COACH
        </q-toolbar-title>

        <div class="row items-center q-gutter-sm">
          <q-chip outline color="white" text-color="white" class="gt-xs">
            <q-avatar color="primary" text-color="white">P</q-avatar>
            PRO COACH
          </q-chip>
          <q-btn flat round dense icon="notifications">
            <q-badge floating color="primary" rounded>5</q-badge>
          </q-btn>
          <q-avatar size="32px" class="cursor-pointer">
            <img src="https://cdn.quasar.dev/img/boy-avatar.png">
          </q-avatar>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      class="bg-white"
      :width="280"
    >
      <q-list class="q-mt-md">
        <q-item-label header class="text-overline text-grey-6 q-pb-md">COACH COMMAND</q-item-label>
        
        <q-item clickable v-ripple to="/coach/timetable" class="menu-item q-mx-md q-mb-sm" active-class="active-coach-item">
          <q-item-section avatar>
            <q-icon name="sports" />
          </q-item-section>
          <q-item-section class="text-weight-medium">My Training Schedule</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/coach/attendance" class="menu-item q-mx-md q-mb-sm" active-class="active-coach-item">
          <q-item-section avatar>
            <q-icon name="check_circle" />
          </q-item-section>
          <q-item-section class="text-weight-medium">Mark Attendance</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/coach/reports" class="menu-item q-mx-md q-mb-sm" active-class="active-coach-item">
          <q-item-section avatar>
            <q-icon name="description" />
          </q-item-section>
          <q-item-section class="text-weight-medium">Session Reports</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/coach/ratings" class="menu-item q-mx-md q-mb-sm" active-class="active-coach-item">
          <q-item-section avatar>
            <q-icon name="stars" />
          </q-item-section>
          <q-item-section class="text-weight-medium">Rate Performance</q-item-section>
        </q-item>
        
        <q-separator class="q-my-lg" />
        
        <q-item clickable v-ripple class="menu-item q-mx-md text-negative">
          <q-item-section avatar>
            <q-icon name="power_settings_new" />
          </q-item-section>
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

const leftDrawerOpen = ref(false);

function toggleLeftDrawer () {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}
</script>

<style lang="scss" scoped>
.letter-spacing-1 { letter-spacing: 1px; }

.menu-item {
  border-radius: 12px;
  color: $primary;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba($secondary, 0.05);
  }
}

.active-coach-item {
  background: $secondary !important;
  color: white !important;
  box-shadow: 0 4px 15px rgba($secondary, 0.3);
}
</style>
