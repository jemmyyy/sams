<template>
  <q-page class="q-pa-xl animate-up">
    <div class="row items-end justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin text-white">Session Scheduling</h1>
        <div class="text-subtitle1 text-grey-5">Manage session series, occurrences, and venues.</div>
      </div>
      <div class="row q-gutter-md">
        <q-btn unelevated class="sams-btn sams-btn-action" label="New Venue" icon="location_on" outline @click="venueDialog = true" />
        <q-btn unelevated class="sams-btn sams-btn-primary" label="New Series" icon="add_circle" @click="openSeriesDialog" />
      </div>
    </div>

    <q-card flat bordered class="sams-card q-mb-lg">
      <q-tabs v-model="tab" no-caps active-color="primary" indicator-color="primary" class="text-grey-5 bg-surface-2" dark>
        <q-tab name="series" label="Session Series" />
        <q-tab name="venues" label="Venues" />
        <q-tab name="occurrences" label="Occurrences" />
      </q-tabs>

      <q-tab-panels v-model="tab" animated dark>
        <q-tab-panel name="series" class="q-pa-none">
          <SamsDataTable
            :rows="sessionsStore.series"
            :columns="seriesColumns"
            row-key="id"
            :loading="sessionsStore.loading"
            table-class="sams-table"
          >
            <template v-slot:body-cell-venue="props">
              <q-td :props="props">{{ props.row.venue?.name || 'N/A' }}</q-td>
            </template>
            <template v-slot:body-cell-is_active="props">
              <q-td :props="props">
                <q-badge :color="props.value ? 'positive' : 'negative'" rounded class="q-px-md">
                  {{ props.value ? 'Active' : 'Inactive' }}
                </q-badge>
              </q-td>
            </template>
          </SamsDataTable>
        </q-tab-panel>

        <q-tab-panel name="venues" class="q-pa-none">
          <SamsDataTable
            :rows="venues"
            :columns="venueColumns"
            row-key="id"
            table-class="sams-table"
          />
        </q-tab-panel>

        <q-tab-panel name="occurrences" class="q-pa-none">
          <SamsDataTable
            :rows="sessionsStore.sessions"
            :columns="occurrenceColumns"
            row-key="id"
            :loading="sessionsStore.loading"
            table-class="sams-table"
          >
            <template v-slot:body-cell-series="props">
              <q-td :props="props">{{ props.row.series?.title || 'N/A' }}</q-td>
            </template>
            <template v-slot:body-cell-venue="props">
              <q-td :props="props">{{ props.row.venue?.name || 'N/A' }}</q-td>
            </template>
            <template v-slot:body-cell-status="props">
              <q-td :props="props">
                <q-badge
                  :color="props.value === 'scheduled' ? 'info' : props.value === 'completed' ? 'positive' : 'negative'"
                  rounded class="q-px-md"
                >
                  {{ props.value }}
                </q-badge>
              </q-td>
            </template>
          </SamsDataTable>
        </q-tab-panel>
      </q-tab-panels>
    </q-card>

    <q-dialog v-model="seriesDialog" persistent>
      <q-card class="sams-card bg-surface-1" style="min-width: 600px">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-white q-mb-md">New Session Series</div>
          <q-form @submit="createSeries">
            <q-input v-model="seriesForm.title" label="Title" dark outlined class="q-mb-md" :rules="[(v: string) => !!v || 'Required']" />
            <q-input v-model="seriesForm.recurrence_rule" label="Recurrence Rule (RRULE)" dark outlined class="q-mb-md" hint="FREQ=WEEKLY;BYDAY=MO,WE" />
            <div class="row q-col-gutter-md q-mb-md">
              <q-input v-model="seriesForm.start_date" label="Start Date" type="date" dark outlined class="col" />
              <q-input v-model="seriesForm.end_date" label="End Date" type="date" dark outlined class="col" />
            </div>
            <div class="row q-col-gutter-md q-mb-md">
              <q-input v-model="seriesForm.start_time" label="Start Time" type="time" dark outlined class="col" />
              <q-input v-model="seriesForm.end_time" label="End Time" type="time" dark outlined class="col" />
            </div>
            <q-select v-model="seriesForm.venue_id" :options="venueOptions" label="Venue" dark outlined class="q-mb-md" />
            <q-input v-model.number="seriesForm.max_capacity" label="Max Capacity" type="number" dark outlined class="q-mb-md" />
            <div class="row justify-end q-gutter-md">
              <q-btn flat label="Cancel" color="grey-5" v-close-popup />
              <q-btn unelevated type="submit" label="Create" class="sams-btn sams-btn-primary" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-dialog v-model="venueDialog" persistent>
      <q-card class="sams-card bg-surface-1" style="min-width: 500px">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-white q-mb-md">New Venue</div>
          <q-form @submit="createVenue">
            <q-input v-model="venueForm.name" label="Venue Name" dark outlined class="q-mb-md" :rules="[(v: string) => !!v || 'Required']" />
            <q-input v-model="venueForm.location" label="Location" dark outlined class="q-mb-md" />
            <q-input v-model.number="venueForm.capacity" label="Capacity" type="number" dark outlined class="q-mb-md" />
            <div class="row justify-end q-gutter-md">
              <q-btn flat label="Cancel" color="grey-5" v-close-popup />
              <q-btn unelevated type="submit" label="Create" class="sams-btn sams-btn-primary" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useSessionsStore } from '../../stores/sessions'
