<template>
  <q-page class="q-pa-xl">
    <!-- Field Header -->
    <div class="row items-center justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-apex heading-lg text-navy no-margin">Field Command</h1>
        <div class="text-subtitle1 text-grey-6">Real-time session management and tactical oversight.</div>
      </div>
      <q-btn unelevated class="apex-btn-victory" label="Deploy Active Session" icon="play_circle_filled" />
    </div>

    <div class="row q-col-gutter-lg">
      <!-- Live Session Focus -->
      <div class="col-12 col-md-7">
        <div class="apex-card overflow-hidden">
          <div class="q-pa-lg border-bottom row items-center justify-between" style="background: #fff1f2">
             <div class="row items-center">
                <div class="live-indicator q-mr-md"></div>
                <span class="text-apex text-subtitle1 text-victory">Live: Football Tactical U16</span>
             </div>
             <span class="text-mono text-grey-7 font-weight-bold">Started 45m ago</span>
          </div>
          
          <div class="q-pa-xl">
             <div class="row q-col-gutter-xl text-center">
                <div class="col-4">
                   <div class="text-apex text-h3 text-navy">24</div>
                   <div class="text-caption text-grey-6 uppercase font-weight-bold">Present</div>
                </div>
                <div class="col-4 border-left border-right">
                   <div class="text-apex text-h3 text-grey-4">2</div>
                   <div class="text-caption text-grey-6 uppercase font-weight-bold">Absent</div>
                </div>
                <div class="col-4">
                   <div class="text-apex text-h3 text-victory">92%</div>
                   <div class="text-caption text-grey-6 uppercase font-weight-bold">Engagement</div>
                </div>
             </div>

             <div class="q-mt-xl">
                <div class="row items-center justify-between q-mb-sm">
                   <span class="text-weight-bold text-navy">Session Completion</span>
                   <span class="text-weight-black text-victory">75%</span>
                </div>
                <q-linear-progress :value="0.75" color="victory" track-color="red-1" rounded size="10px" />
             </div>
          </div>

          <div class="row border-top">
             <q-btn flat class="col q-py-lg text-weight-bold text-navy" label="Mark Attendance" icon="check_circle_outline" />
             <q-separator vertical class="opacity-10" />
             <q-btn flat class="col q-py-lg text-weight-bold text-navy" label="Field Report" icon="history_edu" />
          </div>
        </div>

        <!-- Timeline -->
        <div class="q-mt-xl">
           <div class="text-apex text-h6 text-navy q-mb-lg">Today's Sorties</div>
           <div class="column q-gutter-y-sm">
              <div v-for="i in [1, 2]" :key="i" class="apex-card q-pa-md row items-center">
                 <div class="time-block q-mr-xl text-navy">16:00</div>
                 <div class="column">
                    <span class="text-weight-bold text-navy uppercase">Stamina Conditioning</span>
                    <span class="text-caption text-grey-6">Pitch_02 // Group_Alpha</span>
                 </div>
                 <q-space />
                 <q-btn flat round icon="chevron_right" color="grey-4" />
              </div>
           </div>
        </div>
      </div>

      <!-- Efficiency & Quick Access -->
      <div class="col-12 col-md-5">
        <div class="apex-card q-pa-xl q-mb-lg">
           <div class="text-apex text-h6 text-navy q-mb-xl">Monthly Performance</div>
           <div class="column q-gutter-y-lg">
              <div v-for="stat in coachPerformance" :key="stat.label">
                 <div class="row items-center justify-between q-mb-xs">
                    <span class="text-caption text-grey-6 uppercase font-weight-bold">{{ stat.label }}</span>
                    <span class="text-weight-black text-navy">{{ stat.value }}%</span>
                 </div>
                 <q-linear-progress :value="stat.value/100" color="navy" track-color="blue-1" rounded size="6px" />
              </div>
           </div>
        </div>

        <div class="row q-col-gutter-md">
           <div class="col-6" v-for="link in fieldLinks" :key="link.label">
              <div class="apex-card q-pa-lg column items-center text-center cursor-pointer">
                 <q-icon :name="link.icon" size="32px" color="navy" class="q-mb-sm opacity-40" />
                 <span class="text-caption text-weight-bold text-navy uppercase letter-spacing-1">{{ link.label }}</span>
              </div>
           </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
const coachPerformance = [
  { label: 'Reporting Rate', value: 100 },
  { label: 'Attendance Precision', value: 98 },
  { label: 'Session Rating Avg', value: 85 },
];

const fieldLinks = [
  { label: 'Athlete Intel', icon: 'manage_search' },
  { label: 'Skill Matrix', icon: 'military_tech' },
  { label: 'Venue Status', icon: 'map' },
  { label: 'Tactical Notes', icon: 'edit_note' },
];
</script>

<style lang="scss" scoped>
.text-navy { color: var(--sams-navy); }
.text-victory { color: var(--sams-victory-red); }
.border-bottom { border-bottom: 1px solid var(--sams-border); }
.border-top { border-top: 1px solid var(--sams-border); }

.live-indicator {
  width: 10px; height: 10px;
  background: var(--sams-victory-red);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--sams-victory-red);
  animation: pulse-red 1.5s infinite;
}

@keyframes pulse-red { 0% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.5); opacity: 0.5; } 100% { transform: scale(1); opacity: 1; } }

.time-block {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 800; font-size: 20px;
}

.opacity-10 { opacity: 0.1; }
.opacity-40 { opacity: 0.4; }
</style>
