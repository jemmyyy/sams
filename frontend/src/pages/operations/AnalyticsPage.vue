<template>
  <q-page class="q-pa-xl animate-up">
    <div class="row items-center justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin text-white">Performance Intelligence</h1>
        <div class="text-subtitle1 text-grey-5">Advanced metrics and enrollment trends.</div>
      </div>
      <div class="row q-gutter-md">
         <q-btn flat unelevated class="sams-btn sams-btn-primary" label="Export Raw Data" icon="download" />
      </div>
    </div>

    <!-- Analytics KPI Grid -->
    <div class="row q-col-gutter-lg q-mb-xl">
      <div class="col-12 col-md-3" v-for="stat in analyticsStats" :key="stat.label">
        <q-card flat bordered class="sams-card q-pa-lg">
          <div class="text-caption text-grey-5 uppercase text-weight-bold letter-spacing-1 q-mb-xs">{{ stat.label }}</div>
          <div class="text-h4 text-heading text-white">{{ stat.value }}</div>
          <div :class="`text-caption q-mt-sm ${stat.positive ? 'text-positive' : 'text-negative'}`">
            <q-icon :name="stat.positive ? 'trending_up' : 'trending_down'" /> {{ stat.trend }} vs last period
          </div>
        </q-card>
      </div>
    </div>

    <!-- Chart Placeholder Section -->
    <div class="row q-col-gutter-lg">
      <div class="col-12 col-md-8">
        <q-card flat bordered class="sams-card bg-surface-1 q-pa-xl" style="min-height: 450px">
           <div class="text-heading text-h6 q-mb-xl text-white">Revenue Stream (MTD)</div>
           <div class="flex flex-center column q-gutter-y-md opacity-20">
              <q-icon name="insights" size="80px" color="primary" />
              <div class="text-h6 text-weight-light text-white">Visualizing dataset...</div>
           </div>
        </q-card>
      </div>
      
      <div class="col-12 col-md-4">
        <q-card flat bordered class="sams-card bg-surface-1 q-pa-xl" style="min-height: 450px">
           <div class="text-heading text-h6 q-mb-xl text-white">Attendance Pulse</div>
           <div class="flex flex-center">
              <q-knob
                readonly
                v-model="pulse"
                size="180px"
                :thickness="0.12"
                color="primary"
                track-color="surface-2"
                class="text-primary text-h4 text-heading"
                show-value
              >
                {{ pulse }}%
              </q-knob>
           </div>
           <div class="text-center q-mt-xl text-grey-5">Average across all groups</div>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
const pulse = ref(0);

const analyticsStats = ref<any[]>([]); // To be fetched from API
</script>

<style lang="scss" scoped>
.bg-surface-1 { background-color: var(--sams-surface-1); }
.bg-surface-2 { background-color: var(--sams-surface-2); }
.opacity-20 { opacity: 0.2; }
.letter-spacing-1 { letter-spacing: 1px; }
</style>
