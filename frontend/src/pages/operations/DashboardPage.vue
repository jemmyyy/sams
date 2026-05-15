<template>
  <q-page class="q-pa-xl animate-up">
    <!-- Header Summary -->
    <div class="row items-end justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin">Command Center</h1>
        <div class="text-subtitle1 text-grey-6">Real-time academy pulse and operational metrics.</div>
      </div>
      <div class="row q-gutter-md">
         <q-btn unelevated class="sams-btn sams-btn-primary" label="New Enrollment" icon="person_add" />
         <q-btn unelevated class="sams-btn sams-btn-action" label="System Export" icon="file_download" />
      </div>
    </div>

    <!-- Metric Grid (High Visibility) -->
    <div class="row q-col-gutter-lg q-mb-xl">
      <div class="col-12 col-md-3" v-for="stat in quickStats" :key="stat.label">
        <q-card flat bordered class="sams-card q-pa-lg">
          <div class="row items-center justify-between q-mb-md">
            <div class="stat-icon row items-center justify-center" :style="{ background: stat.bg }">
               <q-icon :name="stat.icon" size="24px" :color="stat.color" />
            </div>
            <div :class="`text-weight-bold ${stat.trend > 0 ? 'text-positive' : 'text-negative'}`">
              {{ stat.trend > 0 ? '+' : '' }}{{ stat.trend }}%
            </div>
          </div>
          <div class="text-h4 text-heading text-navy q-mb-xs">{{ stat.value }}</div>
          <div class="text-caption text-grey-6 uppercase text-weight-bold letter-spacing-1">{{ stat.label }}</div>
        </q-card>
      </div>
    </div>

    <div class="row q-col-gutter-lg">
      <!-- Main Content Area -->
      <div class="col-12 col-md-8">
        <q-card flat bordered class="sams-card">
          <div class="q-pa-lg border-bottom row items-center justify-between bg-slate-50">
             <div class="text-heading text-subtitle1">Active Training Sessions</div>
             <q-btn flat dense round icon="more_horiz" color="grey-6" />
          </div>
          
          <q-table
            flat
            :rows="activeSessions"
            :columns="sessionColumns"
            row-key="id"
            class="sams-table"
          >
            <template v-slot:body-cell-status="props">
              <q-td :props="props">
                <q-badge rounded :color="props.value === 'Live' ? 'red' : 'green'" class="q-px-md q-py-xs">
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
          <div class="text-heading text-subtitle1 q-mb-lg">Priority Notifications</div>
          <q-list padding separator class="q-px-none">
            <q-item v-for="alert in alerts" :key="alert.id" class="q-px-none q-mb-sm">
              <q-item-section avatar>
                <q-avatar :color="alert.type === 'error' ? 'red-1' : 'blue-1'" :text-color="alert.type === 'error' ? 'red' : 'blue'" icon="info_outline" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold">{{ alert.title }}</q-item-label>
                <q-item-label caption>{{ alert.time }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-btn flat round dense icon="chevron_right" color="grey-4" />
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
const quickStats = [
  { label: 'Revenue (MTD)', value: '142.8K', icon: 'payments', color: 'blue-8', bg: '#eff6ff', trend: 12.4 },
  { label: 'Active Roster', value: '384', icon: 'people', color: 'green-8', bg: '#f0fdf4', trend: 4.2 },
  { label: 'Avg Attendance', value: '94%', icon: 'fact_check', color: 'orange-8', bg: '#fff7ed', trend: 0.8 },
  { label: 'Coach Units', value: '24', icon: 'badge', color: 'red-8', bg: '#fef2f2', trend: -1.2 },
];

const sessionColumns = [
  { name: 'group', label: 'GROUP', field: 'group', align: 'left' as const, sortable: true },
  { name: 'coach', label: 'COACH', field: 'coach', align: 'left' as const },
  { name: 'venue', label: 'VENUE', field: 'venue', align: 'left' as const },
  { name: 'status', label: 'STATUS', field: 'status', align: 'center' as const },
];

const activeSessions = [
  { id: 1, group: 'Football Tactical U16', coach: 'Ahmed Salah', venue: 'Pitch 01', status: 'Live' },
  { id: 2, group: 'Elite Strikers B2', coach: 'Omar Hassan', venue: 'Indoor Hall', status: 'Upcoming' },
  { id: 3, group: 'Junior Foundations', coach: 'Mohamed Ali', venue: 'Pitch 02', status: 'Live' },
];

const alerts = [
  { id: 1, title: 'Incomplete Attendance: U14', time: '10m ago', type: 'error' },
  { id: 2, title: 'New Registration: Youssef A.', time: '1h ago', type: 'info' },
  { id: 3, title: 'Report Export Ready', time: '2h ago', type: 'info' },
];
</script>

<style lang="scss" scoped>
.bg-slate-50 { background-color: #f8fafc; }
.border-bottom { border-bottom: 1px solid var(--sams-border); }

.stat-icon {
  width: 44px; height: 44px;
  border-radius: 12px;
}

.sams-table {
  :deep(.q-table__card) { box-shadow: none; }
  :deep(thead tr) { background: #f8fafc; }
  :deep(thead th) { color: #64748b; font-weight: 700; height: 56px; }
  :deep(tbody tr) { height: 60px; &:hover { background: #fdfdfd; } }
}
</style>
