<template>
  <q-layout view="lHh Lpr lFf" class="sams-layout-dark">
    <!-- Obsidian Header -->
    <q-header class="bg-surface-2 border-b">
      <q-toolbar class="q-py-md">
        <q-toolbar-title class="text-heading text-h5 text-white">
          SAMS<span class="text-success">.</span><span class="text-weight-light text-grey-5 q-ml-sm">Field</span>
        </q-toolbar-title>

        <!-- Desktop Navigation -->
        <div class="gt-xs q-mx-md">
          <q-tabs
            no-caps
            active-color="success"
            indicator-color="success"
            class="text-grey-5"
          >
            <q-route-tab to="/coach/timetable" label="Schedule" icon="calendar_today" />
            <q-route-tab to="/coach/attendance" label="Attendance" icon="fact_check" />
            <q-route-tab to="/coach/reports" label="Reports" icon="history_edu" />
            <q-route-tab to="/coach/ratings" label="Ratings" icon="stars" />
            <q-route-tab to="/coach/cancellations" label="Cancellations" icon="cancel" />
            <q-route-tab to="/coach/notifications" label="Messages" icon="notifications" />
          </q-tabs>
        </div>

        <q-space />

        <div class="row items-center q-gutter-md">
          <q-btn flat round icon="notifications_none" color="grey-5" aria-label="Notifications">
            <q-badge floating color="success" rounded />
          </q-btn>
          
          <q-separator vertical dark inset class="q-mx-sm opacity-20" />

          <div class="user-pill-dark row items-center q-pl-md q-pr-sm q-py-xs">
            <div class="column items-end q-mr-md gt-sm">
              <span class="text-weight-bold text-caption text-white">{{ authStore.user?.first_name }} {{ authStore.user?.last_name }}</span>
              <span class="text-grey-6 text-min uppercase letter-spacing-1">Academy Coach</span>
            </div>
            <q-avatar size="36px" class="shadow-sm border-2">
              <img src="https://cdn.quasar.dev/img/boy-avatar.png">
            </q-avatar>
            <q-menu class="bg-surface-2 text-white border-b">
              <q-list style="min-width: 150px">
                <q-item clickable v-ripple @click="logout" class="text-victory-red">
                  <q-item-section avatar><q-icon name="logout" /></q-item-section>
                  <q-item-section>Sign Out</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </div>
        </div>
      </q-toolbar>
    </q-header>

    <!-- Mobile Bottom Navigation -->
    <q-footer class="xs bg-surface-1 border-t">
      <q-tabs
        no-caps
        active-color="success"
        indicator-color="success"
        class="text-grey-5"
        align="justify"
      >
        <q-route-tab to="/coach/timetable" icon="calendar_today" label="Sched" />
        <q-route-tab to="/coach/attendance" icon="fact_check" label="Att" />
        <q-route-tab to="/coach/notifications" icon="notifications" label="Inbox" />
      </q-tabs>
    </q-footer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();

function logout() {
  authStore.logout();
}
</script>

<style lang="scss" scoped>
.sams-layout-dark { background-color: var(--sams-bg); }
.bg-surface-1 { background-color: var(--sams-surface-1); }
.bg-surface-2 { background-color: var(--sams-surface-2); }
.border-b { border-bottom: 1px solid var(--sams-border); }
.border-t { border-top: 1px solid var(--sams-border); }
.text-success { color: var(--sams-success); }
.text-victory-red { color: var(--sams-victory-red); }
.text-min { font-size: 11px; }

.user-pill-dark {
  background: var(--sams-surface-1);
  border-radius: 50px;
  border: 1px solid var(--sams-border);
  cursor: pointer;
  &:hover { border-color: var(--sams-success); }
}

.opacity-20 { opacity: 0.2; }
.border-2 { border: 2px solid var(--sams-border); }
</style>
