<template>
  <q-page class="q-pa-xl animate-up">
    <div class="row items-center justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin">Intelligence Exports</h1>
        <div class="text-subtitle1 text-grey-6">Generate and manage academy data reports.</div>
      </div>
      <q-btn unelevated class="sams-btn sams-btn-action" label="Request Report" icon="add" />
    </div>

    <div class="row q-col-gutter-lg">
      <div class="col-12 col-md-8">
        <q-card flat bordered class="sams-card">
           <div class="q-pa-lg border-bottom bg-slate-50">
              <div class="text-heading text-subtitle1">Recent Generations</div>
           </div>
           <q-table
             flat
             :rows="reports"
             :columns="reportColumns"
             row-key="id"
             class="sams-table"
           >
             <template v-slot:body-cell-status="props">
               <q-td :props="props">
                 <q-badge rounded :color="props.value === 'Ready' ? 'green-1' : 'blue-1'" :text-color="props.value === 'Ready' ? 'green-9' : 'blue-9'" class="q-px-md">
                   {{ props.value }}
                 </q-badge>
               </q-td>
             </template>
             <template v-slot:body-cell-actions="props">
               <q-td :props="props">
                 <q-btn flat round dense icon="download" color="primary" />
                 <q-btn flat round dense icon="delete_outline" color="grey-4" />
               </q-td>
             </template>
           </q-table>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card flat bordered class="sams-card q-pa-lg bg-navy text-white">
           <div class="text-heading text-h6 q-mb-md">Automated Schedules</div>
           <div class="text-caption text-grey-4 q-mb-xl">Recurring intelligence delivery</div>
           
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
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
const toggle = ref(true);

const reportColumns = [
  { name: 'date', label: 'DATE', field: 'date', align: 'left' as const },
  { name: 'type', label: 'TYPE', field: 'type', align: 'left' as const },
  { name: 'status', label: 'STATUS', field: 'status', align: 'center' as const },
  { name: 'actions', label: '', field: 'actions', align: 'right' as const },
];

const reports = [
  { id: 1, date: 'May 15, 09:30', type: 'Financial Summary', status: 'Ready' },
  { id: 2, date: 'May 14, 18:00', type: 'Attendance Audit', status: 'Ready' },
  { id: 3, date: 'May 15, 11:00', type: 'Retention Matrix', status: 'Processing' },
];
</script>

<style lang="scss" scoped>
.bg-navy { background-color: var(--sams-navy); }
.border-bottom { border-bottom: 1px solid var(--sams-border); }
</style>
