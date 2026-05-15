<template>
  <q-page class="q-pa-xl animate-up">
    <!-- Header -->
    <div class="row items-center justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin">Field Command</h1>
        <div class="text-subtitle1 text-grey-6">Session tracking and real-time attendance management.</div>
      </div>
      <q-btn unelevated class="sams-btn sams-btn-action" label="Start New Session" icon="play_circle" />
    </div>

    <div class="row q-col-gutter-lg">
      <!-- Active Session Focus -->
      <div class="col-12 col-md-7">
        <q-card flat bordered class="sams-card overflow-hidden">
          <div class="q-pa-lg border-bottom row items-center justify-between bg-red-50">
             <div class="row items-center">
                <q-badge rounded color="red" class="q-mr-sm" />
                <span class="text-heading text-subtitle1 text-red-9">Live: Football Tactical U16</span>
             </div>
             <span class="text-mono text-grey-6 text-weight-bold">45m elapsed</span>
          </div>
          
          <div class="q-pa-xl">
             <div class="row q-col-gutter-xl text-center">
                <div class="col-4">
                   <div class="text-heading text-h3">24</div>
                   <div class="text-caption text-grey-6 uppercase text-weight-bold">Present</div>
                </div>
                <div class="col-4 border-left border-right">
                   <div class="text-heading text-h3 text-grey-4">2</div>
                   <div class="text-caption text-grey-6 uppercase text-weight-bold">Absent</div>
                </div>
                <div class="col-4">
                   <div class="text-heading text-h3 text-primary">92%</div>
                   <div class="text-caption text-grey-6 uppercase text-weight-bold">Engaged</div>
                </div>
             </div>

             <div class="q-mt-xl">
                <div class="row items-center justify-between q-mb-sm">
                   <span class="text-weight-bold">Current Phase: Drills</span>
                   <span class="text-weight-black text-primary">75%</span>
                </div>
                <q-linear-progress :value="0.75" color="primary" track-color="blue-1" rounded size="8px" />
             </div>
          </div>

          <div class="row border-top">
             <q-btn flat class="col q-py-lg text-weight-bold" label="Attendance" icon="how_to_reg" />
             <q-separator vertical />
             <q-btn flat class="col q-py-lg text-weight-bold" label="Field Report" icon="history_edu" />
          </div>
        </q-card>

        <!-- Upcoming List -->
        <div class="q-mt-xl">
           <div class="text-heading text-h6 q-mb-md">Remaining Schedule</div>
           <div class="column q-gutter-y-sm">
              <q-card v-for="i in [1, 2]" :key="i" flat bordered class="sams-card q-pa-md row items-center">
                 <div class="text-h6 text-weight-bold q-mr-xl">16:00</div>
                 <div class="column">
                    <span class="text-weight-bold uppercase">Stamina Conditioning</span>
                    <span class="text-caption text-grey-6">Pitch 02 // Group Alpha</span>
                 </div>
                 <q-space />
                 <q-btn flat round icon="chevron_right" color="grey-4" />
              </q-card>
           </div>
        </div>
      </div>

      <!-- Coach Performance -->
      <div class="col-12 col-md-5">
        <q-card flat bordered class="sams-card q-pa-xl q-mb-lg">
           <div class="text-heading text-h6 q-mb-xl">Monthly Precision</div>
           <div class="column q-gutter-y-lg">
              <div v-for="stat in coachPerformance" :key="stat.label">
                 <div class="row justify-between q-mb-xs">
                    <span class="text-caption text-grey-6 uppercase text-weight-bold">{{ stat.label }}</span>
                    <span class="text-weight-bold">{{ stat.value }}%</span>
                 </div>
                 <q-linear-progress :value="stat.value/100" color="navy" track-color="slate-100" rounded size="6px" />
              </div>
           </div>
        </q-card>

        <div class="row q-col-gutter-md">
           <div class="col-6" v-for="link in fieldLinks" :key="link.label">
              <q-card flat bordered class="sams-card q-pa-lg column items-center text-center cursor-pointer">
                 <q-icon :name="link.icon" size="32px" color="primary" class="q-mb-sm opacity-40" />
                 <span class="text-caption text-weight-bold uppercase">{{ link.label }}</span>
              </q-card>
           </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
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
</script>

<style lang="scss" scoped>
.border-bottom { border-bottom: 1px solid var(--sams-border); }
.border-top { border-top: 1px solid var(--sams-border); }
.opacity-40 { opacity: 0.4; }
</style>
