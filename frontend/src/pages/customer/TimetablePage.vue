<template>
  <q-page class="q-pa-xl">
    <!-- Welcome Header -->
    <div class="row items-center justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-apex heading-lg text-navy no-margin">Welcome Back, {{ authStore.user?.first_name || 'Champion' }}</h1>
        <div class="text-subtitle1 text-grey-6">Track your journey and upcoming training sessions.</div>
      </div>
      <q-btn unelevated color="blue-6" class="apex-btn-primary" label="Academy Calendar" icon="event" />
    </div>

    <div class="row q-col-gutter-lg">
      <!-- Athlete Profile Overview -->
      <div class="col-12 col-md-4">
        <div class="apex-card q-pa-xl column items-center text-center">
           <q-avatar size="100px" class="apex-avatar q-mb-lg" border="3px solid #3b82f6">
              <img src="https://cdn.quasar.dev/img/avatar.png">
           </q-avatar>
           <div class="text-apex text-h5 text-navy">Junior Academy</div>
           <div class="text-caption text-grey-5 q-mb-xl uppercase letter-spacing-1">Rank: Elite Prospect</div>

           <div class="row full-width q-col-gutter-md q-mb-xl">
              <div class="col-6">
                 <div class="text-apex text-h4 text-blue-6">8.4</div>
                 <div class="text-min text-grey-6 uppercase font-weight-bold">Skill Index</div>
              </div>
              <div class="col-6 border-left">
                 <div class="text-apex text-h4 text-navy">#04</div>
                 <div class="text-min text-grey-6 uppercase font-weight-bold">Academy Rank</div>
              </div>
           </div>

           <div class="column full-width q-gutter-y-md">
              <q-btn unelevated color="blue-1" text-color="blue-9" class="full-width text-weight-bold" label="Profile Intel" icon="person" no-caps />
              <q-btn flat color="grey-7" class="full-width text-weight-bold" label="Billing History" icon="receipt_long" no-caps />
           </div>
        </div>
      </div>

      <!-- Training Schedule -->
      <div class="col-12 col-md-8">
        <div class="apex-card">
           <div class="q-pa-lg border-bottom row items-center justify-between">
              <div class="text-apex text-h6 text-navy">Upcoming Engagements</div>
              <q-badge color="blue-1" text-color="blue-9" class="q-px-md q-py-xs text-weight-bold">Next: Tomorrow</q-badge>
           </div>
           
           <div class="q-pa-xl">
              <q-timeline color="blue-6">
                <q-timeline-entry
                  title="Technical Drill: Ball Control"
                  subtitle="Tuesday, May 16 // 16:00 - 18:00"
                  icon="sports_soccer"
                >
                  <div class="row items-center q-gutter-md q-mt-sm">
                     <div class="schedule-tag">PITCH_01</div>
                     <div class="schedule-tag tag-blue">COACH_AHMED</div>
                  </div>
                </q-timeline-entry>

                <q-timeline-entry
                  title="Stamina & Conditioning"
                  subtitle="Thursday, May 18 // 17:00 - 19:00"
                  icon="fitness_center"
                >
                  <div class="row items-center q-gutter-md q-mt-sm">
                     <div class="schedule-tag">INDOOR_HALL</div>
                     <div class="schedule-tag tag-blue">COACH_OMAR</div>
                  </div>
                </q-timeline-entry>
              </q-timeline>
           </div>
        </div>

        <div class="row q-col-gutter-lg q-mt-md">
           <div class="col-6" v-for="stat in athleteSummary" :key="stat.label">
              <div class="apex-card q-pa-lg">
                 <div class="row items-center justify-between q-mb-md">
                    <span class="text-caption text-grey-6 uppercase font-weight-bold letter-spacing-1">{{ stat.label }}</span>
                    <q-icon :name="stat.icon" size="20px" :color="stat.color" />
                 </div>
                 <div class="text-apex text-h4" :style="{ color: stat.valColor }">{{ stat.value }}</div>
              </div>
           </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useAuthStore } from '../../stores/auth';
const authStore = useAuthStore();

const athleteSummary = [
  { label: 'Recent Rating', value: 'A+', icon: 'military_tech', color: 'blue-6', valColor: '#2563eb' },
  { label: 'Account Balance', value: '500 EGP', icon: 'warning', color: 'red-6', valColor: '#e11d48' },
];
</script>

<style lang="scss" scoped>
.text-navy { color: var(--sams-navy); }
.border-bottom { border-bottom: 1px solid var(--sams-border); }
.text-min { font-size: 11px; }

.apex-avatar {
  background: white;
  padding: 4px;
}

.schedule-tag {
  background: #f1f5f9;
  padding: 4px 12px;
  border-radius: 6px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  color: #64748b;
  &.tag-blue { background: #eff6ff; color: #2563eb; }
}

.opacity-10 { opacity: 0.1; }
</style>
