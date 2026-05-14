<template>
  <q-page class="q-pa-lg">
    <div class="max-width-800 q-mx-auto">
      <div class="row items-center q-mb-xl">
        <div class="col">
          <h1 class="text-h4 text-weight-bold q-my-none">Notifications</h1>
          <p class="text-grey-7 q-mt-sm">Stay updated with academy events</p>
        </div>
        <div class="col-auto">
          <q-btn flat color="primary" label="Mark all as read" @click="markAllAsRead" />
        </div>
      </div>

      <q-list bordered separator class="bg-white" style="border-radius: 16px">
        <q-item v-for="notif in notifications" :key="notif.id" :class="notif.read_at ? 'text-grey-7' : 'bg-blue-1'" class="q-py-md">
          <q-item-section avatar>
            <q-avatar :color="notif.read_at ? 'grey-4' : 'info'" :text-color="notif.read_at ? 'grey-7' : 'white'" icon="notifications" />
          </q-item-section>

          <q-item-section>
            <q-item-label class="text-weight-bold">{{ notif.subject }}</q-item-label>
            <q-item-label>{{ notif.content }}</q-item-label>
            <q-item-label caption class="q-mt-xs">{{ notif.created_at }}</q-item-label>
          </q-item-section>

          <q-item-section side v-if="!notif.read_at">
            <q-btn flat round dense icon="check" color="primary" @click="markAsRead(notif.id)">
              <q-tooltip>Mark as read</q-tooltip>
            </q-btn>
          </q-item-section>
        </q-item>
        
        <q-item v-if="notifications.length === 0" class="text-center q-pa-xl">
          <q-item-section>
            <q-icon name="notifications_off" size="64px" color="grey-4" class="q-mb-md" />
            <div class="text-h6 text-grey-5">No notifications yet</div>
          </q-item-section>
        </q-item>
      </q-list>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const notifications = ref([
  { id: 1, subject: 'Payment Received', content: 'Thank you! We received your payment for Invoice #102.', created_at: '2 hours ago', read_at: null },
  { id: 2, subject: 'Session Cancelled', content: 'The training session today at 4 PM has been cancelled due to weather.', created_at: '5 hours ago', read_at: null },
  { id: 3, subject: 'Welcome to SAMS', content: 'Your academy account has been successfully set up.', created_at: '2 days ago', read_at: '2026-05-13' },
]);

function markAsRead(id: number) {
  const n = notifications.value.find(x => x.id === id);
  if (n) n.read_at = 'now';
}

function markAllAsRead() {
  notifications.value.forEach(n => n.read_at = 'now');
}
</script>

<style lang="scss" scoped>
.max-width-800 { max-width: 800px; }
</style>
