<template>
  <q-page class="q-pa-md">
    <div class="row q-col-gutter-md">
      <!-- Player Header -->
      <div class="col-12">
        <q-card flat bordered class="bg-primary text-white">
          <q-card-section class="row items-center">
            <q-avatar size="100px" class="q-mr-md bg-white text-primary">
              <q-icon name="person" />
            </q-avatar>
            <div>
              <div class="text-h4">Adam Smith</div>
              <div class="text-subtitle1">Under 12 - Elite Group</div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Progress Stats -->
      <div class="col-12 col-md-6">
        <q-card flat bordered>
          <q-card-section>
            <div class="text-h6">Performance Ratings</div>
          </q-card-section>
          <q-card-section>
            <div class="row q-col-gutter-sm">
              <div class="col-6" v-for="skill in skills" :key="skill.name">
                <div class="text-caption">{{ skill.name }}</div>
                <q-linear-progress :value="skill.value" size="10px" color="orange" class="q-mt-xs" />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Attendance Summary -->
      <div class="col-12 col-md-6">
        <q-card flat bordered>
          <q-card-section>
            <div class="text-h6">Attendance History</div>
          </q-card-section>
          <q-card-section class="flex flex-center">
             <q-knob
              readonly
              v-model="attendanceRate"
              show-value
              size="120px"
              :thickness="0.15"
              color="primary"
              track-color="grey-3"
              class="text-primary q-ma-md"
            >
              {{ attendanceRate }}%
            </q-knob>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const attendanceRate = ref(92);
const skills = [
  { name: 'Technique', value: 0.8 },
  { name: 'Stamina', value: 0.7 },
  { name: 'Strategy', value: 0.9 },
  { name: 'Teamwork', value: 0.85 }
];
</script>
