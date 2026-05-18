<template>
  <q-page class="q-pa-xl animate-up">
    <div class="row items-center justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin text-white">Intelligence Exports</h1>
        <div class="text-subtitle1 text-grey-5">Generate and manage academy data reports.</div>
      </div>
      <q-btn unelevated class="sams-btn sams-btn-action" label="Request Report" icon="add" outline color="primary" @click="showDialog = true" />
    </div>

    <div class="row q-col-gutter-lg">
      <div class="col-12 col-md-8">
        <q-card flat bordered class="sams-card">
           <div class="q-pa-lg border-bottom bg-surface-2">
              <div class="text-heading text-subtitle1 text-white">Recent Generations</div>
           </div>
           <q-table
             flat
             :rows="reports"
             :columns="reportColumns"
             row-key="id"
             class="sams-table"
             dark
           >
             <template v-slot:body-cell-status="props">
               <q-td :props="props">
                 <q-badge rounded :color="props.value === 'Ready' ? 'success' : 'primary'" text-color="white" class="q-px-md">
                   {{ props.value }}
                 </q-badge>
               </q-td>
             </template>
             <template v-slot:body-cell-actions="props">
               <q-td :props="props">
                 <q-btn flat round dense icon="download" color="primary" />
                 <q-btn flat round dense icon="delete_outline" color="grey-6" />
               </q-td>
             </template>
           </q-table>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card flat bordered class="sams-card q-pa-lg bg-surface-1 text-white">
           <div class="text-heading text-h6 q-mb-md">Automated Schedules</div>
           <div class="text-caption text-grey-5 q-mb-xl">Recurring intelligence delivery</div>
           
           <q-list dark separator class="q-px-none">
              <q-item v-for="s in [1, 2]" :key="s" class="q-px-none q-py-md">
                 <q-item-section>
                    <q-item-label class="text-weight-bold">Weekly Financial Pulse</q-item-label>
                    <q-item-label caption class="text-grey-5">Every Monday // PDF</q-item-label>
                 </q-item-section>
                 <q-item-section side>
                    <q-toggle v-model="toggle" color="primary" />
                 </q-item-section>
              </q-item>
           </q-list>
        </q-card>
      </div>
    </div>
    <!-- Request Report Dialog -->
    <q-dialog v-model="showDialog" persistent>
      <q-card class="sams-card q-pa-lg" style="min-width: 480px">
        <div class="text-heading text-h6 q-mb-lg text-white">Request New Report</div>
        <q-form @submit="submitReport">
          <q-select
            v-model="reportForm.type"
            :options="reportTypes"
            label="Report Type"
            outlined
            dark
            class="q-mb-md"
            bg-color="surface-2"
          />
          <q-select
            v-model="reportForm.format"
            :options="['csv', 'xlsx', 'pdf']"
            label="Format"
            outlined
            dark
            class="q-mb-md"
            bg-color="surface-2"
          />
          <q-input
            v-model="reportForm.start_date"
            label="Start Date"
            type="date"
            outlined
            dark
            class="q-mb-md"
            bg-color="surface-2"
          />
          <q-input
            v-model="reportForm.end_date"
            label="End Date"
            type="date"
            outlined
            dark
            class="q-mb-lg"
            bg-color="surface-2"
          />
          <div class="row justify-end q-gutter-md">
            <q-btn flat label="Cancel" color="grey-6" v-close-popup />
            <q-btn unelevated type="submit" label="Generate" color="primary" :loading="submitting" />
          </div>
        </q-form>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../../api';

const toggle = ref(true);
const showDialog = ref(false);
const submitting = ref(false);

const reportTypes = [
  { label: 'Financial', value: 'financial' },
  { label: 'Attendance', value: 'attendance' },
  { label: 'Utilization', value: 'utilization' },
  { label: 'Performance', value: 'performance' },
];

const reportForm = ref({
  type: { label: 'Financial', value: 'financial' },
  format: 'csv',
  start_date: '',
  end_date: '',
});

const reportColumns = [
  { name: 'created_at', label: 'DATE', field: (row: any) => row.created_at ? new Date(row.created_at).toLocaleDateString() : '', align: 'left' as const },
  { name: 'report_type', label: 'TYPE', field: 'report_type', align: 'left' as const },
  { name: 'status', label: 'STATUS', field: 'status', align: 'center' as const },
  { name: 'actions', label: '', field: 'actions', align: 'right' as const },
];

const reports = ref<any[]>([]);

async function fetchReports() {
  try {
    const response = await api.get('reports/exports/');
    reports.value = response.data.results || response.data;
  } catch (err) {
    console.error('Failed to fetch reports');
  }
}

async function submitReport() {
  submitting.value = true;
  try {
    await api.post('reports/exports/', {
      report_type: reportForm.value.type.value,
      format: reportForm.value.format,
      parameters: {
        start_date: reportForm.value.start_date || undefined,
        end_date: reportForm.value.end_date || undefined,
      },
    });
    showDialog.value = false;
    await fetchReports();
  } catch (err) {
    console.error('Failed to create report');
  } finally {
    submitting.value = false;
  }
}

onMounted(() => {
  fetchReports();
});
</script>

<style lang="scss" scoped>
.bg-surface-1 { background-color: var(--sams-surface-1); }
.bg-surface-2 { background-color: var(--sams-surface-2); }
.border-bottom { border-bottom: 1px solid var(--sams-border); }

.sams-table {
  background-color: var(--sams-surface-1);
  :deep(.q-table__card) { box-shadow: none; background: transparent; }
  :deep(thead tr) { background: var(--sams-surface-2); }
  :deep(thead th) { color: var(--sams-text-secondary); font-weight: 700; height: 56px; border-bottom: 1px solid var(--sams-border); }
  :deep(tbody tr) { height: 60px; &:hover { background: rgba(255, 255, 255, 0.02); } }
  :deep(tbody td) { border-bottom: 1px solid var(--sams-border); color: var(--sams-text-primary); }
}
</style>
