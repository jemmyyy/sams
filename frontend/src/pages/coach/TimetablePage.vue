<template>
  <q-page class="coach-portal q-pa-lg">
    <div class="row items-center q-mb-xl">
      <div class="col">
        <div class="text-overline text-accent text-weight-bolder letter-spacing-2">FIELD COMMAND</div>
        <h1 class="text-h3 text-white text-weight-black q-my-none">Coach Dashboard</h1>
        <p class="text-grey-4 q-mt-sm">Track athlete progress and session performance</p>
      </div>
      <div class="col-auto">
        <q-btn color="accent" icon="play_arrow" label="Start Session" rounded class="q-px-lg shadow-10 pulse-animation" />
      </div>
    </div>

    <div class="row q-col-gutter-lg">
      <!-- Session Focus -->
      <div class="col-12 col-md-7">
        <q-card flat class="session-card glass-card text-white">
          <q-card-section class="row items-center">
            <div>
              <div class="text-h5 text-weight-bold">Upcoming: Football Intermediate</div>
              <div class="text-subtitle2 text-grey-4">Starts in 15 minutes • Venue: Main Pitch</div>
            </div>
            <q-space />
            <q-badge color="accent" class="q-pa-sm" rounded>LIVE SOON</q-badge>
          </q-card-section>
          
          <q-separator dark class="opacity-10" />

          <q-card-section class="row q-col-gutter-md">
            <div class="col-4 text-center">
              <div class="text-h4 text-weight-bold">24</div>
              <div class="text-caption text-grey-5">ENROLLED</div>
            </div>
            <div class="col-4 text-center">
              <div class="text-h4 text-weight-bold">18</div>
              <div class="text-caption text-grey-5">CHECKED IN</div>
            </div>
            <div class="col-4 text-center text-accent">
              <div class="text-h4 text-weight-bold">85%</div>
              <div class="text-caption text-grey-5">UTILIZATION</div>
            </div>
          </q-card-section>

          <q-card-actions align="center" class="q-pb-lg">
            <q-btn outline color="accent" label="View Roster" class="q-px-xl" rounded />
          </q-card-actions>
        </q-card>

        <!-- Timetable Preview -->
        <div class="q-mt-lg">
          <div class="text-h6 text-white text-weight-bold q-mb-md">Your Schedule Today</div>
          <div class="column q-gutter-y-sm">
            <q-card v-for="s in [1, 2]" :key="s" flat class="mini-session-card glass-card text-white q-pa-md">
              <div class="row items-center">
                <div class="time-box q-mr-md">16:00</div>
                <div>
                  <div class="text-weight-bold">Football Beginners - Group A</div>
                  <div class="text-caption text-grey-4">Main Pitch • 20 Players</div>
                </div>
                <q-space />
                <q-btn flat round dense icon="chevron_right" />
              </div>
            </q-card>
          </div>
        </div>
      </div>

      <!-- Performance & Reports -->
      <div class="col-12 col-md-5">
        <q-card flat class="performance-card glass-card text-white q-mb-lg">
          <q-card-section>
            <div class="text-h6 text-weight-bold">Coach Stats</div>
            <div class="text-caption text-grey-4">Month of May Performance</div>
          </q-card-section>
          <q-card-section class="column q-gutter-y-lg">
            <div>
              <div class="row items-center q-mb-xs">
                <span class="text-caption text-grey-4">Attendance Consistency</span>
                <q-space />
                <span class="text-weight-bold text-accent">92%</span>
              </div>
              <q-linear-progress :value="0.92" color="accent" track-color="grey-9" rounded />
            </div>
            <div>
              <div class="row items-center q-mb-xs">
                <span class="text-caption text-grey-4">Report Submission Rate</span>
                <q-space />
                <span class="text-weight-bold text-info">100%</span>
              </div>
              <q-linear-progress :value="1.0" color="info" track-color="grey-9" rounded />
            </div>
          </q-card-section>
        </q-card>

        <q-card flat class="actions-card glass-card text-white">
          <q-list dark padding>
            <q-item clickable v-ripple to="/coach/attendance">
              <q-item-section avatar><q-icon name="how_to_reg" color="accent" /></q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold">Mark Attendance</q-item-label>
                <q-item-label caption class="text-grey-4">Open active session roster</q-item-label>
              </q-item-section>
            </q-item>
            <q-item clickable v-ripple to="/coach/reports">
              <q-item-section avatar><q-icon name="summarize" color="info" /></q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold">Session Reports</q-item-label>
                <q-item-label caption class="text-grey-4">Submit summary and feedback</q-item-label>
              </q-item-section>
            </q-item>
            <q-item clickable v-ripple to="/coach/ratings">
              <q-item-section avatar><q-icon name="star" color="warning" /></q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold">Rate Athletes</q-item-label>
                <q-item-label caption class="text-grey-4">Skill assessment and levels</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
// Coach Portal Logic
</script>

<style lang="scss" scoped>
.coach-portal {
  background: #0f172a;
  min-height: 100vh;
}

.letter-spacing-2 { letter-spacing: 2px; }

.glass-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
}

.time-box {
  background: rgba($accent, 0.1);
  color: $accent;
  padding: 8px 12px;
  border-radius: 12px;
  font-weight: 800;
  font-family: 'JetBrains Mono', monospace;
}

.pulse-animation {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); box-shadow: 0 0 0 0 rgba($accent, 0.4); }
  70% { transform: scale(1.05); box-shadow: 0 0 0 15px rgba($accent, 0); }
  100% { transform: scale(1); box-shadow: 0 0 0 0 rgba($accent, 0); }
}

.opacity-10 { opacity: 0.1; }
</style>
