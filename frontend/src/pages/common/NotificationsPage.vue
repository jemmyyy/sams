<template>
  <q-page class="q-pa-xl animate-up">
    <div class="max-w-lg q-mx-auto">
      <div class="row items-center justify-between q-mb-xl">
        <div class="column">
          <h1 class="text-heading heading-lg no-margin">Notifications</h1>
          <div class="text-subtitle1 text-grey-6">Stay synchronized with academy activity.</div>
        </div>
        <q-btn flat color="primary" label="Mark all as read" class="sams-btn" />
      </div>

      <q-card flat bordered class="sams-card">
        <q-list separator>
          <q-item v-for="n in notifications" :key="n.id" class="q-py-lg" :class="n.read ? 'opacity-60' : 'bg-blue-50'">
            <q-item-section avatar>
              <q-avatar :color="n.read ? 'grey-2' : 'primary'" :text-color="n.read ? 'grey-6' : 'white'" icon="notifications_none" />
            </q-item-section>

            <q-item-section>
              <q-item-label class="text-weight-bold text-navy">{{ n.title }}</q-item-label>
              <q-item-label class="text-grey-7">{{ n.content }}</q-item-label>
              <q-item-label caption class="q-mt-xs">{{ n.time }}</q-item-label>
            </q-item-section>

            <q-item-section side v-if="!n.read">
              <q-btn flat round icon="done" color="primary" />
            </q-item-section>
          </q-item>
        </q-list>
      </q-card>
    </div>
  </q-page>
</template>

<script setup lang="ts">
const notifications = [
  { id: 1, title: 'Session Completed', content: 'Attendance has been finalized for Football U16.', time: '10 mins ago', read: false },
  { id: 2, title: 'Payment Verified', content: 'Payment of 500 EGP from Athlete #042 confirmed.', time: '1 hour ago', read: false },
  { id: 3, title: 'New Report Ready', content: 'Your requested Weekly Export is ready for download.', time: '2 hours ago', read: true },
];
</script>

<style lang="scss" scoped>
.max-w-lg { max-width: 800px; }
.opacity-60 { opacity: 0.6; }
.bg-blue-50 { background-color: #eff6ff; }
</style>
