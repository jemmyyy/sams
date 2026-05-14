<template>
  <q-page class="q-pa-lg">
    <div class="row items-center q-mb-xl">
      <div class="col">
        <h4 class="text-weight-black no-margin text-primary uppercase letter-spacing-1">
          MARK <span class="text-secondary">ATTENDANCE</span>
        </h4>
        <div class="text-grey-7 text-subtitle1">Verify player presence for the active session</div>
      </div>
    </div>

    <q-card flat bordered class="sport-card overflow-hidden bg-white">
      <div class="bg-secondary text-white q-pa-lg">
        <div class="row items-center justify-between">
          <div>
            <div class="text-h5 text-weight-black uppercase">Elite Juniors</div>
            <div class="text-subtitle2 opacity-80">May 13, 2026 • 10:00 AM</div>
          </div>
          <q-btn unelevated color="white" text-color="secondary" label="SELECT ALL" class="text-weight-bold" />
        </div>
      </div>
      
      <q-list separator>
        <q-item v-for="player in players" :key="player.id" class="q-py-md">
          <q-item-section avatar>
            <q-avatar size="48px">
              <img :src="`https://i.pravatar.cc/150?u=${player.id}`">
            </q-avatar>
          </q-item-section>
          
          <q-item-section>
            <q-item-label class="text-weight-bold text-h6">{{ player.name }}</q-item-label>
            <q-item-label caption>Standard Membership</q-item-label>
          </q-item-section>
          
          <q-item-section side>
            <q-btn-toggle
              v-model="player.status"
              toggle-color="primary"
              color="grey-2"
              text-color="grey-7"
              unelevated
              rounded
              class="attendance-toggle"
              :options="[
                {label: 'PRESENT', value: 'present'},
                {label: 'ABSENT', value: 'absent'},
                {label: 'LATE', value: 'late'}
              ]"
            />
          </q-item-section>
        </q-item>
      </q-list>
      
      <q-card-actions class="q-pa-lg bg-grey-1">
        <q-space />
        <q-btn flat color="grey-6" label="Discard" class="q-mr-md" />
        <q-btn color="primary" label="Finalize Roster" size="lg" class="q-px-xl text-weight-bold shadow-5" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const players = ref([
  { id: 1, name: 'Adam Smith', status: 'present' },
  { id: 2, name: 'Sarah Jones', status: 'present' },
  { id: 3, name: 'Mike Brown', status: 'absent' },
  { id: 4, name: 'Emma Wilson', status: 'late' }
]);
</script>

<style lang="scss" scoped>
.letter-spacing-1 { letter-spacing: 1px; }

.sport-card {
  border-radius: 30px;
}

.attendance-toggle {
  border-radius: 50px;
  overflow: hidden;
}

.opacity-80 { opacity: 0.8; }
</style>
