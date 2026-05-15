<template>
  <q-page class="q-pa-xl animate-up">
    <!-- Header Summary -->
    <div class="row items-center justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin text-white">Session Cancellations</h1>
        <div class="text-subtitle1 text-grey-5">Manage your absence requests and view cancellation history.</div>
      </div>
      <q-btn 
        unelevated 
        class="sams-btn sams-btn-primary" 
        label="Request Cancellation" 
        icon="event_busy" 
        @click="showRequestDialog = true"
      />
    </div>

    <!-- Cancellations Table -->
    <q-card flat bordered class="sams-card">
      <SamsDataTable
        title="My Requests"
        :rows="cancellationsStore.cancellations"
        :columns="columns"
        :loading="cancellationsStore.loading"
        row-key="id"
      >
        <template #body-cell-status="props">
          <q-td :props="props">
            <q-badge 
              rounded 
              :color="props.value === 'Approved' ? 'success' : (props.value === 'Pending' ? 'warning' : 'victory-red')" 
              class="q-px-md q-py-xs text-weight-bold"
            >
              {{ props.value }}
            </q-badge>
          </q-td>
        </template>
        <template #no-data>
           <div class="full-width row flex-center text-grey-5 q-pa-xl">
              <q-icon size="2em" name="event_available" class="q-mr-sm" />
              <span>No cancellation requests found.</span>
           </div>
        </template>
      </SamsDataTable>
    </q-card>

    <!-- Request Dialog -->
    <SamsDialog
      v-model="showRequestDialog"
      title="Request Session Absence"
      subtitle="Submit a reason for your absence. Requires operations approval."
    >
      <div class="q-gutter-y-md">
        <q-select
          v-model="newRequest.session"
          :options="upcomingSessions"
          label="Select Upcoming Session"
          outlined
          dark
          bg-color="surface-2"
          class="sams-input"
          emit-value
          map-options
        />
        <SamsInput v-model="newRequest.reason" label="Reason for Absence" type="textarea" autogrow />
      </div>

      <template #actions>
        <q-btn flat label="Cancel" color="grey-6" v-close-popup class="q-px-lg" />
        <q-btn unelevated label="Submit Request" color="primary" @click="submitRequest" class="q-px-xl text-weight-bold" :loading="submitting" />
      </template>
    </SamsDialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue';
import { useCancellationsStore } from '../../stores/cancellations';
import SamsDataTable from '../../components/common/SamsDataTable.vue';
import SamsDialog from '../../components/common/SamsDialog.vue';
import SamsInput from '../../components/common/SamsInput.vue';
import { useQuasar } from 'quasar';

const $q = useQuasar();
const cancellationsStore = useCancellationsStore();
const showRequestDialog = ref(false);
const submitting = ref(false);

const newRequest = reactive({
  session: '',
  reason: ''
});

// Mock upcoming sessions for the select dropdown
const upcomingSessions = [
  { label: 'Technical Drill - May 16', value: 'session-1' },
  { label: 'Stamina & Power - May 18', value: 'session-2' }
];

const columns = [
  { name: 'session', label: 'Session', field: 'session', align: 'left' as const, sortable: true },
  { name: 'reason', label: 'Reason', field: 'reason', align: 'left' as const },
  { name: 'date', label: 'Requested On', field: 'created_at', align: 'left' as const, sortable: true },
  { name: 'status', label: 'Status', field: 'status', align: 'center' as const },
];

onMounted(() => {
  cancellationsStore.fetchCancellations();
});

async function submitRequest() {
  if (!newRequest.session || !newRequest.reason) {
    $q.notify({ type: 'warning', message: 'Please complete all fields' });
    return;
  }
  
  submitting.value = true;
  try {
    await cancellationsStore.requestCancellation({
      session: newRequest.session,
      reason: newRequest.reason,
      player: 'current-user-id', // Handled by backend usually
      status: 'Pending'
    });
    showRequestDialog.value = false;
    newRequest.session = '';
    newRequest.reason = '';
    $q.notify({ type: 'positive', message: 'Cancellation request submitted' });
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Failed to submit request' });
  } finally {
    submitting.value = false;
  }
}
</script>

<style lang="scss" scoped>
.sams-input {
  :deep(.q-field__control) {
    border-radius: 12px;
  }
}
</style>
