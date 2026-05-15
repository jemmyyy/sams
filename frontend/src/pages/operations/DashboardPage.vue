<template>
  <q-page class="q-pa-xl">
    <!-- Header with Stats Summary -->
    <div class="row items-end justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-apex heading-lg text-navy no-margin">Command Center</h1>
        <div class="text-subtitle1 text-grey-6">Operational intelligence for the current cycle.</div>
      </div>
      <div class="row q-gutter-sm">
         <q-btn flat unelevated class="apex-btn-primary" label="Analytics HQ" icon="insights" to="/operations/analytics" />
         <q-btn unelevated class="apex-btn-victory" label="Quick Dispatch" icon="bolt" />
      </div>
    </div>

    <!-- Clean Metric Grid -->
    <div class="row q-col-gutter-lg q-mb-xl">
      <div class="col-12 col-md-3" v-for="stat in quickStats" :key="stat.label">
        <div class="apex-card q-pa-lg">
          <div class="row items-center justify-between q-mb-md">
            <div class="stat-icon-bg" :style="{ background: stat.bg }">
               <q-icon :name="stat.icon" size="24px" :color="stat.color" />
            </div>
            <q-badge rounded :color="stat.trend > 0 ? 'green-1' : 'red-1'" :text-color="stat.trend > 0 ? 'green-9' : 'red-9'" class="q-px-sm q-py-xs">
              {{ stat.trend > 0 ? '+' : '' }}{{ stat.trend }}%
            </q-badge>
          </div>
          <div class="text-h4 text-apex text-navy q-mb-xs">{{ stat.value }}</div>
          <div class="text-caption text-grey-6 uppercase font-weight-bold letter-spacing-1">{{ stat.label }}</div>
        </div>
      </div>
    </div>

    <div class="row q-col-gutter-lg">
      <!-- Data Visualization Table -->
      <div class="col-12 col-md-8">
        <div class="apex-card overflow-hidden">
          <div class="q-pa-lg border-bottom row items-center justify-between">
             <div class="text-apex text-h6 text-navy">Recent Academy Events</div>
             <q-btn flat dense round icon="more_horiz" color="grey-6" />
          </div>
          <q-table
            flat
            :rows="recentEvents"
            :columns="eventColumns"
            row-key="id"
            class="apex-table"
          >
            <template v-slot:body-cell-status="props">
              <q-td :props="props">
                <q-badge rounded :color="props.value === 'Completed' ? 'green-1' : 'orange-1'" :text-color="props.value === 'Completed' ? 'green-9' : 'orange-9'" class="q-px-md">
                  {{ props.value }}
                </q-badge>
              </q-td>
            </template>
          </q-table>
        </div>
      </div>

      <!-- Quick Actions / Alerts -->
      <div class="col-12 col-md-4">
        <div class="apex-card q-pa-lg">
          <div class="text-apex text-h6 text-navy q-mb-lg">System Alerts</div>
          <q-list padding separator class="q-px-none">
            <q-item v-for="alert in alerts" :key="alert.id" class="q-px-none q-mb-sm">
              <q-item-section avatar>
                <q-avatar :color="alert.type === 'error' ? 'red-1' : 'blue-1'" :text-color="alert.type === 'error' ? 'red-9' : 'blue-9'" icon="priority_high" size="40px" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold text-navy">{{ alert.title }}</q-item-label>
                <q-item-label caption>{{ alert.time }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-btn flat round dense icon="chevron_right" color="grey-5" />
              </q-item-section>
            </q-item>
          </q-list>
          <q-btn unelevated color="blue-1" text-color="blue-9" class="full-width q-mt-md text-weight-bold" label="View All Activity" no-caps />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
const quickStats = [
  { label: 'Net Revenue', value: '142.8K', icon: 'payments', color: 'blue-9', bg: '#eff6ff', trend: 12.4 },
  { label: 'Active Athletes', value: '384', icon: 'groups', color: 'green-9', bg: '#f0fdf4', trend: 4.2 },
  { label: 'Avg Attendance', value: '94%', icon: 'fact_check', color: 'orange-9', bg: '#fff7ed', trend: 0.8 },
  { label: 'Staff Deployed', value: '24', icon: 'badge', color: 'red-9', bg: '#fef2f2', trend: -1.2 },
];

const eventColumns = [
  { name: 'event', label: 'EVENT', field: 'event', align: 'left' as const, sortable: true },
  { name: 'user', label: 'USER', field: 'user', align: 'left' as const },
  { name: 'time', label: 'TIME', field: 'time', align: 'left' as const },
  { name: 'status', label: 'STATUS', field: 'status', align: 'center' as const },
];

const recentEvents = [
  { id: 1, event: 'Monthly Billing Batch', user: 'System', time: '10:30 AM', status: 'Completed' },
  { id: 2, event: 'New Player Registration', user: 'Ops_Admin', time: '09:15 AM', status: 'Completed' },
  { id: 3, event: 'Venue Maintenance Alert', user: 'Coach_A', time: '08:45 AM', status: 'Pending' },
  { id: 4, event: 'Report Export Requested', user: 'Ops_01', time: '07:20 AM', status: 'Completed' },
];

const alerts = [
  { id: 1, title: 'Outstanding Invoice #1022', time: '2 hours ago', type: 'error' },
  { id: 2, title: 'New Coach Application', time: '4 hours ago', type: 'info' },
  { id: 3, title: 'System Backup Completed', time: '1 day ago', type: 'info' },
];
</script>

<style lang="scss" scoped>
.text-navy { color: var(--sams-navy); }
.text-victory { color: var(--sams-victory-red); }
.border-bottom { border-bottom: 1px solid var(--sams-border); }

.stat-icon-bg {
  width: 48px; height: 48px;
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
}

.apex-table {
  :deep(.q-table__card) { box-shadow: none; border-radius: 0; }
  :deep(thead tr) { height: 64px; background: #f8fafc; }
  :deep(thead th) { color: #64748b; font-weight: 700; letter-spacing: 1px; }
  :deep(tbody tr) { height: 60px; &:hover { background: #fdfdfd; } }
}
</style>
