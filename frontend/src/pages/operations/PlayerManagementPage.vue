<template>
  <q-page class="q-pa-xl animate-up">
    <!-- Header Summary -->
    <div class="row items-center justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin text-white">Athlete Roster</h1>
        <div class="text-subtitle1 text-grey-5">Manage and monitor all academy players.</div>
      </div>
      <q-btn 
        unelevated 
        class="sams-btn sams-btn-primary" 
        label="Register Athlete" 
        icon="person_add" 
        @click="showAddDialog = true"
      />
    </div>

    <!-- Filters & Search -->
    <div class="row q-mb-lg q-gutter-md items-center">
      <SamsInput
        v-model="search"
        dense
        placeholder="Search by name or ID..."
        class="col-12 col-md-4"
      >
        <template #prepend>
          <q-icon name="search" />
        </template>
      </SamsInput>
      
      <q-space />
      
      <q-btn outline color="grey-6" icon="filter_list" label="Filters" class="sams-btn" />
      <q-btn outline color="grey-6" icon="file_download" label="Export" class="sams-btn" />
    </div>

    <!-- Players Table -->
    <SamsDataTable
      :rows="filteredPlayers"
      :columns="columns"
      :loading="playersStore.loading"
      row-key="id"
    >
      <template #body-cell-name="props">
        <q-td :props="props">
          <div class="row items-center no-wrap">
            <q-avatar size="32px" class="q-mr-md border-b">
              <img :src="`https://ui-avatars.com/api/?name=${props.row.first_name}+${props.row.last_name}&background=random`" />
            </q-avatar>
            <div class="column">
              <div class="text-weight-bold text-white">{{ props.row.first_name }} {{ props.row.last_name }}</div>
              <div class="text-caption text-grey-5">{{ props.row.registration_number }}</div>
            </div>
          </div>
        </q-td>
      </template>

      <template #body-cell-actions="props">
        <q-td :props="props">
          <q-btn flat round dense icon="visibility" color="primary" @click="viewPlayer(props.row)" />
          <q-btn flat round dense icon="edit" color="grey-5" />
        </q-td>
      </template>
    </SamsDataTable>

    <!-- Add Player Dialog -->
    <SamsDialog
      v-model="showAddDialog"
      title="Register New Athlete"
      subtitle="Complete the profile to add a new player to the academy roster."
    >
      <div class="q-gutter-y-md">
        <div class="row q-col-gutter-md">
          <div class="col-12 col-sm-6">
            <SamsInput v-model="newPlayer.first_name" label="First Name" />
          </div>
          <div class="col-12 col-sm-6">
            <SamsInput v-model="newPlayer.last_name" label="Last Name" />
          </div>
        </div>
        <SamsInput v-model="newPlayer.birth_date" label="Date of Birth" type="date" stack-label />
        <q-select
          v-model="newPlayer.gender"
          :options="['Male', 'Female']"
          label="Gender"
          outlined
          dark
          bg-color="surface-2"
          class="sams-input"
        />
        <SamsInput v-model="newPlayer.medical_conditions" label="Medical Conditions" type="textarea" autogrow />
      </div>

      <template #actions>
        <q-btn flat label="Cancel" color="grey-6" v-close-popup class="q-px-lg" />
        <q-btn unelevated label="Confirm Registration" color="primary" @click="savePlayer" class="q-px-xl text-weight-bold" />
      </template>
    </SamsDialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, reactive } from 'vue';
import { usePlayersStore } from '../../stores/players';
import SamsInput from '../../components/common/SamsInput.vue';
import SamsDataTable from '../../components/common/SamsDataTable.vue';
import SamsDialog from '../../components/common/SamsDialog.vue';
import { useQuasar } from 'quasar';

const $q = useQuasar();
const playersStore = usePlayersStore();
const search = ref('');
const showAddDialog = ref(false);

const newPlayer = reactive({
  first_name: '',
  last_name: '',
  birth_date: '',
  gender: 'Male',
  medical_conditions: ''
});

const columns = [
  { name: 'name', label: 'Athlete', field: (row: any) => `${row.first_name} ${row.last_name}`, align: 'left' as const, sortable: true },
  { name: 'dob', label: 'DOB', field: 'birth_date', align: 'left' as const, sortable: true },
  { name: 'reg', label: 'Reg #', field: 'registration_number', align: 'left' as const, sortable: true },
  { name: 'actions', label: '', field: 'actions', align: 'right' as const },
];

const filteredPlayers = computed(() => {
  if (!search.value) return playersStore.players;
  const s = search.value.toLowerCase();
  return playersStore.players.filter(p => 
    p.first_name.toLowerCase().includes(s) || 
    p.last_name.toLowerCase().includes(s) || 
    p.registration_number.toLowerCase().includes(s)
  );
});

onMounted(() => {
  playersStore.fetchPlayers();
});

async function savePlayer() {
  try {
    await playersStore.addPlayer(newPlayer);
    showAddDialog.value = false;
    $q.notify({ type: 'positive', message: 'Athlete registered successfully' });
  } catch (err) {
    $q.notify({ type: 'negative', message: 'Failed to register athlete' });
  }
}

function viewPlayer(player: any) {
  // Navigation to detailed profile
  console.log('Viewing player:', player);
}
</script>

<style lang="scss" scoped>
.border-b { border-bottom: 1px solid var(--sams-border); }
.letter-spacing-1 { letter-spacing: 1px; }
.letter-spacing-2 { letter-spacing: 2px; }
</style>
