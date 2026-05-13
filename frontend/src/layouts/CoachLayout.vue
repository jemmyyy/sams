<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-secondary text-white">
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
          SAMS Coach Portal
        </q-toolbar-title>

        <div>
          <q-btn flat round dense icon="notifications">
            <q-badge floating color="red">5</q-badge>
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
        <q-item-label header>Coach Menu</q-item-label>
        
        <q-item clickable v-ripple to="/coach/timetable">
          <q-item-section avatar>
            <q-icon name="event" />
          </q-item-section>
          <q-item-section>
            <q-item-label>My Schedule</q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/coach/attendance">
          <q-item-section avatar>
            <q-icon name="how_to_reg" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Mark Attendance</q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/coach/reports">
          <q-item-section avatar>
            <q-icon name="assignment" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Session Reports</q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/coach/ratings">
          <q-item-section avatar>
            <q-icon name="star" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Player Ratings</q-item-label>
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
