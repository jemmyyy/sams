<template>
  <q-page class="q-pa-xl animate-up">
    <!-- Header Summary -->
    <div class="row items-end justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin text-white">Command Center</h1>
        <div class="text-subtitle1 text-grey-5">Real-time academy pulse and operational metrics.</div>
      </div>
      <div class="row q-gutter-md">
         <q-btn unelevated class="sams-btn sams-btn-primary" label="New Enrollment" icon="person_add" />
         <q-btn unelevated class="sams-btn sams-btn-action" label="System Export" icon="file_download" outline color="primary" />
      </div>
    </div>

    <!-- Metric Grid (High Visibility) -->
    <div class="row q-col-gutter-lg q-mb-xl">
      <div class="col-12 col-md-3" v-for="stat in quickStats" :key="stat.label">
        <q-card flat bordered class="sams-card q-pa-lg">
          <div class="row items-center justify-between q-mb-md">
            <div class="stat-icon row items-center justify-center bg-surface-2 border-b">
               <q-icon :name="stat.icon" size="24px" :color="stat.color" />
            </div>
            <div :class="`text-weight-bold ${stat.trend > 0 ? 'text-positive' : 'text-negative'}`">
              {{ stat.trend > 0 ? '+' : '' }}{{ stat.trend }}%
            </div>
          </div>
          <div class="text-h4 text-heading text-white q-mb-xs">{{ stat.value }}</div>
          <div class="text-caption text-grey-5 uppercase text-weight-bold letter-spacing-1">{{ stat.label }}</div>
        </q-card>
      </div>
    </div>

    <div class="row q-col-gutter-lg">
      <!-- Main Content Area -->
      <div class="col-12 col-md-8">
        <q-card flat bordered class="sams-card">
          <div class="q-pa-lg border-bottom row items-center justify-between bg-surface-2">
             <div class="text-heading text-subtitle1 text-white">Active Training Sessions</div>
             <q-btn flat dense round icon="more_horiz" color="grey-6" />
          </div>
          
          <q-table
            flat
            :rows="sessionsStore.sessions"
            :columns="sessionColumns"
            row-key="id"
            class="sams-table"
            dark
          >
            <template v-slot:body-cell-series="props">
              <q-td :props="props">{{ props.row.series?.title || 'N/A' }}</q-td>
            </template>
            <template v-slot:body-cell-venue="props">
              <q-td :props="props">{{ props.row.venue?.name || 'N/A' }}</q-td>
            </template>
            <template v-slot:body-cell-status="props">
              <q-td :props="props">
                <q-badge rounded :color="props.value === 'live' ? 'victory-red' : 'success'" class="q-px-md q-py-xs">
                  {{ props.value }}
                </q-badge>
              </q-td>
            </template>
          </q-table>
        </q-card>
      </div>

      <!-- Side Alerts/Activity -->
      <div class="col-12 col-md-4">
        <q-card flat bordered class="sams-card q-pa-lg">
          <div class="text-heading text-subtitle1 q-mb-lg text-white">Priority Notifications</div>
          <q-list padding separator class="q-px-none" dark>
            <q-item v-for="alert in alerts" :key="alert.id" class="q-px-none q-mb-sm">
              <q-item-section avatar>
                <q-avatar :color="alert.type === 'error' ? 'victory-red' : 'primary'" text-color="white" icon="info_outline" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold text-white">{{ alert.title }}</q-item-label>
                <q-item-label caption class="text-grey-5">{{ alert.time }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-btn flat round dense icon="chevron_right" color="grey-6" />
              </q-item-section>
            </q-item>
          </q-list>
          <q-btn outline color="primary" class="full-width q-mt-md sams-btn" label="View All Activity" />
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useSessionsStore } from '../../stores/sessions';

const sessionsStore = useSessionsStore();

onMounted(() => {
  sessionsStore.fetchSessions();
});

const quickStats = [
  { label: 'Revenue (MTD)', value: '0', icon: 'payments', color: 'primary', trend: 0 },
  { label: 'Active Roster', value: '0', icon: 'people', color: 'success', trend: 0 },
  { label: 'Avg Attendance', value: '0%', icon: 'fact_check', color: 'warning', trend: 0 },
  { label: 'Coach Units', value: '0', icon: 'badge', color: 'victory-red', trend: 0 },
];

const sessionColumns = [
  { name: 'series', label: 'GROUP', field: (row: any) => row.series?.title || 'N/A', align: 'left' as const, sortable: true },
  { name: 'date', label: 'DATE', field: 'start_datetime', align: 'left' as const },
  { name: 'venue', label: 'VENUE', field: (row: any) => row.venue?.name || 'N/A', align: 'left' as const },
  { name: 'status', label: 'STATUS', field: 'status', align: 'center' as const },
];

const alerts = ref<any[]>([]); // Fetch from API
</script>

<script lang="ts">
export default {
  name: 'DashboardPage'
}
</script>

<style lang="scss" scoped>
.bg-surface-2 { background-color: var(--sams-surface-2); }
.border-bottom { border-bottom: 1px solid var(--sams-border); }
.border-b { border: 1px solid var(--sams-border); }

.stat-icon {
  width: 44px; height: 44px;
  border-radius: 12px;
}

.sams-table {
  background-color: var(--sams-surface-1);
  :deep(.q-table__card) { box-shadow: none; background: transparent; }
  :deep(thead tr) { background: var(--sams-surface-2); }
  :deep(thead th) { color: var(--sams-text-secondary); font-weight: 700; height: 56px; border-bottom: 1px solid var(--sams-border); }
  :deep(tbody tr) { height: 60px; &:hover { background: rgba(255, 255, 255, 0.02); } }
  :deep(tbody td) { border-bottom: 1px solid var(--sams-border); color: var(--sams-text-primary); }
}
</style>
