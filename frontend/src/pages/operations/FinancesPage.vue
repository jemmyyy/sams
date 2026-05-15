<template>
  <q-page class="q-pa-xl animate-up">
    <!-- Header Summary -->
    <div class="row items-center justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin text-white">Financial Matrix</h1>
        <div class="text-subtitle1 text-grey-5">Monitor revenue streams and transaction history.</div>
      </div>
      <div class="row q-gutter-md">
        <q-btn outline color="primary" label="Generate Ledger" icon="assessment" class="sams-btn" @click="exportReport" />
        <q-btn unelevated color="primary" label="New Entry" icon="add" class="sams-btn" />
      </div>
    </div>

    <!-- Metric Grid -->
    <div class="row q-col-gutter-lg q-mb-xl">
      <div class="col-12 col-md-4">
        <q-card flat bordered class="sams-card q-pa-lg">
          <div class="row items-center justify-between q-mb-md">
            <div class="stat-icon row items-center justify-center bg-surface-2 border-b">
               <q-icon name="payments" size="24px" color="primary" />
            </div>
            <div class="text-positive text-weight-bold">+12.4%</div>
          </div>
          <div class="text-h4 text-heading text-white q-mb-xs">{{ (stats?.total_invoiced || 0).toLocaleString() }} EGP</div>
          <div class="text-caption text-grey-5 uppercase text-weight-bold letter-spacing-1">Total Invoiced</div>
        </q-card>
      </div>
      
      <div class="col-12 col-md-4">
        <q-card flat bordered class="sams-card q-pa-lg">
          <div class="row items-center justify-between q-mb-md">
            <div class="stat-icon row items-center justify-center bg-surface-2 border-b">
               <q-icon name="account_balance_wallet" size="24px" color="warning" />
            </div>
            <div class="text-warning text-weight-bold">{{ stats?.overdue_count || 0 }} Overdue</div>
          </div>
          <div class="text-h4 text-heading text-white q-mb-xs">{{ (stats?.total_outstanding || 0).toLocaleString() }} EGP</div>
          <div class="text-caption text-grey-5 uppercase text-weight-bold letter-spacing-1">Outstanding Arrears</div>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card flat bordered class="sams-card q-pa-lg">
          <div class="row items-center justify-between q-mb-md">
            <div class="stat-icon row items-center justify-center bg-surface-2 border-b">
               <q-icon name="receipt_long" size="24px" color="success" />
            </div>
            <div class="text-grey-5">System Health</div>
          </div>
          <div class="text-h4 text-heading text-white q-mb-xs">Operational</div>
          <div class="text-caption text-grey-5 uppercase text-weight-bold letter-spacing-1">Status</div>
        </q-card>
      </div>
    </div>

    <!-- Transactions Table -->
    <SamsDataTable
      title="Recent Transactions"
      :rows="financesStore.transactions"
      :columns="columns"
      :loading="financesStore.loading"
      row-key="id"
    >
      <template #body-cell-status="props">
        <q-td :props="props">
          <q-badge 
            rounded 
            :color="props.value === 'Completed' || props.value === 'Paid' ? 'success' : (props.value === 'Pending' ? 'warning' : 'victory-red')" 
            class="q-px-md q-py-xs"
          >
            {{ props.value }}
          </q-badge>
        </q-td>
      </template>

      <template #body-cell-amount="props">
        <q-td :props="props" class="text-weight-bold text-white">
          {{ (props.value || 0).toLocaleString() }} EGP
        </q-td>
      </template>
    </SamsDataTable>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useFinancesStore } from '../../stores/finances';
import SamsDataTable from '../../components/common/SamsDataTable.vue';
import api from '../../api';
import { useQuasar } from 'quasar';

const $q = useQuasar();
const financesStore = useFinancesStore();
const stats = ref<any>(null);

const columns = [
  { name: 'player', label: 'Athlete', field: (row: any) => row.player_name || row.player, align: 'left' as const, sortable: true },
  { name: 'date', label: 'Date', field: 'date', align: 'left' as const, sortable: true },
  { name: 'amount', label: 'Amount', field: 'amount', align: 'left' as const, sortable: true },
  { name: 'type', label: 'Type', field: 'type', align: 'left' as const },
  { name: 'status', label: 'Status', field: 'status', align: 'center' as const },
];

onMounted(async () => {
  financesStore.fetchTransactions();
  try {
    const response = await api.get('payments/dashboard/');
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

<style lang="scss" scoped>
.stat-icon {
  width: 44px; height: 44px;
  border-radius: 12px;
}
.letter-spacing-1 { letter-spacing: 1px; }
.border-b { border: 1px solid var(--sams-border); }
</style>
