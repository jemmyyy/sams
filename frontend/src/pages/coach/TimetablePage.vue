<template>
  <q-page class="q-pa-lg">
    <div class="row items-center q-mb-xl">
      <div class="col">
        <h4 class="text-weight-black no-margin text-secondary uppercase letter-spacing-1">
          COMMAND <span class="text-primary">CENTER</span>
        </h4>
        <div class="text-grey-7 text-subtitle1">Manage your professional training schedule</div>
      </div>
    </div>

    <div class="row q-col-gutter-lg">
      <div class="col-12">
        <q-list bordered separator class="bg-white sport-card overflow-hidden">
          <div class="bg-primary text-white q-pa-md text-weight-bold uppercase letter-spacing-2">
            Today's Assignments
          </div>
          <q-item v-for="session in sessions" :key="session.id" clickable @click="viewSession(session)" class="q-py-lg">
            <q-item-section avatar>
              <q-avatar color="secondary" text-white icon="sports_tennis" size="56px" class="shadow-2" />
            </q-item-section>
            
            <q-item-section>
              <q-item-label class="text-h6 text-weight-black text-primary">{{ session.title }}</q-item-label>
              <q-item-label caption class="text-grey-7">
                <q-icon name="schedule" class="q-mr-xs" />{{ new Date(session.start_datetime).toLocaleTimeString() }} • <q-icon name="place" class="q-mr-xs" />{{ session.venue_name }}
              </q-item-label>
            </q-item-section>
            
            <q-item-section side>
              <div class="row q-gutter-x-sm">
                <q-btn flat round color="primary" icon="how_to_reg" @click.stop="$router.push('/coach/attendance')" />
                <q-btn flat round color="secondary" icon="assignment" @click.stop="$router.push('/coach/reports')" />
                <q-btn flat round color="accent" icon="chevron_right" />
              </div>
            </q-item-section>
          </q-item>
        </q-list>
      </div>
    </div>
    
    <q-page-sticky position="bottom-right" :offset="[24, 24]">
      <q-btn fab icon="add" color="secondary" class="shadow-10" />
    </q-page-sticky>
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
  venue: number;
  series: number;
}

const sessions = ref<any[]>([]);

onMounted(async () => {
  try {
    const response = await api.get('sessions/occurrences/');
    // Standardized response format: response.data.data
    sessions.value = response.data.data.results || response.data.data;
  } catch (error) {
    console.error('Failed to fetch sessions:', error);
  }
});

function viewSession(session: any) {
  console.log('Viewing session', session);
}
</script>

<style lang="scss" scoped>
.letter-spacing-1 { letter-spacing: 1px; }
.letter-spacing-2 { letter-spacing: 2px; }

.sport-card {
  border-radius: 24px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  border: 1px solid rgba(0,0,0,0.05);
}
</style>
