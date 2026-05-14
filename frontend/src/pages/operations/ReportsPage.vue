<template>
  <q-page class="q-pa-lg">
    <div class="row items-center q-mb-xl">
      <div class="col">
        <h1 class="text-h4 text-weight-bold q-my-none">Reports & Exports</h1>
        <p class="text-grey-7 q-mt-sm">Generate and manage data exports</p>
      </div>
      <div class="col-auto">
        <q-btn color="dark" icon="add" label="New Report" @click="showDialog = true" rounded />
      </div>
    </div>

    <div class="row q-col-gutter-lg">
      <div class="col-12 col-md-8">
        <q-card flat bordered class="report-list-card">
          <q-table
            flat
            :rows="reports"
            :columns="columns"
            row-key="id"
            class="bg-transparent"
          >
            <template v-slot:body-cell-status="props">
              <q-td :props="props">
                <q-badge :color="statusColor(props.value)" rounded class="q-px-sm q-py-xs">
                  {{ props.value.toUpperCase() }}
                </q-badge>
              </q-td>
            </template>
            <template v-slot:body-cell-actions="props">
              <q-td :props="props" class="q-gutter-sm">
                <q-btn flat round dense icon="download" color="primary" v-if="props.row.status === 'completed'" />
                <q-btn flat round dense icon="refresh" color="grey" v-if="props.row.status === 'failed'" />
                <q-btn flat round dense icon="delete" color="negative" />
              </q-td>
            </template>
          </q-table>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card flat bordered class="schedule-card bg-dark text-white">
          <q-card-section>
            <div class="text-h6 text-weight-bold">Scheduled Reports</div>
            <div class="text-caption text-grey-5 q-mb-md">Automated periodic exports</div>
            
            <q-list dark separator>
              <q-item v-for="sched in schedules" :key="sched.id" class="q-px-none">
                <q-item-section>
                  <q-item-label class="text-weight-bold">{{ sched.name }}</q-item-label>
                  <q-item-label caption class="text-grey-4">{{ sched.frequency }} • {{ sched.format.toUpperCase() }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-toggle v-model="sched.active" color="info" />
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Request Dialog -->
    <q-dialog v-model="showDialog">
      <q-card style="min-width: 400px; border-radius: 16px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6 text-weight-bold">Request Report</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section class="q-gutter-md">
          <q-select v-model="form.type" :options="reportTypes" label="Report Type" filled />
          <q-select v-model="form.format" :options="['PDF', 'Excel', 'CSV']" label="Format" filled />
          <div class="row q-col-gutter-sm">
            <div class="col-6">
              <q-input v-model="form.start" label="Start Date" filled type="date" stack-label />
            </div>
            <div class="col-6">
              <q-input v-model="form.end" label="End Date" filled type="date" stack-label />
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right" class="q-pa-md">
          <q-btn flat label="Cancel" v-close-popup />
          <q-btn color="dark" label="Generate" rounded class="q-px-lg" @click="requestReport" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const showDialog = ref(false);
const form = ref({ type: 'Financial Report', format: 'PDF', start: '', end: '' });

const reportTypes = ['Financial Report', 'Attendance Report', 'Utilization Report', 'Coach Performance'];

const statusColor = (status: string) => {
  switch (status) {
    case 'completed': return 'positive';
    case 'processing': return 'info';
    case 'failed': return 'negative';
    default: return 'grey';
  }
};

const columns = [
  { name: 'date', label: 'DATE', field: 'date', align: 'left', sortable: true },
  { name: 'type', label: 'REPORT TYPE', field: 'type', align: 'left' },
  { name: 'format', label: 'FORMAT', field: 'format', align: 'center' },
  { name: 'status', label: 'STATUS', field: 'status', align: 'center' },
  { name: 'actions', label: '', field: 'actions', align: 'right' },
];

const reports = ref([
  { id: 1, date: '2026-05-15 09:30', type: 'Financial Report', format: 'pdf', status: 'completed' },
  { id: 2, date: '2026-05-14 18:20', type: 'Attendance Report', format: 'csv', status: 'completed' },
  { id: 3, date: '2026-05-15 10:45', type: 'Utilization Report', format: 'xlsx', status: 'processing' },
  { id: 4, date: '2026-05-10 14:00', type: 'Performance Report', format: 'pdf', status: 'failed' },
]);

const schedules = ref([
  { id: 1, name: 'Weekly Financial Summary', frequency: 'Weekly', format: 'pdf', active: true },
  { id: 2, name: 'Daily Attendance Log', frequency: 'Daily', format: 'csv', active: true },
  { id: 3, name: 'Monthly Performance Audit', frequency: 'Monthly', format: 'xlsx', active: false },
]);

function requestReport() {
  showDialog.value = false;
  // logic to call API
}
</script>

<style lang="scss" scoped>
.report-list-card, .schedule-card {
  border-radius: 20px;
}
</style>
