<template>
  <q-page class="q-pa-xl animate-up">
    <!-- Header -->
    <div class="row items-center justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin text-white">Field Command</h1>
        <div class="text-subtitle1 text-grey-5">Session tracking and real-time attendance management.</div>
      </div>
      <q-btn unelevated class="sams-btn sams-btn-primary" label="Start New Session" icon="play_circle" />
    </div>

    <div class="row q-col-gutter-lg">
      <!-- Active Session Focus -->
      <div class="col-12 col-md-7">
        <q-card flat bordered class="sams-card overflow-hidden">
          <div class="q-pa-lg border-bottom row items-center justify-between bg-surface-2">
             <div class="row items-center">
                <q-badge rounded color="victory-red" class="q-mr-sm" />
                <span class="text-heading text-subtitle1 text-white">Live: Football Tactical U16</span>
             </div>
             <span class="text-mono text-grey-5 text-weight-bold">45m elapsed</span>
          </div>
          
          <div class="q-pa-xl bg-surface-1">
             <div class="row q-col-gutter-xl text-center">
                <div class="col-4">
                   <div class="text-heading text-h3 text-white">24</div>
                   <div class="text-caption text-grey-5 uppercase text-weight-bold">Present</div>
                </div>
                <div class="col-4 border-left border-right">
                   <div class="text-heading text-h3 text-grey-6">2</div>
                   <div class="text-caption text-grey-5 uppercase text-weight-bold">Absent</div>
                </div>
                <div class="col-4">
                   <div class="text-heading text-h3 text-primary">92%</div>
                   <div class="text-caption text-grey-5 uppercase text-weight-bold">Engaged</div>
                </div>
             </div>

             <div class="q-mt-xl">
                <div class="row items-center justify-between q-mb-sm text-white">
                   <span class="text-weight-bold">Current Phase: Drills</span>
                   <span class="text-weight-black text-primary">75%</span>
                </div>
                <q-linear-progress :value="0.75" color="primary" track-color="surface-2" rounded size="8px" />
             </div>
          </div>

          <div class="row border-top bg-surface-2">
             <q-btn flat color="white" class="col q-py-lg text-weight-bold" label="Attendance" icon="how_to_reg" to="/coach/attendance" />
             <q-separator vertical dark />
             <q-btn flat color="white" class="col q-py-lg text-weight-bold" label="Field Report" icon="history_edu" to="/coach/reports" />
          </div>
        </q-card>

        <!-- Upcoming List -->
        <div class="q-mt-xl">
           <div class="text-heading text-h6 q-mb-md text-white">Remaining Schedule</div>
           <div class="column q-gutter-y-sm">
              <div v-if="sessionsStore.loading" class="text-center q-pa-md"><q-spinner color="primary" /></div>
              <q-card v-else v-for="session in sessionsStore.sessions" :key="session.id" flat bordered class="sams-card q-pa-md row items-center">
                 <div class="text-h6 text-weight-bold q-mr-xl text-white">{{ session.start_time || '16:00' }}</div>
                 <div class="column">
                    <span class="text-weight-bold uppercase text-white">{{ session.series?.title || 'Training Session' }}</span>
                    <span class="text-caption text-grey-5">{{ session.venue?.name || 'TBD' }}</span>
                 </div>
                 <q-space />
                 <q-btn flat round icon="chevron_right" color="grey-5" />
              </q-card>
              <div v-if="!sessionsStore.loading && sessionsStore.sessions.length === 0" class="text-grey-5">
                 No upcoming sessions today.
              </div>
           </div>
        </div>
      </div>

      <!-- Coach Performance -->
      <div class="col-12 col-md-5">
        <q-card flat bordered class="sams-card q-pa-xl q-mb-lg bg-surface-1">
           <div class="text-heading text-h6 q-mb-xl text-white">Monthly Precision</div>
           <div class="column q-gutter-y-lg">
              <div v-for="stat in coachPerformance" :key="stat.label">
                 <div class="row justify-between q-mb-xs text-white">
                    <span class="text-caption text-grey-5 uppercase text-weight-bold">{{ stat.label }}</span>
                    <span class="text-weight-bold">{{ stat.value }}%</span>
                 </div>
                 <q-linear-progress :value="stat.value/100" color="primary" track-color="surface-2" rounded size="6px" />
              </div>
           </div>
        </q-card>

        <div class="row q-col-gutter-md">
           <div class="col-6" v-for="link in fieldLinks" :key="link.label">
              <q-card flat bordered class="sams-card bg-surface-2 q-pa-lg column items-center text-center cursor-pointer hover-elevate">
                 <q-icon :name="link.icon" size="32px" color="primary" class="q-mb-sm opacity-80" />
                 <span class="text-caption text-weight-bold uppercase text-white">{{ link.label }}</span>
              </q-card>
           </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useSessionsStore } from '../../stores/sessions';

const sessionsStore = useSessionsStore();

const coachPerformance = [
  { label: 'Reporting Rate', value: 100 },
  { label: 'Attendance Accuracy', value: 98 },
  { label: 'Session Rating', value: 85 },
];

const fieldLinks = [
  { label: 'Athlete Intel', icon: 'person_search' },
  { label: 'Skill Matrix', icon: 'military_tech' },
  { label: 'Venue Map', icon: 'map' },
  { label: 'Tactical Notes', icon: 'edit_note' },
];

onMounted(() => {
  sessionsStore.fetchSessions();
});
</script>

<style lang="scss" scoped>
.bg-surface-1 { background-color: var(--sams-surface-1); }
.bg-surface-2 { background-color: var(--sams-surface-2); }
.border-bottom { border-bottom: 1px solid var(--sams-border); }
.border-top { border-top: 1px solid var(--sams-border); }
.border-left { border-left: 1px solid var(--sams-border); }
.border-right { border-right: 1px solid var(--sams-border); }
.opacity-80 { opacity: 0.8; }

.hover-elevate {
  transition: transform 0.2s ease, border-color 0.2s ease;
  &:hover {
    transform: translateY(-4px);
    border-color: var(--sams-primary);
  }
}
</style>
