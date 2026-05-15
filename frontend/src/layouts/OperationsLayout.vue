<template>
  <q-layout view="lHh Lpr lFf" class="sams-layout-dark">
    <!-- Obsidian Header -->
    <q-header class="bg-surface-2 border-b">
      <q-toolbar class="q-py-md">
        <q-toolbar-title class="text-heading text-h5 text-white">
          SAMS<span class="text-primary">.</span><span class="text-weight-light text-grey-5 q-ml-sm">HQ</span>
        </q-toolbar-title>

        <!-- Desktop Navigation -->
        <div class="gt-xs q-mx-md">
          <q-tabs
            no-caps
            active-color="primary"
            indicator-color="primary"
            class="text-grey-5"
          >
            <q-route-tab to="/operations/dashboard" label="Dashboard" icon="dashboard" />
            <q-route-tab to="/operations/analytics" label="Insights" icon="analytics" />
            <q-route-tab to="/operations/reports" label="Reports" icon="assessment" />
            <q-route-tab to="/operations/players" label="Athletes" icon="people_alt" />
            <q-route-tab to="/operations/finances" label="Financials" icon="payments" />
          </q-tabs>
        </div>

        <q-space />

        <div class="row items-center q-gutter-md">
          <!-- Language Switcher -->
          <q-btn flat round icon="language" color="grey-5">
            <q-menu class="bg-surface-2 text-white border-b">
              <q-list style="min-width: 120px">
                <q-item clickable v-ripple @click="appStore.setLocale('en-US')" :active="appStore.locale === 'en-US'">
                  <q-item-section>English</q-item-section>
                </q-item>
                <q-item clickable v-ripple @click="appStore.setLocale('ar-EG')" :active="appStore.locale === 'ar-EG'">
                  <q-item-section>العربية</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>

          <q-btn flat round icon="notifications_none" color="grey-5">
            <q-badge floating color="victory-red" rounded />
          </q-btn>
          
          <q-separator vertical dark inset class="q-mx-sm opacity-20" />

          <div class="user-pill-dark row items-center q-pl-md q-pr-sm q-py-xs">
            <div class="column items-end q-mr-md gt-sm">
              <span class="text-weight-bold text-caption text-white">{{ authStore.user?.username }}</span>
              <span class="text-grey-6 text-min uppercase letter-spacing-1">Operations Command</span>
            </div>
            <q-avatar size="36px" class="shadow-sm border-2">
              <img src="https://cdn.quasar.dev/img/avatar.png">
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
        active-color="primary"
        indicator-color="primary"
        class="text-grey-5"
        align="justify"
      >
        <q-route-tab to="/operations/dashboard" icon="dashboard" label="Dash" />
        <q-route-tab to="/operations/analytics" icon="analytics" label="Stats" />
        <q-route-tab to="/operations/reports" icon="assessment" label="Docs" />
        <q-route-tab to="/operations/players" icon="people_alt" label="Athletes" />
        <q-route-tab to="/operations/finances" icon="payments" label="Cash" />
      </q-tabs>
    </q-footer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth';
import { useAppStore } from '../stores/app';

const authStore = useAuthStore();
const appStore = useAppStore();

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
.text-primary { color: var(--sams-primary); }
.text-victory-red { color: var(--sams-victory-red); }
.text-min { font-size: 11px; }

.user-pill-dark {
  background: var(--sams-surface-1);
  border-radius: 50px;
  border: 1px solid var(--sams-border);
  cursor: pointer;
  &:hover { border-color: var(--sams-primary); }
}

.opacity-20 { opacity: 0.2; }
.border-2 { border: 2px solid var(--sams-border); }
</style>
