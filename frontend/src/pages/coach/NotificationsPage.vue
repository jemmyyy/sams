<template>
  <q-page class="q-pa-xl animate-up">
    <div class="row items-end justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin text-white">Notifications</h1>
        <div class="text-subtitle1 text-grey-5">Stay updated on sessions, cancellations, and academy announcements.</div>
      </div>
      <q-btn v-if="notificationStore.unreadCount" unelevated class="sams-btn sams-btn-action" label="Mark All Read" icon="done_all" outline @click="notificationStore.markAllRead()" />
    </div>

    <q-card flat bordered class="sams-card">
      <q-list dark separator>
        <q-item v-for="n in notificationStore.notifications" :key="n.id" :class="{ 'bg-surface-2': !n.is_read }">
          <q-item-section avatar>
            <q-avatar :color="n.is_read ? 'grey-7' : 'primary'" text-color="white" :icon="channelIcon(n.channel)" />
          </q-item-section>
          <q-item-section @click="notificationStore.markRead(n.id)">
            <q-item-label class="text-white" :class="{ 'text-weight-bold': !n.is_read }">
              {{ n.title }}
            </q-item-label>
            <q-item-label caption class="text-grey-5">{{ n.body }}</q-item-label>
            <q-item-label caption class="text-grey-6 text-caption q-mt-xs">
              {{ n.sent_at }} · {{ n.channel }}
            </q-item-label>
          </q-item-section>
          <q-item-section side v-if="!n.is_read">
            <q-badge color="primary" rounded />
          </q-item-section>
        </q-item>
        <q-item v-if="!notificationStore.notifications.length" class="text-grey-5 text-center q-pa-lg">
          <q-item-section>No notifications</q-item-section>
        </q-item>
      </q-list>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useNotificationStore } from '../../stores/notifications'

const notificationStore = useNotificationStore()

function channelIcon(channel: string) {
  return { push: 'notifications', email: 'email', sms: 'sms' }[channel] || 'notifications'
}

onMounted(() => {
  notificationStore.fetchNotifications()
})
</script>

<script lang="ts">
export default { name: 'CoachNotificationsPage' }
</script>
