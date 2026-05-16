<template>
  <q-page class="q-pa-xl animate-up">
    <!-- Header -->
    <div class="row items-center q-mb-xl justify-between">
      <div class="col">
        <h1 class="text-heading heading-lg no-margin text-white">Mark Attendance</h1>
        <div class="text-subtitle1 text-grey-5">Verify player presence for the active session</div>
      </div>
      <q-btn unelevated color="primary" class="sams-btn" label="Load Active Session" @click="loadSession" icon="refresh" />
    </div>

    <q-card flat class="sams-card overflow-hidden">
      <div class="bg-surface-2 q-pa-lg border-b">
        <div class="row items-center justify-between">
          <div>
            <div class="text-h5 text-weight-black text-white uppercase">Elite Juniors</div>
            <div class="text-mono text-min text-grey-5 uppercase">May 13, 2026 • 10:00 AM</div>
          </div>
          <q-btn unelevated color="primary" outline class="text-weight-bold" label="SELECT ALL PRESENT" @click="markAllPresent" />
        </div>
      </div>

      <q-list dark separator class="bg-surface-1">
        <div v-if="attendanceStore.loading" class="q-pa-xl text-center">
          <q-spinner color="primary" size="3em" />
        </div>
        <q-item v-else v-for="record in attendanceRecords" :key="record.player" class="q-py-md">
          <q-item-section avatar>
            <q-avatar size="48px" class="border-2 shadow-sm">
              <img :src="`https://ui-avatars.com/api/?name=Player+${record.player}&background=random`">
            </q-avatar>
          </q-item-section>

          <q-item-section>
            <q-item-label class="text-weight-bold text-white">{{ record.player_name || `Player #${record.player}` }}</q-item-label>
            <q-item-label caption class="text-grey-5">Standard Membership</q-item-label>
          </q-item-section>

          <q-item-section side>
            <q-btn-toggle
              v-model="record.status"
              toggle-color="primary"
              color="surface-2"
              text-color="white"
              unelevated
              rounded
              class="attendance-toggle"
              :options="[
                {label: 'PRESENT', value: 'Present'},
                {label: 'ABSENT', value: 'Absent'},
                {label: 'LATE', value: 'Late'}
              ]"
            />
          </q-item-section>
        </q-item>
        <div v-if="!attendanceStore.loading && attendanceRecords.length === 0" class="q-pa-xl text-center text-grey-5">
          No players found for this session.
        </div>
      </q-list>

      <q-card-actions class="q-pa-lg bg-surface-2 border-t">
        <q-space />
        <q-btn flat color="grey-5" label="Discard" />
        <q-btn unelevated color="primary" class="sams-btn text-weight-bold" label="Finalize Roster" size="lg" @click="finalizeAttendance" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAttendanceStore, AttendanceRecord } from '../../stores/attendance';
import { useQuasar } from 'quasar';

const $q = useQuasar();
const attendanceStore = useAttendanceStore();
const activeSessionId = ref('');

// Local state to manage toggles before saving
const attendanceRecords = ref<Partial<AttendanceRecord>[]>([]);
const sessions = ref<any[]>([]);

async function loadSession() {
  await attendanceStore.fetchAttendance({ session: activeSessionId.value || undefined });
  attendanceRecords.value = [...attendanceStore.records];
}

onMounted(async () => {
  try {
    const { useApi } = await import('../../composables/useApi')
    const { get } = useApi()
    const data = await get<any[]>('sessions/occurrences/')
    sessions.value = Array.isArray(data) ? data : data?.results || []
  } catch {}
  loadSession();
});

function markAllPresent() {
  attendanceRecords.value.forEach(record => record.status = 'Present');
}

async function finalizeAttendance() {
  try {
    for (const record of attendanceRecords.value) {
      await attendanceStore.markAttendance(record);
    }
    $q.notify({ type: 'positive', message: 'Attendance finalized' });
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Error saving attendance' });
  }
}
</script>

<style lang="scss" scoped>
.letter-spacing-2 { letter-spacing: 2px; }

.bg-surface-1 { background-color: var(--sams-surface-1); }
.bg-surface-2 { background-color: var(--sams-surface-2); }
.border-b { border-bottom: 1px solid var(--sams-border); }
.border-t { border-top: 1px solid var(--sams-border); }
.border-2 { border: 2px solid var(--sams-border); }

.attendance-toggle {
  border-radius: 50px;
  overflow: hidden;
  border: 1px solid var(--sams-border);
}
</style>
