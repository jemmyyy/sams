<template>
  <q-page class="q-pa-xl animate-up">
    <div class="row items-end justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin text-white">Cancellations</h1>
        <div class="text-subtitle1 text-grey-5">Review and process session cancellation requests.</div>
      </div>
    </div>

    <q-card flat bordered class="sams-card q-mb-lg">
      <q-tabs v-model="tab" no-caps active-color="primary" indicator-color="primary" class="text-grey-5 bg-surface-2" dark>
        <q-tab name="pending" label="Pending" />
        <q-tab name="approved" label="Approved" />
        <q-tab name="rejected" label="Rejected" />
      </q-tabs>

      <q-tab-panels v-model="tab" animated dark>
        <q-tab-panel name="pending" class="q-pa-none">
          <q-list dark separator>
            <q-item v-for="req in pendingRequests" :key="req.id" class="q-py-md">
              <q-item-section>
                <q-item-label class="text-white text-weight-bold">
                  {{ req.player_name }} — {{ req.session_title }}
                </q-item-label>
                <q-item-label caption class="text-grey-5">
                  {{ req.reason }} · Requested {{ req.request_date }}
                </q-item-label>
              </q-item-section>
              <q-item-section side>
                <div class="row q-gutter-sm">
                  <q-btn unelevated color="positive" label="Approve" size="sm" @click="review(req.id, 'approved')" />
                  <q-btn unelevated color="negative" label="Reject" size="sm" @click="review(req.id, 'rejected')" />
                </div>
              </q-item-section>
            </q-item>
            <q-item v-if="!pendingRequests.length" class="text-grey-5 text-center q-pa-lg">
              <q-item-section>No pending cancellation requests</q-item-section>
            </q-item>
          </q-list>
        </q-tab-panel>

        <q-tab-panel name="approved" class="q-pa-none">
          <q-list dark separator>
            <q-item v-for="req in approvedRequests" :key="req.id">
              <q-item-section>
                <q-item-label class="text-white">{{ req.player_name }} — {{ req.session_title }}</q-item-label>
                <q-item-label caption class="text-grey-5">Approved {{ req.review_date }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-tab-panel>

        <q-tab-panel name="rejected" class="q-pa-none">
          <q-list dark separator>
            <q-item v-for="req in rejectedRequests" :key="req.id">
              <q-item-section>
                <q-item-label class="text-white">{{ req.player_name }} — {{ req.session_title }}</q-item-label>
                <q-item-label caption class="text-grey-5">Rejected {{ req.review_date }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-tab-panel>
      </q-tab-panels>
    </q-card>

    <q-dialog v-model="showReviewDialog" persistent>
      <q-card class="sams-card bg-surface-1" style="min-width: 400px">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-white q-mb-md">Review Cancellation</div>
          <q-input v-model="reviewNotes" label="Review Notes" type="textarea" dark outlined class="q-mb-md" />
          <div class="row justify-end q-gutter-md">
            <q-btn flat label="Cancel" color="grey-5" v-close-popup />
            <q-btn unelevated label="Submit" class="sams-btn sams-btn-primary" @click="submitReview" />
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApi } from '../../composables/useApi'

const { get, post } = useApi()

const tab = ref('pending')
const showReviewDialog = ref(false)
const reviewNotes = ref('')
const currentReviewId = ref('')
const currentAction = ref('')

interface CancellationRequest {
  id: string
  player_name: string
  session_title: string
  reason: string
  status: string
  request_date: string
  review_date: string | null
}

const requests = ref<CancellationRequest[]>([])

const pendingRequests = computed(() => requests.value.filter((r) => r.status === 'pending'))
const approvedRequests = computed(() => requests.value.filter((r) => r.status === 'approved'))
const rejectedRequests = computed(() => requests.value.filter((r) => r.status === 'rejected'))

async function fetchRequests() {
  try {
    const data = await get<CancellationRequest[]>('cancellations/')
    requests.value = Array.isArray(data) ? data : (data as any)?.results || []
  } catch {}
}

function review(id: string, action: string) {
  currentReviewId.value = id
  currentAction.value = action
  reviewNotes.value = ''
  showReviewDialog.value = true
}

async function submitReview() {
  await post(`cancellations/${currentReviewId.value}/review/`, {
    status: currentAction.value,
    review_notes: reviewNotes.value,
  })
  showReviewDialog.value = false
  fetchRequests()
}

onMounted(() => fetchRequests())
</script>

<script lang="ts">
export default { name: 'CoachCancellationsPage' }
</script>
