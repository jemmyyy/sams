<template>
  <q-page class="q-pa-lg">
    <div class="row items-center q-mb-xl">
      <div class="col">
        <h4 class="text-weight-black no-margin text-primary uppercase letter-spacing-1">
          TRAINING <span class="text-secondary">TIMETABLE</span>
        </h4>
        <div class="text-grey-7 text-subtitle1">Track your upcoming championship sessions</div>
      </div>
      <div class="col-auto">
        <q-btn-toggle
          v-model="viewMode"
          no-caps
          rounded
          unelevated
          toggle-color="primary"
          color="white"
          text-color="primary"
          class="shadow-1"
          :options="[
            {label: 'WEEK', value: 'week'},
            {label: 'MONTH', value: 'month'}
          ]"
        />
      </div>
    </div>

    <div class="row q-col-gutter-lg">
      <div class="col-12 col-md-8">
        <q-card flat bordered class="sport-card bg-white">
          <q-card-section class="q-pa-none">
            <!-- Dynamic Calendar Header -->
            <div class="row items-center q-pa-md bg-grey-1">
              <q-btn flat round icon="chevron_left" />
              <q-space />
              <div class="text-h6 text-weight-bold">MAY 13 - 19, 2026</div>
              <q-space />
              <q-btn flat round icon="chevron_right" />
            </div>
            
            <!-- Styled Grid Placeholder -->
            <div class="calendar-grid q-pa-md">
              <div class="row no-wrap q-gutter-x-sm overflow-auto">
                <div v-for="day in ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']" :key="day" class="col-grow">
                   <q-card flat bordered class="day-col text-center q-py-sm">
                      <div class="text-caption text-grey-6">{{ day }}</div>
                      <div class="text-h6 text-weight-black">13</div>
                      
                      <!-- Session Card -->
                      <div v-if="day === 'MON'" class="session-pill q-mt-md q-mx-xs q-pa-xs bg-primary-10 text-primary cursor-pointer">
                        <div class="text-bold">TENNIS</div>
                        <div style="font-size: 10px">10:00 AM</div>
                      </div>
                   </q-card>
                </div>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card flat bordered class="sport-card bg-white overflow-hidden">
          <div class="bg-secondary text-white q-pa-md text-weight-bold uppercase letter-spacing-1">
            Upcoming Action
          </div>
          <q-list separator>
            <q-item v-for="session in sessions" :key="session.id" class="q-py-md">
              <q-item-section avatar>
                <div class="date-badge bg-primary text-white text-center q-pa-xs">
                  <div class="text-caption">{{ new Date(session.start_datetime).toLocaleDateString('en-US', { month: 'short' }).toUpperCase() }}</div>
                  <div class="text-h6 text-weight-black">{{ new Date(session.start_datetime).getDate() }}</div>
                </div>
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold text-primary">{{ session.title }}</q-item-label>
                <q-item-label caption>
                  <q-icon name="schedule" /> {{ new Date(session.start_datetime).toLocaleTimeString() }} • <q-icon name="place" /> {{ session.venue_name }}
                </q-item-label>
              </q-item-section>
              <q-item-section side>
                 <q-chip size="sm" color="positive" text-color="white" class="text-weight-bold">LIVE</q-chip>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../../api';

interface Session {
  id: number;
  start_datetime: string;
  end_datetime: string;
  status: string;
  title: string;
  venue_name: string;
}

const viewMode = ref('week');
const sessions = ref<Session[]>([]);

onMounted(async () => {
  try {
    const response = await api.get('sessions/occurrences/');
    // Standardized response format: response.data.data
    sessions.value = response.data.data.results || response.data.data;
  } catch (error) {
    console.error('Failed to fetch sessions:', error);
  }
});
</script>

<style lang="scss" scoped>
.letter-spacing-1 { letter-spacing: 1px; }

.sport-card {
  border-radius: 20px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.03);
  border: 1px solid rgba(0,0,0,0.05);
}

.day-col {
  border-radius: 12px;
  min-width: 80px;
}

.date-badge {
  border-radius: 10px;
  width: 50px;
}

.bg-primary-10 {
  background: rgba($primary, 0.08);
}

.session-pill {
  border-radius: 8px;
  border-left: 4px solid $primary;
  transition: all 0.2s ease;
  &:hover {
    background: rgba($primary, 0.15);
    transform: scale(1.05);
  }
}
</style>
