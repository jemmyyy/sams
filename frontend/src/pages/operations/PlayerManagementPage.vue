<template>
  <q-page class="q-pa-lg">
    <div class="row items-center q-mb-xl">
      <div class="col">
        <div class="text-mono text-min text-grey-5 letter-spacing-2 uppercase q-mb-sm">Roster Control</div>
        <h4 class="text-apex heading-md no-margin text-white">
          PLAYER <span class="text-pro-blue">MANAGEMENT</span>
        </h4>
        <div class="text-grey-5 text-subtitle1 text-mono text-min uppercase q-mt-sm">Manage athlete profiles and roster assignments</div>
      </div>
    </div>

    <q-card flat class="elite-card">
      <q-card-section class="row items-center justify-between">
         <q-input v-model="search" dense outlined placeholder="Search players..." style="width: 300px" dark color="white" />
         <q-btn unelevated class="btn-victory text-mono" label="Add Player" icon="add" />
      </q-card-section>
      <q-table
        :rows="players"
        :columns="columns"
        row-key="id"
        flat
        dark
        :loading="loading"
        class="sams-table"
      />
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../../api';

const players = ref<Record<string, unknown>[]>([]);
const search = ref('');
const loading = ref(false);

const columns = [
  { name: 'id', label: 'ID', field: 'id', sortable: true },
  { name: 'first_name', label: 'First Name', field: 'first_name', sortable: true },
  { name: 'last_name', label: 'Last Name', field: 'last_name', sortable: true },
  { name: 'reg', label: 'Registration #', field: 'registration_number', sortable: true },
  { name: 'dob', label: 'Date of Birth', field: 'birth_date', sortable: true }
];

onMounted(async () => {
  loading.value = true;
  try {
    const response = await api.get('players/');
    players.value = response.data.results || response.data;
  } catch (error) {
    console.error('Failed to fetch players:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.elite-card {
  border-radius: var(--sams-radius-lg);
  border: 1px solid var(--sams-border);
  background: var(--sams-obsidian);
}

.sams-table :deep(.q-table) {
  background: transparent;
  color: #f8fafc;
}
.sams-table :deep(.q-table thead th) {
  color: #94a3b8;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.sams-table :deep(.q-table tbody td) {
  color: #cbd5e1;
}
</style>
