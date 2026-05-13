<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          SAMS Customer Portal
        </q-toolbar-title>

        <div>
           <q-btn flat round dense icon="notifications">
            <q-badge floating color="red">3</q-badge>
          </q-btn>
          <q-btn flat round dense icon="account_circle" class="q-ml-sm" />
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label header>Menu</q-item-label>
        
        <q-item clickable v-ripple to="/customer/timetable">
          <q-item-section avatar>
            <q-icon name="calendar_today" />
          </q-item-section>
          <q-item-section>
            <q-item-label>My Timetable</q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/customer/profile">
          <q-item-section avatar>
            <q-icon name="person" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Player Profile</q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/customer/cancellations">
          <q-item-section avatar>
            <q-icon name="event_busy" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Cancellation Requests</q-item-label>
          </q-item-section>
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
