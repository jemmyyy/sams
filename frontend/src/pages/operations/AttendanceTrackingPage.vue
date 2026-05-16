<template>
  <q-page class="q-pa-xl animate-up">
    <div class="row items-end justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin text-white">Attendance Tracking</h1>
        <div class="text-subtitle1 text-grey-5">Monitor session attendance across all groups and sessions.</div>
      </div>
    </div>

    <q-card flat bordered class="sams-card q-mb-lg">
      <div class="row q-pa-lg q-col-gutter-md">
        <q-input v-model="dateFilter" label="Filter by Date" type="date" dark outlined class="col-12 col-md-3" @update:model-value="loadData" />
        <q-select v-model="statusFilter" :options="statusOptions" label="Status" dark outlined class="col-12 col-md-3" @update:model-value="loadData" />
        <q-select v-model="sessionFilter" :options="sessionOptions" label="Session" dark outlined class="col-12 col-md-4" @update:model-value="loadData" />
        <q-btn flat round icon="refresh" color="primary" class="col-auto self-end q-mb-md" @click="loadData" />
      </div>
    </q-card>

    <q-card flat bordered class="sams-card">
      <SamsDataTable
        :rows="records"
        :columns="columns"
        row-key="id"
        :loading="loading"
        table-class="sams-table"
      >
        <template v-slot:body-cell-status="props">
          <q-td :props="props">
            <q-badge
              :color="statusColor(props.value)"
              rounded class="q-px-md"
            >
              {{ props.value }}
            </q-badge>
          </q-td>
        </template>
        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <q-btn flat round icon="edit" color="primary" size="sm" />
          </q-td>
        </template>
      </SamsDataTable>
    </q-card>

    <div class="row q-col-gutter-lg q-mt-lg">
      <div class="col-12 col-md-4">
        <q-card flat bordered class="sams-card q-pa-lg text-center">
          <div class="text-h3 text-primary q-mb-sm">{{ summary.total }}</div>
          <div class="text-grey-5 uppercase text-weight-bold">Total Sessions</div>
        </q-card>
      </div>
      <div class="col-12 col-md-4">
        <q-card flat bordered class="sams-card q-pa-lg text-center">
          <div class="text-h3 text-positive q-mb-sm">{{ summary.present }}</div>
          <div class="text-grey-5 uppercase text-weight-bold">Present</div>
        </q-card>
      </div>
      <div class="col-12 col-md-4">
        <q-card flat bordered class="sams-card q-pa-lg text-center">
          <div class="text-h3 text-victory-red q-mb-sm">{{ summary.rate }}%</div>
          <div class="text-grey-5 uppercase text-weight-bold">Attendance Rate</div>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useApi } from '../../composables/useApi'
import { ATTENDANCE_STATUS, getStatusColor } from '../../utils/status'
import SamsDataTable from '../../components/common/SamsDataTable.vue'

const { get } = useApi()

const loading = ref(false)
const dateFilter = ref('')
const statusFilter = ref('')
const sessionFilter = ref('')
const records = ref<any[]>([])

const summary = reactive({ total: 0, present: 0, rate: 0 })

const statusOptions = [
  { label: 'All', value: '' },
  { label: 'Present', value: 'present' },
  { label: 'Absent', value: 'absent' },
  { label: 'Late', value: 'late' },
  { label: 'Excused', value: 'excused' },
]

const sessionOptions: { label: string; value: string }[] = []

const columns = [
  { name: 'player', label: 'PLAYER', field: 'player_name', align: 'left' as const, sortable: true },
  { name: 'session', label: 'SESSION', field: 'session_title', align: 'left' as const },
  { name: 'status', label: 'STATUS', field: 'status', align: 'center' as const },
  { name: 'marked_by', label: 'MARKED BY', field: 'marked_by_name', align: 'left' as const },
  { name: 'marked_at', label: 'MARKED AT', field: 'marked_at', align: 'center' as const },
  { name: 'actions', label: '', field: 'id', align: 'center' as const },
]

function statusColor(s: string) {
  return getStatusColor(ATTENDANCE_STATUS, s)
}

async function loadData() {
  loading.value = true
  try {
    const params: Record<string, string> = {}
    if (dateFilter.value) params.date = dateFilter.value
    if (statusFilter.value) params.status = statusFilter.value
    if (sessionFilter.value) params.session = sessionFilter.value

    const data = await get<any>('attendance/', params)
    records.value = Array.isArray(data) ? data : data?.results || []
    summary.total = records.value.length
    summary.present = records.value.filter((r: any) => r.status === 'present').length
    summary.rate = summary.total ? Math.round((summary.present / summary.total) * 100) : 0
  } catch {}
  loading.value = false
}

onMounted(() => loadData())
</script>

<script lang="ts">
export default { name: 'AttendanceTrackingPage' }
</script>
