<template>
  <q-page class="q-pa-md">
    <div class="text-h5 q-mb-md">Mark Attendance</div>
    
    <q-card flat bordered class="q-mb-md">
      <q-card-section>
        <div class="text-subtitle1">Elite Juniors - 10:00 AM Today</div>
      </q-card-section>
      
      <q-list separator>
        <q-item v-for="player in players" :key="player.id">
          <q-item-section>
            <q-item-label>{{ player.name }}</q-item-label>
          </q-item-section>
          
          <q-item-section side>
            <q-btn-toggle
              v-model="player.status"
              toggle-color="primary"
              flat
              dense
              :options="[
                {label: 'P', value: 'present'},
                {label: 'A', value: 'absent'},
                {label: 'L', value: 'late'}
              ]"
            />
          </q-item-section>
        </q-item>
      </q-list>
      
      <q-card-actions align="right">
        <q-btn color="primary" label="Save Attendance" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const players = ref([
  { id: 1, name: 'Adam Smith', status: 'present' },
  { id: 2, name: 'Sarah Jones', status: 'present' },
  { id: 3, name: 'Mike Brown', status: 'absent' }
]);
</script>
