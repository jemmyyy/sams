<template>
  <q-page class="q-pa-lg">
    <div class="row items-center q-mb-xl">
      <div class="col">
        <h4 class="text-weight-black no-margin text-dark uppercase letter-spacing-1">
          FINANCIAL <span class="text-info">COMMAND</span>
        </h4>
        <div class="text-grey-7 text-subtitle1">Manage revenue and receivables</div>
      </div>
    </div>

    <div class="row q-col-gutter-lg q-mb-lg">
      <div class="col-12 col-md-4">
        <q-card flat bordered class="ops-card bg-info text-white">
          <q-card-section>
            <div class="text-subtitle2 uppercase opacity-80">Total Invoiced</div>
            <div class="text-h3 text-weight-black" v-if="stats">EGP {{ stats.total_invoiced || 0 }}</div>
            <q-spinner-puff v-else color="white" size="2em" />
          </q-card-section>
        </q-card>
      </div>
      
      <div class="col-12 col-md-4">
        <q-card flat bordered class="ops-card bg-white">
          <q-card-section>
            <div class="text-subtitle2 text-grey-6 uppercase">Total Outstanding</div>
            <div class="text-h3 text-weight-black text-warning" v-if="stats">EGP {{ stats.total_outstanding || 0 }}</div>
             <q-spinner-puff v-else color="warning" size="2em" />
          </q-card-section>
        </q-card>
      </div>
      
      <div class="col-12 col-md-4">
        <q-card flat bordered class="ops-card bg-white">
          <q-card-section>
            <div class="text-subtitle2 text-grey-6 uppercase">Overdue Invoices</div>
            <div class="text-h3 text-weight-black text-negative" v-if="stats">{{ stats.overdue_count || 0 }}</div>
            <q-spinner-puff v-else color="negative" size="2em" />
          </q-card-section>
        </q-card>
      </div>
    </div>

    <q-card flat bordered class="ops-card bg-white">
       <q-card-actions class="q-pa-md bg-grey-1">
         <q-btn color="info" label="Export Report" icon="download" @click="exportReport" />
       </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../../api';
import { useQuasar } from 'quasar';

const $q = useQuasar();
const stats = ref<any>(null);

onMounted(async () => {
  try {
    const response = await api.get('payments/dashboard/');
    stats.value = response.data.data;
  } catch (error) {
    console.error('Failed to fetch stats:', error);
  }
});

async function exportReport() {
  try {
    const res = await api.post('payments/dashboard/export-report/');
    $q.notify({
      type: 'positive',
      message: res.data.status || 'Export initiated.',
      position: 'top'
    });
  } catch (e) {
    $q.notify({
      type: 'negative',
      message: 'Failed to initiate export.',
      position: 'top'
    });
  }
}
</script>

<style scoped>
.ops-card {
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}
.opacity-80 { opacity: 0.8; }
</style>
