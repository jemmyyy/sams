<template>
  <q-page class="q-pa-md">
    <div class="text-h5 q-mb-md">My Training Schedule</div>
    
    <q-list bordered separator class="bg-white">
      <q-item v-for="session in sessions" :key="session.id" clickable @click="viewSession(session)">
        <q-item-section avatar>
          <q-avatar color="secondary" text-white icon="sports_tennis" />
        </q-item-section>
        
        <q-item-section>
          <q-item-label>{{ session.title }}</q-item-label>
          <q-item-label caption>{{ session.time }} - {{ session.venue }}</q-item-label>
        </q-item-section>
        
        <q-item-section side>
          <q-btn flat round icon="chevron_right" />
        </q-item-section>
      </q-item>
    </q-list>
    
    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn fab icon="add" color="secondary" />
    </q-page-sticky>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Session {
  id: number;
  title: string;
  time: string;
  venue: string;
}

const sessions = ref<Session[]>([
  { id: 1, title: 'Morning Drills', time: '08:00 AM', venue: 'Court 1' },
  { id: 2, title: 'Elite Juniors', time: '10:00 AM', venue: 'Main Arena' },
  { id: 3, title: 'Afternoon Group', time: '04:00 PM', venue: 'Court 3' }
]);

function viewSession(session: Session) {
  console.log('Viewing session', session);
}
</script>
