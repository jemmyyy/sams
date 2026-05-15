<template>
  <q-page class="customer-portal q-pa-lg">
    <div class="row items-center q-mb-xl">
      <div class="col">
        <div class="text-overline text-secondary text-weight-bolder letter-spacing-2">ATHLETE ARENA</div>
        <h1 class="text-h3 text-white text-weight-black q-my-none">Welcome, {{ authStore.user?.first_name || 'Champion' }}</h1>
        <p class="text-grey-4 q-mt-sm">Manage training, view ratings, and track progress</p>
      </div>
    </div>

    <div class="row q-col-gutter-lg">
      <!-- Athlete Profile Overview -->
      <div class="col-12 col-md-4">
        <q-card flat class="profile-card glass-card text-white">
          <q-card-section class="column items-center q-py-xl">
            <q-avatar size="100px" class="q-mb-md shadow-10 border-accent">
              <img src="https://cdn.quasar.dev/img/avatar.png">
            </q-avatar>
            <div class="text-h5 text-weight-bold">Junior Academy</div>
            <div class="text-caption text-grey-4">Registration: #ELITE-2026-042</div>
            
            <div class="row q-mt-lg q-gutter-x-md">
              <div class="text-center">
                <div class="text-h6 text-weight-bold">B1</div>
                <div class="text-caption text-grey-5 uppercase">Level</div>
              </div>
              <q-separator vertical dark class="opacity-10" />
              <div class="text-center">
                <div class="text-h6 text-weight-bold">85%</div>
                <div class="text-caption text-grey-5 uppercase">Skill</div>
              </div>
            </div>
          </q-card-section>
          
          <q-list dark padding class="q-pb-md">
            <q-item clickable v-ripple>
              <q-item-section avatar><q-icon name="person" color="secondary" /></q-item-section>
              <q-item-section>Profile Settings</q-item-section>
            </q-item>
            <q-item clickable v-ripple>
              <q-item-section avatar><q-icon name="account_balance_wallet" color="secondary" /></q-item-section>
              <q-item-section>Payment History</q-item-section>
            </q-item>
          </q-list>
        </q-card>
      </div>

      <!-- Schedule & Timeline -->
      <div class="col-12 col-md-8">
        <q-card flat class="schedule-card glass-card text-white">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6 text-weight-bold">Upcoming Sessions</div>
            <q-space />
            <q-btn flat color="secondary" label="Full Calendar" no-caps />
          </q-card-section>
          
          <q-card-section>
            <q-timeline color="secondary" dark>
              <q-timeline-entry
                title="Football Tactical Training"
                subtitle="Tomorrow, 16:00 - 18:00"
                icon="sports_soccer"
              >
                <div>Venue: Main Field • Coach: Ahmed Salah</div>
              </q-timeline-entry>

              <q-timeline-entry
                title="Physical Conditioning"
                subtitle="Wednesday, 17:00 - 19:00"
                icon="fitness_center"
              >
                <div>Venue: Indoor Hall • Coach: Omar Hassan</div>
              </q-timeline-entry>
            </q-timeline>
          </q-card-section>
        </q-card>

        <div class="row q-col-gutter-md q-mt-md">
          <div class="col-6">
            <q-card flat class="stat-box glass-card text-white text-center q-pa-md">
              <q-icon name="trending_up" size="32px" color="secondary" class="q-mb-sm" />
              <div class="text-h4 text-weight-bold">A+</div>
              <div class="text-caption text-grey-4">RECENT RATING</div>
            </q-card>
          </div>
          <div class="col-6">
            <q-card flat class="stat-box glass-card text-white text-center q-pa-md">
              <q-icon name="payments" size="32px" color="negative" class="q-mb-sm" />
              <div class="text-h4 text-weight-bold">500</div>
              <div class="text-caption text-grey-4">DUE AMOUNT (EGP)</div>
            </q-card>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useAuthStore } from '../../stores/auth';
const authStore = useAuthStore();
</script>

<style lang="scss" scoped>
.customer-portal {
  background: #020617;
  min-height: 100vh;
}

.letter-spacing-2 { letter-spacing: 2px; }

.glass-card {
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 28px;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
}

.border-accent {
  border: 3px solid $secondary;
}

.opacity-10 { opacity: 0.1; }
</style>
