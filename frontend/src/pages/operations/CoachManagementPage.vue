<template>
  <q-page class="q-pa-xl animate-up">
    <div class="row items-end justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin text-white">Coach Management</h1>
        <div class="text-subtitle1 text-grey-5">Manage coaching staff, workload, and availability.</div>
      </div>
      <q-btn unelevated class="sams-btn sams-btn-primary" label="Add Coach" icon="person_add" @click="openCreateDialog" />
    </div>

    <q-card flat bordered class="sams-card">
      <SamsDataTable
        :rows="coachStore.coaches"
        :columns="columns"
        row-key="id"
        :loading="coachStore.loading"
        table-class="sams-table"
      >
        <template v-slot:body-cell-user_name="props">
          <q-td :props="props">
            <div class="row items-center q-gutter-sm">
              <q-avatar size="32px" color="primary" text-color="white">
                {{ (props.row.user_name || '?')[0] }}
              </q-avatar>
              <span class="text-white">{{ props.row.user_name }}</span>
            </div>
          </q-td>
        </template>
        <template v-slot:body-cell-is_active="props">
          <q-td :props="props">
            <q-toggle v-model="props.row.is_active" @update:model-value="toggleCoach(props.row)" color="primary" />
          </q-td>
        </template>
        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <q-btn flat round icon="schedule" color="info" @click="openAvailability(props.row)">
              <q-tooltip>Manage Availability</q-tooltip>
            </q-btn>
            <q-btn flat round icon="analytics" color="warning" @click="viewWorkload(props.row)">
              <q-tooltip>View Workload</q-tooltip>
            </q-btn>
            <q-btn flat round icon="edit" color="primary" @click="openEditDialog(props.row)" />
          </q-td>
        </template>
      </SamsDataTable>
    </q-card>

    <q-dialog v-model="showDialog" persistent>
      <q-card class="sams-card bg-surface-1" style="min-width: 500px">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-white q-mb-md">{{ isEditing ? 'Edit Coach' : 'Add Coach' }}</div>
          <q-form @submit="saveCoach">
            <q-select v-model="form.user_id" :options="[]" label="User Account" dark outlined class="q-mb-md" />
            <q-input v-model="form.specializations_str" label="Specializations (comma-separated)" dark outlined class="q-mb-md" />
            <q-input v-model="form.bio" label="Bio" type="textarea" dark outlined class="q-mb-md" />
            <q-input v-model.number="form.max_weekly_hours" label="Max Weekly Hours" type="number" dark outlined class="q-mb-md" />
            <div class="row justify-end q-gutter-md">
              <q-btn flat label="Cancel" color="grey-5" v-close-popup />
              <q-btn unelevated type="submit" label="Save" class="sams-btn sams-btn-primary" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-dialog v-model="showAvailabilityDialog" persistent>
      <q-card class="sams-card bg-surface-1" style="min-width: 600px">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-white q-mb-md">
            Availability — {{ selectedCoach?.user_name }}
          </div>
          <q-list dark separator>
            <q-item v-for="a in availabilities" :key="a.id">
              <q-item-section>
                {{ ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][a.day_of_week] }}
                {{ a.start_time }}–{{ a.end_time }}
              </q-item-section>
              <q-item-section side>
                <q-btn flat round icon="delete" color="negative" @click="removeAvailability(a.id)" />
              </q-item-section>
            </q-item>
          </q-list>
          <q-form @submit="addAvailability" class="q-mt-md row q-gutter-sm items-end">
            <q-select v-model="newAvail.day_of_week" :options="dayOptions" label="Day" dark outlined style="width: 140px" />
            <q-input v-model="newAvail.start_time" label="Start" type="time" dark outlined style="width: 130px" />
            <q-input v-model="newAvail.end_time" label="End" type="time" dark outlined style="width: 130px" />
            <q-btn unelevated type="submit" label="Add" class="sams-btn sams-btn-primary" />
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useCoachStore } from '../../stores/coaches'
import SamsDataTable from '../../components/common/SamsDataTable.vue'

const coachStore = useCoachStore()

const showDialog = ref(false)
const showAvailabilityDialog = ref(false)
const isEditing = ref(false)
const selectedCoach = ref<any>(null)
const availabilities = ref<any[]>([])
const newAvail = reactive({ day_of_week: 0, start_time: '09:00', end_time: '17:00' })

const form = reactive({
  id: '',
  user_id: '',
  specializations_str: '',
  bio: '',
  max_weekly_hours: 40,
})

const dayOptions = [
  { label: 'Monday', value: 0 }, { label: 'Tuesday', value: 1 },
  { label: 'Wednesday', value: 2 }, { label: 'Thursday', value: 3 },
  { label: 'Friday', value: 4 }, { label: 'Saturday', value: 5 },
  { label: 'Sunday', value: 6 },
]

const columns = [
  { name: 'user_name', label: 'COACH', field: 'user_name', align: 'left' as const, sortable: true },
  { name: 'user_email', label: 'EMAIL', field: 'user_email', align: 'left' as const },
  { name: 'max_weekly_hours', label: 'MAX HRS/WK', field: 'max_weekly_hours', align: 'center' as const },
  { name: 'is_active', label: 'ACTIVE', field: 'is_active', align: 'center' as const },
  { name: 'actions', label: 'ACTIONS', field: 'id', align: 'center' as const },
]

onMounted(() => {
  coachStore.fetchCoaches()
})

function openCreateDialog() {
  isEditing.value = false
  Object.assign(form, { id: '', user_id: '', specializations_str: '', bio: '', max_weekly_hours: 40 })
  showDialog.value = true
}

function openEditDialog(coach: any) {
  isEditing.value = true
  Object.assign(form, {
    id: coach.id,
    user_id: coach.user?.id || '',
    specializations_str: (coach.specializations || []).join(', '),
    bio: coach.bio || '',
    max_weekly_hours: coach.max_weekly_hours,
  })
  showDialog.value = true
}

async function saveCoach() {
  const payload = {
    user_id: form.user_id,
    specializations: form.specializations_str.split(',').map((s: string) => s.trim()).filter(Boolean),
    bio: form.bio,
    max_weekly_hours: form.max_weekly_hours,
  }
  if (isEditing.value) {
    await coachStore.updateCoach(form.id, payload)
  } else {
    await coachStore.createCoach(payload)
  }
  showDialog.value = false
}

async function toggleCoach(coach: any) {
  await coachStore.toggleActive(coach.id)
}

async function openAvailability(coach: any) {
  selectedCoach.value = coach
  availabilities.value = await coachStore.fetchAvailabilities(coach.id)
  showAvailabilityDialog.value = true
}

async function addAvailability() {
  await coachStore.addAvailability(selectedCoach.value.id, { ...newAvail })
  availabilities.value = await coachStore.fetchAvailabilities(selectedCoach.value.id)
}

async function removeAvailability(availId: string) {
  await coachStore.removeAvailability(selectedCoach.value.id, availId)
  availabilities.value = await coachStore.fetchAvailabilities(selectedCoach.value.id)
}

function viewWorkload(coach: any) {
  coachStore.fetchWorkload(coach.id)
}
</script>

<script lang="ts">
export default { name: 'CoachManagementPage' }
</script>
