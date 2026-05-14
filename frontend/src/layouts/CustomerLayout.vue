<template>
  <q-layout view="lHh Lpr lFf" class="bg-grey-1">
    <q-header elevated class="bg-primary text-white">
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
          SAMS<span class="text-secondary">.</span> CUSTOMER
        </q-toolbar-title>

        <div class="row items-center q-gutter-sm">
          <q-btn flat round dense icon="notifications" class="text-grey-4">
            <q-badge floating color="secondary" rounded>3</q-badge>
          </q-btn>
          <q-avatar size="32px" class="cursor-pointer">
            <img src="https://cdn.quasar.dev/img/avatar.png">
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
        <q-item-label header class="text-overline text-grey-6 q-pb-md">PORTAL MENU</q-item-label>
        
        <q-item clickable v-ripple to="/customer/timetable" class="menu-item q-mx-md q-mb-sm" active-class="active-menu-item">
          <q-item-section avatar>
            <q-icon name="calendar_today" />
          </q-item-section>
          <q-item-section class="text-weight-medium">My Timetable</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/customer/profile" class="menu-item q-mx-md q-mb-sm" active-class="active-menu-item">
          <q-item-section avatar>
            <q-icon name="person" />
          </q-item-section>
          <q-item-section class="text-weight-medium">Player Profile</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/customer/cancellations" class="menu-item q-mx-md q-mb-sm" active-class="active-menu-item">
          <q-item-section avatar>
            <q-icon name="event_busy" />
          </q-item-section>
          <q-item-section class="text-weight-medium">Cancellations</q-item-section>
        </q-item>
        
        <q-separator class="q-my-lg" />
        
        <q-item clickable v-ripple class="menu-item q-mx-md text-negative">
          <q-item-section avatar>
            <q-icon name="logout" />
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
    background: rgba($primary, 0.05);
  }
}

.active-menu-item {
  background: $primary !important;
  color: white !important;
  box-shadow: 0 4px 15px rgba($primary, 0.3);
}
</style>
