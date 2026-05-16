<template>
  <q-page class="q-pa-xl animate-up">
    <div class="row items-end justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin text-white">Communications</h1>
        <div class="text-subtitle1 text-grey-5">Send announcements and view notification history.</div>
      </div>
      <q-btn unelevated class="sams-btn sams-btn-primary" label="New Announcement" icon="campaign" @click="showCompose = true" />
    </div>

    <div class="row q-col-gutter-lg">
      <div class="col-12 col-md-8">
        <q-card flat bordered class="sams-card">
          <div class="q-pa-lg border-bottom bg-surface-2">
            <div class="text-h6 text-white">Notification History</div>
          </div>
          <q-list dark separator>
            <q-item v-for="n in notificationStore.notifications" :key="n.id">
              <q-item-section avatar>
                <q-avatar :icon="channelIcon(n.channel)" :color="n.is_read ? 'grey-7' : 'primary'" text-color="white" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-white" :class="{ 'text-weight-bold': !n.is_read }">{{ n.title }}</q-item-label>
                <q-item-label caption class="text-grey-5">{{ n.body }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <div class="text-caption text-grey-6">{{ n.sent_at }}</div>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card flat bordered class="sams-card q-pa-lg">
          <div class="text-h6 text-white q-mb-lg">Quick Stats</div>
          <div class="row q-col-gutter-md">
            <div class="col-6">
              <q-card flat class="bg-surface-2 q-pa-md text-center">
                <div class="text-h4 text-primary">{{ notificationStore.notifications.length }}</div>
                <div class="text-caption text-grey-5">Total Sent</div>
              </q-card>
            </div>
            <div class="col-6">
              <q-card flat class="bg-surface-2 q-pa-md text-center">
                <div class="text-h4 text-positive">{{ notificationStore.unreadCount }}</div>
                <div class="text-caption text-grey-5">Unread</div>
              </q-card>
            </div>
          </div>
        </q-card>
      </div>
    </div>

    <q-dialog v-model="showCompose" persistent>
      <q-card class="sams-card bg-surface-1" style="min-width: 600px">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-white q-mb-md">New Announcement</div>
          <q-form @submit="sendAnnouncement">
            <q-input v-model="compose.title" label="Title" dark outlined class="q-mb-md" :rules="[(v: string) => !!v || 'Required']" />
            <q-input v-model="compose.body" label="Message" type="textarea" dark outlined class="q-mb-md" :rules="[(v: string) => !!v || 'Required']" />
            <q-select v-model="compose.channel" :options="channelOptions" label="Channel" dark outlined class="q-mb-md" />
            <q-select v-model="compose.recipients" :options="recipientOptions" label="Recipients" dark outlined class="q-mb-md" multiple />
            <div class="row justify-end q-gutter-md">
              <q-btn flat label="Cancel" color="grey-5" v-close-popup />
              <q-btn unelevated type="submit" label="Send" class="sams-btn sams-btn-primary" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useNotificationStore } from '../../stores/notifications'
import { useApi } from '../../composables/useApi'

const notificationStore = useNotificationStore()
const { post } = useApi()

const showCompose = ref(false)

const compose = reactive({
  title: '', body: '', channel: 'push', recipients: [] as string[],
})

const channelOptions = [
  { label: 'Push Notification', value: 'push' },
  { label: 'Email', value: 'email' },
  { label: 'SMS', value: 'sms' },
]

const recipientOptions = [
  { label: 'All Customers', value: 'all_customers' },
  { label: 'All Coaches', value: 'all_coaches' },
  { label: 'All Staff', value: 'all_staff' },
  { label: 'Entire Academy', value: 'all' },
]

function channelIcon(channel: string) {
  return { push: 'notifications', email: 'email', sms: 'sms' }[channel] || 'notifications'
}

async function sendAnnouncement() {
  await post('notifications/broadcast/', compose)
  showCompose.value = false
  notificationStore.fetchNotifications()
}

onMounted(() => {
  notificationStore.fetchNotifications()
})
</script>

<script lang="ts">
export default { name: 'CommunicationsPage' }
</script>
