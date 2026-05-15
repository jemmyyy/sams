<template>
  <q-page class="q-pa-lg">
    <div class="row items-center q-mb-xl">
      <div class="col">
        <div class="text-mono text-min text-grey-5 letter-spacing-2 uppercase q-mb-sm">Session Tracking</div>
        <h4 class="text-apex heading-md no-margin text-white">
          MARK <span class="text-energy-volt">ATTENDANCE</span>
        </h4>
        <div class="text-grey-5 text-mono text-min uppercase q-mt-sm">Verify player presence for the active session</div>
      </div>
    </div>

    <q-card flat class="elite-card overflow-hidden">
      <div class="bg-sams-obsidian q-pa-lg" style="border-bottom: 1px solid var(--sams-border);">
        <div class="row items-center justify-between">
          <div>
            <div class="text-h5 text-weight-black text-white text-apex uppercase">Elite Juniors</div>
            <div class="text-mono text-min text-grey-5 uppercase">May 13, 2026 • 10:00 AM</div>
          </div>
          <q-btn unelevated class="btn-victory text-mono" label="SELECT ALL" />
        </div>
      </div>

      <q-list dark separator>
        <q-item v-for="player in players" :key="player.id" class="q-py-md">
          <q-item-section avatar>
            <q-avatar size="48px">
              <img :src="`https://i.pravatar.cc/150?u=${player.id}`">
            </q-avatar>
          </q-item-section>

          <q-item-section>
            <q-item-label class="text-weight-bold text-white">{{ player.name }}</q-item-label>
            <q-item-label caption class="text-grey-5">Standard Membership</q-item-label>
          </q-item-section>

          <q-item-section side>
            <q-btn-toggle
              v-model="player.status"
              toggle-color="primary"
              color="grey-8"
              text-color="white"
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

      <q-card-actions class="q-pa-lg" style="background: rgba(0,0,0,0.2);">
        <q-space />
        <q-btn flat class="text-grey-5" label="Discard" />
        <q-btn unelevated class="btn-victory text-mono" label="Finalize Roster" size="lg" />
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
.letter-spacing-2 { letter-spacing: 2px; }

.elite-card {
  border-radius: var(--sams-radius-lg);
  border: 1px solid var(--sams-border);
  background: var(--sams-obsidian);
}

.attendance-toggle {
  border-radius: 50px;
  overflow: hidden;
}
</style>