import { useApi } from '../../composables/useApi'
import SamsDataTable from '../../components/common/SamsDataTable.vue'

const sessionsStore = useSessionsStore()
const { get, post } = useApi()

const tab = ref('series')
const seriesDialog = ref(false)
const venueDialog = ref(false)
const venues = ref<any[]>([])

const seriesForm = reactive({
  title: '', recurrence_rule: 'FREQ=WEEKLY;BYDAY=MO,WE',
  start_date: '', end_date: '', start_time: '09:00', end_time: '10:30',
  venue_id: '', max_capacity: 20,
})

const venueForm = reactive({ name: '', location: '', capacity: 50 })

const venueOptions = computed(() => venues.value.map((v: any) => ({ label: v.name, value: v.id })))

const seriesColumns = [
  { name: 'title', label: 'TITLE', field: 'title', align: 'left' as const, sortable: true },
  { name: 'recurrence_rule', label: 'SCHEDULE', field: 'recurrence_rule', align: 'left' as const },
  { name: 'start_time', label: 'TIME', field: 'start_time', align: 'center' as const },
  { name: 'venue', label: 'VENUE', field: (row: any) => row.venue?.name, align: 'left' as const },
  { name: 'max_capacity', label: 'CAP', field: 'max_capacity', align: 'center' as const },
  { name: 'is_active', label: 'STATUS', field: 'is_active', align: 'center' as const },
]

const venueColumns = [
  { name: 'name', label: 'NAME', field: 'name', align: 'left' as const, sortable: true },
  { name: 'location', label: 'LOCATION', field: 'location', align: 'left' as const },
  { name: 'capacity', label: 'CAPACITY', field: 'capacity', align: 'center' as const },
]

const occurrenceColumns = [
  { name: 'series', label: 'SERIES', field: (row: any) => row.series?.title, align: 'left' as const },
  { name: 'start_datetime', label: 'START', field: 'start_datetime', align: 'center' as const },
  { name: 'end_datetime', label: 'END', field: 'end_datetime', align: 'center' as const },
  { name: 'venue', label: 'VENUE', field: (row: any) => row.venue?.name, align: 'left' as const },
  { name: 'status', label: 'STATUS', field: 'status', align: 'center' as const },
]

onMounted(async () => {
  sessionsStore.fetchSessions()
  try {
    const data = await get<any[]>('sessions/venues/')
    venues.value = Array.isArray(data) ? data : data?.results || []
  } catch {}
})

async function createSeries() {
  await post('sessions/series/', {
    ...seriesForm,
    venue: seriesForm.venue_id,
  })
  seriesDialog.value = false
}

async function createVenue() {
  await post('sessions/venues/', venueForm)
  venueDialog.value = false
}
</script>

<script lang="ts">
export default { name: 'SessionSchedulingPage' }
</script>
