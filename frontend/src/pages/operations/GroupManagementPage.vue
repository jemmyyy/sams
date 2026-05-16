<template>
  <q-page class="q-pa-xl animate-up">
    <div class="row items-end justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin text-white">Group Management</h1>
        <div class="text-subtitle1 text-grey-5">Create and manage player groups and training squads.</div>
      </div>
      <q-btn unelevated class="sams-btn sams-btn-primary" label="New Group" icon="group_add" @click="openCreateDialog" />
    </div>

    <div class="row q-col-gutter-lg">
      <div class="col-12 col-md-4" v-for="group in groupStore.groups" :key="group.id">
        <q-card flat bordered class="sams-card q-pa-lg">
          <div class="row items-center justify-between q-mb-md">
            <div class="text-h6 text-white">{{ group.name }}</div>
            <q-btn flat round icon="more_vert" color="grey-5">
              <q-menu class="bg-surface-2 text-white">
                <q-list>
                  <q-item clickable @click="openEditDialog(group)">
                    <q-item-section avatar><q-icon name="edit" /></q-item-section>
                    <q-item-section>Edit</q-item-section>
                  </q-item>
                  <q-item clickable @click="deleteGroup(group.id)" class="text-negative">
                    <q-item-section avatar><q-icon name="delete" /></q-item-section>
                    <q-item-section>Delete</q-item-section>
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </div>
          <div class="text-grey-5 text-caption q-mb-sm">{{ group.description || 'No description' }}</div>
          <div class="row items-center q-gutter-sm text-grey-5">
            <q-icon name="people" size="18px" />
            <span>{{ (group.players || []).length }} players</span>
          </div>
          <div class="row items-center q-gutter-sm text-grey-5 q-mt-xs" v-if="group.coach">
            <q-icon name="badge" size="18px" />
            <span>Coach assigned</span>
          </div>
        </q-card>
      </div>
    </div>

    <q-dialog v-model="showDialog" persistent>
      <q-card class="sams-card bg-surface-1" style="min-width: 500px">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-white q-mb-md">{{ isEditing ? 'Edit Group' : 'New Group' }}</div>
          <q-form @submit="saveGroup">
            <q-input v-model="form.name" label="Group Name" dark outlined class="q-mb-md" :rules="[(v: string) => !!v || 'Required']" />
            <q-input v-model="form.description" label="Description" type="textarea" dark outlined class="q-mb-md" />
            <q-select v-model="form.coach_id" :options="coachOptions" label="Assigned Coach" dark outlined class="q-mb-md" />
            <div class="row justify-end q-gutter-md">
              <q-btn flat label="Cancel" color="grey-5" v-close-popup />
              <q-btn unelevated type="submit" label="Save" class="sams-btn sams-btn-primary" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useGroupStore } from '../../stores/groups'
import { useCoachStore } from '../../stores/coaches'

const groupStore = useGroupStore()
const coachStore = useCoachStore()

const showDialog = ref(false)
const isEditing = ref(false)

const form = reactive({
  id: '',
  name: '',
  description: '',
  coach_id: null as string | null,
})

const coachOptions = computed(() =>
  coachStore.coaches.map((c) => ({ label: c.user_name, value: c.user?.id || c.id }))
)

onMounted(() => {
  groupStore.fetchGroups()
  coachStore.fetchCoaches()
})

function openCreateDialog() {
  isEditing.value = false
  Object.assign(form, { id: '', name: '', description: '', coach_id: null })
  showDialog.value = true
}

function openEditDialog(group: any) {
  isEditing.value = true
  Object.assign(form, {
    id: group.id,
    name: group.name,
    description: group.description,
    coach_id: group.coach || null,
  })
  showDialog.value = true
}

async function saveGroup() {
  const payload = { name: form.name, description: form.description, coach: form.coach_id }
  if (isEditing.value) {
    await groupStore.updateGroup(form.id, payload)
  } else {
    await groupStore.createGroup(payload)
  }
  showDialog.value = false
}

async function deleteGroup(id: string) {
  await groupStore.deleteGroup(id)
}
</script>

<script lang="ts">
export default { name: 'GroupManagementPage' }
</script>
