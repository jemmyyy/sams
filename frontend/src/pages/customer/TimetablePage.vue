<template>
  <q-page class="q-pa-xl animate-up">
    <!-- Welcome Header -->
    <div class="row items-center justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin text-white">Welcome Back, {{ authStore.user?.first_name || 'Champion' }}</h1>
        <div class="text-subtitle1 text-grey-5">Track your academy journey and upcoming training sessions.</div>
      </div>
      <q-btn unelevated color="primary" class="sams-btn" label="Academy Calendar" icon="event" />
    </div>

    <div class="row q-col-gutter-lg">
      <!-- Athlete Profile Card -->
      <div class="col-12 col-md-4">
        <q-card flat bordered class="sams-card q-pa-xl column items-center text-center">
           <q-avatar size="110px" class="q-mb-lg shadow-sm border-2">
              <img src="https://cdn.quasar.dev/img/avatar.png">
           </q-avatar>
           <div class="text-heading text-h5 text-white">Elite Junior</div>
           <div class="text-caption text-grey-5 q-mb-xl uppercase letter-spacing-1">Rank: Academy Prospect</div>

           <div class="row full-width q-col-gutter-md q-mb-xl">
              <div class="col-6">
                 <div class="text-heading text-h4 text-primary">8.4</div>
                 <div class="text-caption text-grey-6 uppercase text-weight-bold">Skill Index</div>
              </div>
              <div class="col-6 border-left">
                 <div class="text-heading text-h4 text-white">#04</div>
                 <div class="text-caption text-grey-6 uppercase text-weight-bold">Academy Rank</div>
              </div>
           </div>

           <div class="column full-width q-gutter-y-md">
              <q-btn unelevated color="surface-2" text-color="primary" class="full-width text-weight-bold sams-btn border-b" label="Profile Settings" icon="person" no-caps />
              <q-btn flat color="grey-6" class="full-width text-weight-bold" label="Billing History" icon="receipt_long" no-caps />
           </div>
        </q-card>
      </div>

      <!-- Schedule & Performance -->
      <div class="col-12 col-md-8">
        <q-card flat bordered class="sams-card">
           <div class="q-pa-lg border-bottom row items-center justify-between bg-surface-2">
              <div class="text-heading text-subtitle1 text-white">Your Training Timeline</div>
              <q-badge color="primary" text-color="white" class="q-px-md q-py-xs text-weight-bold">Active Enrollment</q-badge>
           </div>
           
           <div class="q-pa-xl">
              <q-timeline color="primary" dark>
                <div v-if="sessionsStore.loading" class="text-center"><q-spinner color="primary" size="2em"/></div>
                <q-timeline-entry
                  v-else
                  v-for="session in sessionsStore.sessions"
                  :key="session.id"
                  :title="session.series?.title || 'Training Session'"
                  :subtitle="session.start_time"
                  icon="sports_soccer"
                  class="text-white"
                >
                  <div class="row items-center q-gutter-sm q-mt-sm">
                     <q-badge outline color="grey-5" :label="session.venue?.name || 'TBA'" />
                  </div>
                </q-timeline-entry>
              </q-timeline>
           </div>
        </q-card>

        <div class="row q-col-gutter-lg q-mt-md">
           <div class="col-6" v-for="stat in athleteSummary" :key="stat.label">
              <q-card flat bordered class="sams-card q-pa-lg">
                 <div class="row items-center justify-between q-mb-sm">
                    <span class="text-caption text-grey-6 uppercase text-weight-bold">{{ stat.label }}</span>
                    <q-icon :name="stat.icon" size="20px" :color="stat.color" />
                 </div>
                 <div class="text-heading text-h4" :style="{ color: stat.valColor }">{{ stat.value }}</div>
              </q-card>
           </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useAuthStore } from '../../stores/auth';
import { useSessionsStore } from '../../stores/sessions';

const authStore = useAuthStore();
const sessionsStore = useSessionsStore();

const athleteSummary = [
  { label: 'Latest Rating', value: 'A+', icon: 'military_tech', color: 'primary', valColor: 'var(--sams-primary)' },
  { label: 'Outstanding Balance', value: '500 EGP', icon: 'error_outline', color: 'victory-red', valColor: 'var(--sams-victory-red)' },
];

onMounted(() => {
  sessionsStore.fetchSessions();
});
</script>

<style lang="scss" scoped>
.bg-surface-2 { background-color: var(--sams-surface-2); }
.border-bottom { border-bottom: 1px solid var(--sams-border); }
.border-b { border: 1px solid var(--sams-border); }
.border-left { border-left: 1px solid var(--sams-border); }
.border-2 { border: 2px solid var(--sams-border); }
</style>
