<template>
  <q-page class="q-pa-lg">
    <div class="row items-center q-mb-xl">
      <div class="col">
        <div class="text-mono text-min text-grey-5 letter-spacing-2 uppercase q-mb-sm">Financial Oversight</div>
        <h4 class="text-apex heading-md no-margin text-white">
          FINANCIAL <span class="text-victory-red">COMMAND</span>
        </h4>
      </div>
    </div>

    <div class="row q-col-gutter-lg q-mb-lg">
      <div class="col-12 col-md-4">
        <q-card flat class="elite-card">
          <q-card-section>
            <div class="text-mono text-min text-grey-5 uppercase q-mb-sm">Total Invoiced</div>
            <div class="text-h3 text-weight-black text-white text-apex" v-if="stats">EGP {{ stats.total_invoiced || 0 }}</div>
            <q-spinner-puff v-else color="victory-red" size="2em" />
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card flat class="elite-card">
          <q-card-section>
            <div class="text-mono text-min text-grey-5 uppercase q-mb-sm">Total Outstanding</div>
            <div class="text-h3 text-weight-black text-energy-volt text-apex" v-if="stats">EGP {{ stats.total_outstanding || 0 }}</div>
            <q-spinner-puff v-else color="energy-volt" size="2em" />
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card flat class="elite-card">
          <q-card-section>
            <div class="text-mono text-min text-grey-5 uppercase q-mb-sm">Overdue Invoices</div>
            <div class="text-h3 text-weight-black text-victory-red text-apex" v-if="stats">{{ stats.overdue_count || 0 }}</div>
            <q-spinner-puff v-else color="victory-red" size="2em" />
          </q-card-section>
        </q-card>
      </div>
    </div>

    <q-card flat class="elite-card q-px-md q-py-sm">
       <q-card-actions class="q-pa-md">
         <q-btn unelevated class="btn-victory text-mono" label="Export Report" icon="download" @click="exportReport" />
       </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../../api';
import { useQuasar } from 'quasar';

const $q = useQuasar();
const stats = ref<Record<string, unknown> | null>(null);

onMounted(async () => {
  try {
    const response = await api.get('payments/dashboard/');
    // api interceptor already unwraps StandardizedJSONRenderer { success, data, errors }
    stats.value = response.data;
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
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Failed to initiate export.',
      position: 'top'
    });
  }
}
</script>

<style scoped>
.elite-card {
  border-radius: var(--sams-radius-lg);
  border: 1px solid var(--sams-border);
  background: var(--sams-obsidian);
}
</style>
