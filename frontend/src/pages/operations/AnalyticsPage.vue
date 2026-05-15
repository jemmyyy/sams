<template>
  <q-page class="q-pa-xl animate-up">
    <div class="row items-center justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin">Performance Intelligence</h1>
        <div class="text-subtitle1 text-grey-6">Advanced metrics and enrollment trends.</div>
      </div>
      <div class="row q-gutter-md">
         <q-btn flat unelevated class="sams-btn sams-btn-primary" label="Export Raw Data" icon="download" />
      </div>
    </div>

    <!-- Analytics KPI Grid -->
    <div class="row q-col-gutter-lg q-mb-xl">
      <div class="col-12 col-md-3" v-for="stat in analyticsStats" :key="stat.label">
        <q-card flat bordered class="sams-card q-pa-lg">
          <div class="text-caption text-grey-6 uppercase text-weight-bold letter-spacing-1 q-mb-xs">{{ stat.label }}</div>
          <div class="text-h4 text-heading text-navy">{{ stat.value }}</div>
          <div :class="`text-caption q-mt-sm ${stat.positive ? 'text-positive' : 'text-negative'}`">
            <q-icon :name="stat.positive ? 'trending_up' : 'trending_down'" /> {{ stat.trend }} vs last period
          </div>
        </q-card>
      </div>
    </div>

    <!-- Chart Placeholder Section -->
    <div class="row q-col-gutter-lg">
      <div class="col-12 col-md-8">
        <q-card flat bordered class="sams-card q-pa-xl" style="min-height: 450px">
           <div class="text-heading text-h6 q-mb-xl">Revenue Stream (MTD)</div>
           <div class="flex flex-center column q-gutter-y-md opacity-20">
              <q-icon name="insights" size="80px" color="primary" />
              <div class="text-h6 text-weight-light">Visualizing dataset...</div>
           </div>
        </q-card>
      </div>
      
      <div class="col-12 col-md-4">
        <q-card flat bordered class="sams-card q-pa-xl" style="min-height: 450px">
           <div class="text-heading text-h6 q-mb-xl">Attendance Pulse</div>
           <div class="flex flex-center">
              <q-knob
                readonly
                v-model="pulse"
                size="180px"
                :thickness="0.12"
                color="primary"
                track-color="blue-1"
                class="text-primary text-h4 text-heading"
                show-value
              >
                {{ pulse }}%
              </q-knob>
           </div>
           <div class="text-center q-mt-xl text-grey-6">Average across all groups</div>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
const pulse = ref(92);

const analyticsStats = [
  { label: 'Net Revenue', value: '42,500 EGP', trend: '+12.5%', positive: true },
  { label: 'Conversion Rate', value: '18.4%', trend: '+2.1%', positive: true },
  { label: 'Churn Rate', value: '1.2%', trend: '-0.5%', positive: true },
  { label: 'Coach ROI', value: '4.2x', trend: '+0.8x', positive: true },
];
</script>
