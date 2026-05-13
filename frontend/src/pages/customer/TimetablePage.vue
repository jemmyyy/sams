<template>
  <q-page class="q-pa-md">
    <div class="row q-col-gutter-md">
      <div class="col-12 col-md-8">
        <q-card flat bordered>
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">My Timetable</div>
            <q-space />
            <q-btn-toggle
              v-model="viewMode"
              flat
              toggle-color="primary"
              :options="[
                {label: 'Week', value: 'week'},
                {label: 'Month', value: 'month'}
              ]"
            />
          </q-card-section>

          <q-card-section>
            <!-- Calendar Placeholder -->
            <div class="calendar-placeholder flex flex-center bg-grey-2" style="height: 400px">
              <q-icon name="calendar_month" size="100px" color="grey-4" />
              <div class="text-grey-6">Calendar implementation goes here</div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card flat bordered>
          <q-card-section>
            <div class="text-h6">Upcoming Sessions</div>
          </q-card-section>
          <q-separator />
          <q-list separator>
            <q-item v-for="n in 3" :key="n" clickable>
              <q-item-section avatar>
                <q-icon name="event" color="primary" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Tennis Training</q-item-label>
                <q-item-label caption>Monday, 10:00 AM</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-badge color="green">Confirmed</q-badge>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const viewMode = ref('week');
</script>

<style scoped>
.calendar-placeholder {
  border-radius: 8px;
  border: 2px dashed #e0e0e0;
}
</style>
