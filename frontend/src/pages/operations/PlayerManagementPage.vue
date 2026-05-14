<template>
  <q-page class="q-pa-lg">
    <div class="row items-center q-mb-xl">
      <div class="col">
        <h4 class="text-weight-black no-margin text-dark uppercase letter-spacing-1">
          PLAYER <span class="text-info">MANAGEMENT</span>
        </h4>
        <div class="text-grey-7 text-subtitle1">Manage athlete profiles and roster assignments</div>
      </div>
    </div>

    <q-card flat bordered class="ops-card bg-white">
      <q-card-section class="row items-center justify-between">
         <q-input v-model="search" dense outlined placeholder="Search players..." style="width: 300px">
           <template v-slot:append>
             <q-icon name="search" />
           </template>
         </q-input>
         <q-btn color="info" label="Add Player" icon="add" />
      </q-card-section>
      <q-table
        :rows="players"
        :columns="columns"
        row-key="id"
        flat
        :loading="loading"
      />
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../../api';

const players = ref<any[]>([]);
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
.ops-card {
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}
</style>
